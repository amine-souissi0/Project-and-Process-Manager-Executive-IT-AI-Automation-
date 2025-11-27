# SOP – Automation & AI Implementation

**Document Version:** 1.0  
**Date:** 2024  
**Department:** IT, AI & Automation  
**Purpose:** Standard Operating Procedure for implementing automation and AI features in Ulink Assist Operations

---

## 1. Overview

This SOP outlines the procedures for implementing, maintaining, and monitoring automation and AI features within the Ulink Assist Operations system. The system demonstrates capabilities in:

- Automated email notifications
- AI-powered triage and priority assessment
- Text summarization using NLP
- Automatic SOP generation
- Data backup and security

---

## 2. Automation Features

### 2.1 Email Notification Automation

**Purpose:** Automatically notify patients and stakeholders when request status changes.

**Implementation:**
- Location: `automation/email_notification.py`
- Trigger: Status change events
- Output: Simulated email (console + activity log)

**Workflow:**
1. Status change detected in `routes/main_routes.py`
2. `EmailNotificationService.notify_status_change()` called
3. Email template selected based on new status
4. Email logged to console and activity.log
5. In production: Email sent via SMTP/API

**Configuration:**
- Enable/disable: `Config.EMAIL_NOTIFICATIONS_ENABLED`
- Email templates: Customizable in `EmailNotificationService`

**Monitoring:**
- Check `activity.log` for email notification entries
- Monitor for failed notifications
- Review email delivery rates (in production)

---

### 2.2 AI Triage Assistant

**Purpose:** Automatically analyze requests and provide intelligent suggestions for priority, workflow, and next steps.

**Implementation:**
- Location: `automation/ai_triage.py`
- Trigger: New request creation
- Method: Rule-based AI with keyword analysis

**Workflow:**
1. New request submitted
2. `AITriageService.analyze_request()` called
3. Analysis performed on:
   - Request type
   - Description keywords
   - Urgency indicators
4. Recommendations generated:
   - Priority level
   - Workflow suggestion
   - Next steps
   - Key suggestions
5. Results stored in request data

**Analysis Criteria:**
- **Request Type Analysis:**
  - Medical Evacuation → Urgent priority
  - Teleconsultation → Standard workflow
  - Hospital Booking → Coordination workflow
  
- **Keyword Analysis:**
  - High urgency: "urgent", "emergency", "critical"
  - Medical conditions: "pain", "accident", "surgery", "cancer"
  - Scoring system: 0-5+ urgency score

**Enhancement Opportunities:**
- Integrate machine learning models
- Use NLP libraries (spaCy, NLTK)
- Connect to medical knowledge base
- Implement predictive analytics

---

### 2.3 Text Summarization

**Purpose:** Automatically summarize long request descriptions for quick review.

**Implementation:**
- Location: `automation/text_summarization.py`
- Method: Extractive summarization
- Output: 2-3 sentence summary

**Workflow:**
1. Request description analyzed
2. Sentences scored based on:
   - Position in text
   - Length
   - Keyword presence
   - Medical terminology
3. Top sentences selected
4. Summary generated and stored

**Scoring Algorithm:**
- Beginning sentences: +2 points
- Long sentences (>100 chars): +1 point
- Contains numbers: +1 point
- Question words: +1 point
- Medical keywords: +1 point each

**Enhancement Opportunities:**
- Abstractive summarization (GPT, BERT)
- Multi-language support
- Context-aware summarization
- Integration with medical ontologies

---

### 2.4 SOP Generation

**Purpose:** Automatically generate Standard Operating Procedure templates based on request type.

**Implementation:**
- Location: `automation/sop_generator.py`
- Method: Template-based generation
- Output: Structured SOP document

**Workflow:**
1. Request type identified
2. Appropriate SOP template selected
3. Template populated with:
   - Procedure steps
   - Required documents
   - Communication flow
   - Timeline
   - Stakeholders
4. SOP formatted and made available for download

