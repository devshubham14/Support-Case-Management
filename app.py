from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Case, CaseNote
from forms import LoginForm, RegistrationForm, CaseForm, CaseUpdateForm, CaseAssignmentForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_agent=form.is_agent.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_agent:
        cases = Case.query.all()
    else:
        cases = Case.query.filter_by(customer_id=current_user.id).all()
    return render_template('dashboard.html', cases=cases)

@app.route('/case/new', methods=['GET', 'POST'])
@login_required
def new_case():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status='Open',
            customer_id=current_user.id
        )
        db.session.add(case)
        db.session.commit()
        flash('Case created successfully!')
        return redirect(url_for('dashboard'))
    return render_template('new_case.html', form=form)

@app.route('/case/<int:case_id>')
@login_required
def view_case(case_id):
    case = Case.query.get_or_404(case_id)
    if not current_user.is_agent and case.customer_id != current_user.id:
        flash('You do not have permission to view this case.')
        return redirect(url_for('dashboard'))
    return render_template('view_case.html', case=case)

@app.route('/case/<int:case_id>/update', methods=['GET', 'POST'])
@login_required
def update_case(case_id):
    if not current_user.is_agent:
        flash('Only support agents can update cases.')
        return redirect(url_for('dashboard'))
    
    case = Case.query.get_or_404(case_id)
    form = CaseUpdateForm()
    
    if form.validate_on_submit():
        case.status = form.status.data
        note = CaseNote(
            content=form.note.data,
            case_id=case.id,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Case updated successfully!')
        return redirect(url_for('view_case', case_id=case.id))
    
    return render_template('update_case.html', form=form, case=case)

@app.route('/case/<int:case_id>/assign', methods=['GET', 'POST'])
@login_required
def assign_case(case_id):
    if not current_user.is_agent:
        flash('Only support agents can assign cases.')
        return redirect(url_for('dashboard'))
    
    case = Case.query.get_or_404(case_id)
    form = CaseAssignmentForm()
    form.agent_id.choices = [(a.id, a.username) for a in User.query.filter_by(is_agent=True).all()]
    
    if form.validate_on_submit():
        case.agent_id = form.agent_id.data
        db.session.commit()
        flash('Case assigned successfully!')
        return redirect(url_for('view_case', case_id=case.id))
    
    return render_template('assign_case.html', form=form, case=case)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 