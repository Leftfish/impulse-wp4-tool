# IMPULSE WP4 Copyright Assessment Tool

This is a tool designed as part of the efforts of [IMPULSE](https://euimpulse.eu/) WP4, based on our earlier conclusions described in deliverables D4.1 and D4.2, as well as the datasets prepared as part of WP3's deliverable D3.2. It is a Flask-based web application for assessing copyright status and digital representation rights of cultural heritage objects. 

Functionally, its aim is to streamline the process of combining information about an object and its digital representation to verify if, under EU law, they can be made available online under relatively free circumstances (i.e. including making changes such as those allowed by the IMPULSE platform). The fact that we mention "EU law" here is important, as the tool does not take into account any national variations or additional protections. This is why, although we designed it with the principle of "erring on the side of caution" in mind, it cannot be treated as a complete substitute for legal advice. 

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

## Running tests

Run the full test suite from the command line:

```bash
python -m pytest -v
```

### Running tests in VS Code

To run tests in Visual Studio Code:

1. Open the project folder in VS Code.
2. Install the Python extension (ms-python.python) and select your interpreter (Ctrl+Shift+P → Python: Select Interpreter).
3. Configure tests: Ctrl+Shift+P → “Python: Configure Tests”, choose “pytest”, select the `tests` folder.
4. Use the Testing sidebar (beaker icon) to run all tests or individual tests, or press Ctrl+Shift+P → “Python: Run All Tests”.

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
   - Click "Add a new web app" (or modify existing)
   - Choose "Manual configuration"
   - Select Python 3.11
   - Set the following configuration:
     - Source code: `/home/yourusername/[repository-directory]`
     - Working directory: `/home/yourusername/[repository-directory]`
     - Virtual environment: `/home/yourusername/[repository-directory]/venv`

6. Configure Static Files:
   - In the Web tab, under "Static files"
   - Add the following mappings:
     - URL: `/static/` → Directory: `/home/yourusername/[repository-directory]/static`
     - URL: `/img/` → Directory: `/home/yourusername/[repository-directory]/static/img`

7. Modify the WSGI configuration file:
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

8. Update the application:
   - In the Bash console:
```bash
cd [repository-directory]
git pull  # Get latest changes
source venv/bin/activate
pip install -r requirements.txt  # Update dependencies if needed
```

9. Reload the web app:
   - Go to the Web tab
   - Click the "Reload" button

Your application should now be available at `yourusername.pythonanywhere.com`

## Updating an Existing Deployment

To update an existing PythonAnywhere deployment:

1. SSH into your PythonAnywhere account or use the Bash console

2. Navigate to your project directory:
```bash
cd [repository-directory]
```

3. Pull the latest changes:
```bash
git pull
```

4. Update dependencies if needed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

5. Reload the web app from the Web tab

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
├── app.py                # Main application file
├── forms.py              # Form definitions and validation
├── utils.py              # Utility functions and calculations
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── index.html        # Main form template
├── static/               # Static files
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── img/              # Images
├── data/                 # Data files
│   └── country_codes.py  # Country codes and EU/EEA status
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── README.md             # This file
```
