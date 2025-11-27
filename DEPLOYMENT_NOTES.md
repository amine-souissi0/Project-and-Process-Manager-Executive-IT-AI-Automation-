# Deployment Notes

## For Recruiter/Interviewer

This is a **demonstration project** built for the Project and Process Manager Executive (IT, AI & Automation) role at Ulink Assist.

## Quick Setup

1. Install Python 3.8+ and dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   # or
   py app.py  # on Windows
   ```

3. Access at: `http://127.0.0.1:5000`

4. Login with demo credentials:
   - Admin: `admin` / `admin123`
   - Staff: `staff` / `staff123`
   - Viewer: `viewer` / `viewer123`

## Key Features Demonstrated

- ✅ Full-stack web application (Python/Flask)
- ✅ Automation workflows (email notifications, AI triage)
- ✅ AI features (text summarization, intelligent suggestions)
- ✅ Security (input sanitization, role-based access)
- ✅ Multi-language support (English/Indonesian)
- ✅ Professional documentation

## Important Notes

- **Email notifications** are simulated by default (displayed in console)
- **Database** uses JSON files (auto-created on first run)
- **All data** is stored locally in `database.json`
- **Activity logs** are saved to `activity.log`

## Documentation

- `README.md` - Complete project overview
- `SOP_Automation_AI_Implementation.md` - Automation procedures
- `IT_Troubleshooting_Playbook.md` - Troubleshooting guide
- `Information_Security_Policy_Lite.md` - Security policies

## Project Structure

```
├── app.py                    # Main application
├── config.py                 # Configuration
├── translations.py           # Multi-language support
├── routes/                   # Route handlers
├── services/                 # Business logic
├── automation/               # AI & automation features
├── security/                 # Security modules
├── templates/                # HTML templates
└── static/                   # Static files (CSS, images)
```

## Contact

For questions about this demo project, please refer to the comprehensive documentation in the README.md file.

