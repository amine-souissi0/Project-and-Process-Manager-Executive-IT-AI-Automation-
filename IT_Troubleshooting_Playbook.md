# IT Troubleshooting Playbook

**Document Version:** 1.0  
**Date:** 2024  
**Department:** IT Support  
**Purpose:** Quick reference guide for common IT issues and resolutions

---

## 1. Application Startup Issues

### Issue: Application won't start

**Symptoms:**
- Error: "Module not found"
- Port already in use
- Database file errors

**Solutions:**

#### Module Not Found
```bash
# Install dependencies
py -m pip install -r requirements.txt

# Or on Linux/Mac
pip install -r requirements.txt
```

#### Port Already in Use
```python
# Edit app.py, change port:
app.run(debug=True, host='127.0.0.1', port=5001)  # Change from 5000
```

#### Database File Errors
```bash
# Delete and recreate database
rm database.json
# Restart application (will auto-create)
```

---

## 2. Database Issues

### Issue: Database corruption

**Symptoms:**
- JSON decode errors
- Missing data
- Application crashes on load

**Solutions:**

1. **Check database file:**
   ```bash
   # Verify JSON is valid
   python -m json.tool database.json
   ```

2. **Restore from backup:**
   ```bash
   # List backups
   ls backups/
   
   # Restore specific backup
   cp backups/database_backup_YYYYMMDD_HHMMSS.json database.json
   ```

3. **Manual fix:**
   - Open `database.json` in text editor
   - Validate JSON syntax
   - Ensure proper array structure: `[{...}, {...}]`

---

### Issue: Data not saving

**Symptoms:**
- Changes not persisting
- New requests not appearing

**Solutions:**

1. **Check file permissions:**
   ```bash
   # Ensure write permissions
   chmod 644 database.json
   ```

2. **Check disk space:**
   ```bash
   df -h  # Linux/Mac
   # Or check in Windows
   ```

3. **Review activity log:**
   ```bash
   tail -f activity.log
   # Look for save errors
   ```

4. **Verify backup directory exists:**
   ```bash
   mkdir -p backups
   ```

---

## 3. Authentication Issues

### Issue: Can't login

**Symptoms:**
- "Invalid username or password"
- Session not persisting

**Solutions:**

1. **Verify credentials:**
   - Admin: `admin` / `admin123`
   - Staff: `staff` / `staff123`
   - Viewer: `viewer` / `viewer123`

2. **Clear browser session:**
   - Clear cookies
   - Try incognito/private mode

3. **Check session configuration:**
   - Verify `SECRET_KEY` in `config.py`
   - Check session cookie settings

---

### Issue: Permission denied errors

**Symptoms:**
- "You don't have permission"
- Actions blocked

**Solutions:**

1. **Check user role:**
   - Verify role in session
   - Check `security/auth_service.py` permissions

2. **Role requirements:**
   - Admin: Full access
   - Staff: Create, read, update
   - Viewer: Read only

---

## 4. Automation Issues

### Issue: Email notifications not working

**Symptoms:**
- No email output
- Notifications not logged

**Solutions:**

1. **Check configuration:**
   ```python
   # In config.py
   EMAIL_NOTIFICATIONS_ENABLED = True
   ```

2. **Verify service initialization:**
   - Check `routes/main_routes.py`
   - Ensure `EmailNotificationService` imported

3. **Review activity log:**
   ```bash
   grep "Email notification" activity.log
   ```

4. **Test manually:**
   ```python
   from automation.email_notification import EmailNotificationService
   service = EmailNotificationService()
   service.send_notification("test@example.com", "Test", "Test message")
   ```

---

### Issue: AI Triage not running

**Symptoms:**
- No AI suggestions
- Missing priority recommendations

**Solutions:**

1. **Check if enabled:**
   ```python
   # In config.py
   AI_TRIAGE_ENABLED = True
   ```

2. **Verify request data:**
   - Check `request_data` has required fields
   - Verify description is not empty

3. **Test triage service:**
   ```python
   from automation.ai_triage import AITriageService
   service = AITriageService()
   result = service.analyze_request(request_data)
   print(result)
   ```

4. **Review keyword patterns:**
   - Check `automation/ai_triage.py`
   - Update keywords if needed

---

### Issue: Text summarization errors

**Symptoms:**
- No summary generated
- Summary too short/long

**Solutions:**

1. **Check input text:**
   - Minimum 50 characters required
   - Verify description exists

2. **Adjust parameters:**
   ```python
   # In automation/text_summarization.py
   summarize(text, max_sentences=3)  # Adjust as needed
   ```

3. **Test summarization:**
   ```python
   from automation.text_summarization import TextSummarizationService
   service = TextSummarizationService()
   summary = service.summarize("Long text here...")
   ```

---

## 5. Performance Issues

### Issue: Application slow

**Symptoms:**
- Slow page loads
- Delayed responses

**Solutions:**

1. **Check database size:**
   ```bash
   # Large database files slow down operations
   ls -lh database.json
   ```

2. **Optimize database:**
   - Archive old requests
   - Remove unnecessary data

