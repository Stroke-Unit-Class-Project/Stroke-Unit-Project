# Mobile Stroke Unit System

A Django-based web application for managing mobile stroke unit patient data and remote neurologist consultations.

## Features

- Patient data management
- Vital signs tracking
- Lab results recording
- Imaging studies management
- Remote neurologist consultations
- NIHSS score tracking

## Requirements

- Python 3.8+
- Django 5.2
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stroke_unit_system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://localhost:8000

## Usage

1. Log in to the admin interface at http://localhost:8000/admin to manage data
2. Access the main application at http://localhost:8000
3. Add new patients and their related data through the user interface
4. View and manage patient records, vital signs, lab results, and consultations

## Project Structure

- `core/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions and classes
  - `forms.py` - Form definitions
  - `templates/` - HTML templates
  - `admin.py` - Admin interface configuration
- `static/` - Static files (CSS, JavaScript)
- `stroke_unit/` - Project settings and configuration

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 