**SOP Templates Available:**
- Teleconsultation
- Hospital Booking
- Medical Evacuation
- Case Inquiry
- Default template for other types

**Enhancement Opportunities:**
- Dynamic SOP generation based on case specifics
- Integration with document management system
- Version control for SOPs
- Multi-language SOP generation

---

## 3. Security & Data Protection

### 3.1 Input Sanitization

**Purpose:** Prevent injection attacks and data corruption.

**Implementation:**
- Location: `security/input_sanitizer.py`
- Applied to: All user inputs

**Sanitization Methods:**
- String sanitization: HTML escaping, length limits
- Email validation: Regex pattern matching
- Phone sanitization: Character filtering
- Request ID validation: Alphanumeric only
- Text area sanitization: Preserve formatting

**Best Practices:**
- Always sanitize before database storage
- Validate against allowed values
- Log suspicious inputs
- Regular security audits

---

### 3.2 Authentication & Authorization

**Purpose:** Control access based on user roles.

**Implementation:**
- Location: `security/auth_service.py`
- Method: Password hashing (Werkzeug)

**Roles:**
- **Admin:** Full access (create, read, update, delete, manage users)
- **Staff:** Create, read, update requests
- **Viewer:** Read-only access

**Security Features:**
- Password hashing: PBKDF2 with SHA256
- Session management
- Role-based permissions
- Security event logging

---

### 3.3 Data Backup

**Purpose:** Automatic backup of database to prevent data loss.

**Implementation:**
- Location: `services/database_service.py`
- Frequency: Before each save operation
- Retention: Last 10 backups

**Backup Process:**
1. Before saving, create timestamped backup
2. Store in `backups/` directory
3. Clean up old backups (keep 10 most recent)
4. Log backup operations

**Recovery Procedure:**
1. Identify backup file by timestamp
2. Copy backup to `database.json`
3. Restart application
4. Verify data integrity

---

## 4. Monitoring & Maintenance

### 4.1 Activity Logging

**Location:** `activity.log`

**Log Types:**
- Info: General operations
- Security: Authentication events
- Error: System errors
- Automation: AI/automation actions

**Log Format:**
```
[YYYY-MM-DD HH:MM:SS] [TYPE] [USER] Message
```

**Monitoring:**
- Review logs daily
- Check for errors
- Monitor security events
- Track automation performance

---

### 4.2 Performance Monitoring

**Metrics to Track:**
- Request processing time
- AI analysis duration
- Database operation speed
- Email notification delivery

**Optimization:**
- Cache frequently accessed data
- Optimize database queries
- Use async operations for long tasks
- Monitor memory usage

---

## 5. Troubleshooting

### 5.1 Automation Not Working

**Symptoms:**
- No email notifications
- AI triage not running
- Summaries not generated

**Solutions:**
1. Check `Config` settings (automation enabled?)
2. Review `activity.log` for errors
3. Verify service initialization
4. Check database connectivity

---

### 5.2 AI Analysis Issues

**Symptoms:**
- Incorrect priority recommendations
- Missing workflow suggestions

**Solutions:**
1. Review keyword patterns in `ai_triage.py`
2. Update urgency keywords
3. Adjust scoring algorithm
4. Test with sample requests

---

## 6. Future Enhancements

### 6.1 Machine Learning Integration
- Train models on historical data
- Predictive priority assessment
- Pattern recognition for similar cases

### 6.2 Advanced NLP
- Sentiment analysis
- Entity extraction (names, dates, locations)
- Multi-language support

### 6.3 Integration Opportunities
- Email service APIs (SendGrid, AWS SES)
- Cloud AI services (OpenAI, Google Cloud AI)
- Document management systems
- CRM integration

---

## 7. Contact & Support

**IT Support:**  
Email: ops@ulinkassist.com  
Phone: +65 6835 0388

**Document Owner:**  
Project and Process Manager Executive (IT, AI & Automation)

---

**Last Updated:** 2024  
**Next Review:** Quarterly