3. **Check activity log size:**
   ```bash
   # Large logs can slow operations
   ls -lh activity.log
   # Rotate if needed
   mv activity.log activity.log.old
   touch activity.log
   ```

4. **Review backup directory:**
   ```bash
   # Too many backups can slow saves
   ls backups/ | wc -l
   # Clean up old backups (keep last 10)
   ```

---

### Issue: High memory usage

**Symptoms:**
- Application crashes
- System slowdown

**Solutions:**

1. **Check Python processes:**
   ```bash
   # Linux/Mac
   ps aux | grep python
   
   # Windows
   tasklist | findstr python
   ```

2. **Restart application:**
   - Stop current instance
   - Clear Python cache: `rm -r __pycache__`
   - Restart

3. **Optimize code:**
   - Load only necessary data
   - Use pagination for large lists
   - Implement caching

---

## 6. Security Issues

### Issue: Input validation errors

**Symptoms:**
- Special characters causing issues
- SQL injection attempts (if using SQL)

**Solutions:**

1. **Verify sanitization:**
   - Check `security/input_sanitizer.py`
   - Ensure all inputs sanitized

2. **Review logs:**
   ```bash
   grep "security" activity.log
   # Look for suspicious patterns
   ```

3. **Update sanitization rules:**
   - Add new patterns as needed
   - Test with various inputs

---

### Issue: Session security concerns

**Symptoms:**
- Sessions not expiring
- Unauthorized access

**Solutions:**

1. **Check session configuration:**
   ```python
   # In config.py
   SESSION_COOKIE_SECURE = True  # For HTTPS
   SESSION_COOKIE_HTTPONLY = True
   SESSION_TIMEOUT = timedelta(hours=8)
   ```

2. **Implement session timeout:**
   - Check session age
   - Force logout after timeout

3. **Review authentication:**
   - Verify password hashing
   - Check role assignments

---

## 7. Language/Translation Issues

### Issue: Translations not working

**Symptoms:**
- Text not translated
- Language switcher not working

**Solutions:**

1. **Check session:**
   ```python
   # Verify language in session
   session.get('language', 'en')
   ```

2. **Verify translation file:**
   - Check `translations.py` exists
   - Verify language codes ('en', 'id')

3. **Clear session:**
   - Logout and login again
   - Set language preference

4. **Check template:**
   - Verify `translations` passed to template
   - Check translation keys exist

---

## 8. UI/Display Issues

### Issue: Logo not displaying

**Symptoms:**
- Logo image missing
- Broken image icon

**Solutions:**

1. **Verify file exists:**
   ```bash
   ls static/images/logo.svg
   ```

2. **Check file path:**
   ```html
   <!-- In template -->
   {{ url_for('static', filename='images/logo.svg') }}
   ```

3. **Verify static folder:**
   - Check Flask static folder configuration
   - Ensure proper file permissions

---

### Issue: Charts not loading

**Symptoms:**
- Empty chart containers
- JavaScript errors

**Solutions:**

1. **Check Chart.js CDN:**
   ```html
   <!-- Verify CDN link in template -->
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
   ```

2. **Check API endpoint:**
   ```bash
   # Test API
   curl http://127.0.0.1:5000/api/stats
   ```

3. **Browser console:**
   - Open browser developer tools
   - Check for JavaScript errors
   - Verify API responses

---

## 9. Backup & Recovery

### Issue: Need to restore data

**Procedure:**

1. **List available backups:**
   ```bash
   ls -lt backups/
   ```

2. **Select backup:**
   - Choose most recent or specific date

3. **Restore:**
   ```bash
   cp backups/database_backup_YYYYMMDD_HHMMSS.json database.json
   ```

4. **Verify:**
   ```bash
   python -m json.tool database.json
   # Should show valid JSON
   ```

5. **Restart application**

---

## 10. Common Error Messages

### "JSONDecodeError"
- **Cause:** Corrupted database file
- **Fix:** Restore from backup or fix JSON syntax

### "Permission denied"
- **Cause:** File permissions or role restrictions
- **Fix:** Check file permissions and user role

### "ModuleNotFoundError"
- **Cause:** Missing Python package
- **Fix:** Install requirements: `pip install -r requirements.txt`

### "Port already in use"
- **Cause:** Another process using port 5000
- **Fix:** Change port in `app.py` or stop other process

---

## 11. Quick Diagnostic Commands

```bash
# Check Python version
python --version  # or py --version on Windows

# Check installed packages
pip list

# Validate JSON
python -m json.tool database.json

# Check log file
tail -f activity.log

# Test application
curl http://127.0.0.1:5000/

# Check file permissions
ls -la database.json
```

---

## 12. Escalation

If issue persists:

1. **Document:**
   - Error messages
   - Steps to reproduce
   - Screenshots/logs

2. **Contact:**
   - IT Support: ops@ulinkassist.com
   - Phone: +65 6835 0388

3. **Provide:**
   - Error logs from `activity.log`
   - System information
   - Recent changes made

---

**Last Updated:** 2024  
**Next Review:** Monthly

