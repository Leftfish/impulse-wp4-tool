# IMPULSE WP4 Copyright Assessment Tool

A Flask-based web application for assessing copyright status and digital representation rights of cultural heritage objects.

## Overview

This tool helps cultural heritage institutions evaluate:
- Copyright status of original objects
- Digital representation rights
- Online availability permissions
- IP rights coverage and acquisition status

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Local Development Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-directory]
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment on PythonAnywhere

1. Sign up for a PythonAnywhere account at https://www.pythonanywhere.com/

2. Go to the PythonAnywhere dashboard and open a Bash console

3. Clone your repository:
```bash
git clone [your-repository-url]
cd [repository-directory]
```

4. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure the web app:
   - Go to the "Web" tab in PythonAnywhere
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.11
   - Set the following configuration:
     - Source code: `/home/yourusername/[repository-directory]`
     - Working directory: `/home/yourusername/[repository-directory]`
     - Virtual environment: `/home/yourusername/[repository-directory]/venv`

6. Modify the WSGI configuration file:
   - Click on the WSGI configuration file link
   - Replace the contents with:
```python
import sys
import os

path = '/home/yourusername/[repository-directory]'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
application.secret_key = 'your-secret-key-here'  # Change this!
```

7. Reload the web app using the "Reload" button in the Web tab

Your application should now be available at `yourusername.pythonanywhere.com`

## Security Considerations

1. Change the secret key:
   - In `app.py`, replace the default secret key with a secure one
   - For production, use an environment variable:
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key-for-development')
```

2. Enable HTTPS:
   - PythonAnywhere provides HTTPS by default
   - For other deployments, use HTTPS in production

## Project Structure

```
.
├── app.py              # Main application file
├── forms.py            # Form definitions and validation
├── utils.py            # Utility functions and calculations
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   └── index.html     # Main form template
├── data/              # Data files
│   └── country_codes.py  # Country codes and EU/EEA status
├── tests/             # Test files
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**:
   - Ensure you're in the virtual environment
   - Verify all dependencies are installed
   - Check Python path in WSGI configuration

2. **Form Not Submitting**:
   - Verify CSRF token is properly configured
   - Check browser console for JavaScript errors
   - Ensure form fields match expected types

3. **PythonAnywhere Specific**:
   - If static files aren't loading, check the Static Files configuration
   - For 502 errors, check the error logs in the Web tab
   - Ensure working directory and virtual environment paths are correct

### Getting Help

For issues with:
- The application: Open an issue in the repository
- PythonAnywhere: Consult their help pages or forums
- Flask-specific questions: Refer to Flask documentation

## Development Notes

- The application uses Flask-WTF for form handling
- Form validation includes complex business logic for copyright assessment
- Test suite covers core calculation functionality
- Frontend uses Bootstrap for responsive design

## License

[Your license information here] 