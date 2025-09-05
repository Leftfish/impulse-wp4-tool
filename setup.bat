@echo off
echo Setting up the IMPULSE WP4 Legal Verification Tool...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

:: Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt

echo Setup complete! You can now run the application with:
echo venv\Scripts\python app.py
echo or by using the run_app.bat script on Windows.

:: Keep the window open
pause 