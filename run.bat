@echo off
echo ========================================
echo Medical Assistance Request Tracker
echo Starting Flask Application...
echo ========================================
echo.
echo Installing dependencies...
py -m pip install -r requirements.txt
echo.
echo Starting server...
echo Open your browser to: http://127.0.0.1:5000
echo.
py app.py
pause

