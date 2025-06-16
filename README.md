# Support Case Management System

A web-based application for managing customer support cases, built with Flask and SQLite.

## Features

- Customer case submission and tracking
- Support agent case management
- Case status updates and assignment
- Basic reporting functionality
- User authentication for support agents

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:5000

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `forms.py`: Form definitions
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS)
- `instance/`: Database and configuration files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Shubham Pandey** - [@devshubham14](https://github.com/devshubham14)

## Acknowledgments

- Flask and its extensions for the web framework
- Bootstrap for the frontend design
- SQLite for the database 