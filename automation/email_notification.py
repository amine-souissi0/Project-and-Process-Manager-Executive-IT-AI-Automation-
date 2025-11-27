"""
Email Notification Automation Module
Sends real email notifications for status changes via SMTP
"""

from datetime import datetime
from services.logging_service import LoggingService
from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailNotificationService:
    """Service for automated email notifications"""
    
    def __init__(self):
        self.logger = LoggingService()
        # Email configuration from environment variables or config
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username or 'noreply@ulinkassist.com')
        self.enable_real_emails = os.environ.get('ENABLE_REAL_EMAILS', 'false').lower() == 'true'
    
    def send_notification(self, recipient_email, subject, body, request_id=None):
        """
        Send an email notification via SMTP
        
        If SMTP credentials are configured, sends real email.
        Otherwise, simulates email (prints to console).
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Try to send real email if configured
        if self.enable_real_emails and self.smtp_username and self.smtp_password:
            try:
                return self._send_real_email(recipient_email, subject, body, request_id, timestamp)
            except Exception as e:
                # If real email fails, fall back to simulation
                self.logger.log_error(
                    f"Failed to send real email to {recipient_email}: {str(e)}. Falling back to simulation.",
                    'System'
                )
        
        # Simulate email (for demo or if SMTP not configured)
        email_content = f"""
{'='*60}
EMAIL NOTIFICATION (SIMULATED)
{'='*60}
To: {recipient_email}
Subject: {subject}
Time: {timestamp}
Request ID: {request_id or 'N/A'}
{'='*60}
{body}
{'='*60}
"""
        
        # Log to console
        print(email_content)
        
        # Log to activity log
        self.logger.log_activity(
            f"Email notification (simulated) to {recipient_email}: {subject}",
            action_type='automation'
        )
        
        return {
            'success': True,
            'timestamp': timestamp,
            'recipient': recipient_email,
            'subject': subject,
            'method': 'simulated'
        }
    
    def _send_real_email(self, recipient_email, subject, body, request_id, timestamp):
        """Send real email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add body
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background-color: #0066cc; color: white; padding: 20px; text-align: center;">
                        <h1 style="margin: 0;">Ulink Assist</h1>
                    </div>
                    <div style="padding: 20px; background-color: #f8f9fa;">
                        {body.replace(chr(10), '<br>')}
                    </div>
                    <div style="padding: 20px; background-color: #ffffff; border-top: 1px solid #e9ecef;">
                        <p style="font-size: 12px; color: #6c757d; margin: 0;">
                            Request ID: {request_id or 'N/A'}<br>
                            Time: {timestamp}
                        </p>
                    </div>
                    <div style="background-color: #2c3e50; color: white; padding: 15px; text-align: center; font-size: 12px;">
                        <p style="margin: 0;">
                            Ulink Assist | +65 6835 0388 | ops@ulinkassist.com<br>
                            With 25+ years of experience in medical assistance
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable encryption
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            # Log success
            self.logger.log_activity(
                f"Real email sent successfully to {recipient_email}: {subject}",
                action_type='automation'
            )
            
            print(f"✅ Real email sent to {recipient_email}: {subject}")
            
            return {
                'success': True,
                'timestamp': timestamp,
                'recipient': recipient_email,
                'subject': subject,
                'method': 'real_smtp'
            }
            
        except Exception as e:
            error_msg = f"Failed to send email to {recipient_email}: {str(e)}"
            self.logger.log_error(error_msg, 'System')
            print(f"❌ {error_msg}")
            raise
    
    def notify_status_change(self, request_data, old_status, new_status):
        """Send notification when request status changes"""
        patient_email = request_data.get('contact_info', '')
        request_id = request_data.get('request_id', '')
        patient_name = request_data.get('patient_name', 'Patient')
        
        # Determine notification type based on status
        if new_status == 'In Progress':
            subject = f"Request {request_id} - Case Assigned and In Progress"
            body = f"""
Dear {patient_name},

Your medical assistance request (ID: {request_id}) has been assigned to our team and is now in progress.

Our team will be coordinating your {request_data.get('request_type', 'request')} and will keep you updated on the progress.

If you have any questions, please contact us at ops@ulinkassist.com or +65 6835 0388.

Best regards,
Ulink Assist Team
"""
        elif new_status == 'Completed':
            subject = f"Request {request_id} - Case Completed"
            body = f"""
Dear {patient_name},

Your medical assistance request (ID: {request_id}) has been completed.

We hope that we have provided you with excellent service. If you need any further assistance, please don't hesitate to contact us.

Thank you for choosing Ulink Assist.

Best regards,
Ulink Assist Team
"""
        else:
            subject = f"Request {request_id} - Status Updated to {new_status}"
            body = f"""
Dear {patient_name},

The status of your medical assistance request (ID: {request_id}) has been updated to: {new_status}

We will continue to keep you informed of any developments.

Best regards,
Ulink Assist Team
"""
        
        # Only send if email is provided
        if '@' in patient_email:
            return self.send_notification(patient_email, subject, body, request_id)
        else:
            # Log that notification would be sent but no email provided
            self.logger.log_activity(
                f"Status change notification prepared for {request_id} but no email address provided",
                action_type='automation'
            )
            return {'success': False, 'reason': 'No email address provided'}
    
    def notify_new_request(self, request_data):
        """Send notification when a new request is created"""
        patient_email = request_data.get('contact_info', '')
        request_id = request_data.get('request_id', '')
        patient_name = request_data.get('patient_name', 'Patient')
        request_type = request_data.get('request_type', 'request')
        
        subject = f"Request {request_id} - Confirmation of Your Medical Assistance Request"
        body = f"""
Dear {patient_name},

Thank you for contacting Ulink Assist. We have received your {request_type} request (ID: {request_id}).

Your request has been logged and assigned a unique reference number. Our team will review your request and get back to you shortly.

Request Details:
- Request ID: {request_id}
- Request Type: {request_type}
- Priority: {request_data.get('priority', 'Medium')}
- Status: New

We will keep you updated on the progress of your request. If you have any urgent questions, please contact us at ops@ulinkassist.com or +65 6835 0388.

Best regards,
Ulink Assist Team

With 25+ years of experience, Ulink Assist is the medical assistance provider of choice.
"""
        
        # Only send if email is provided
        if '@' in patient_email:
            return self.send_notification(patient_email, subject, body, request_id)
        else:
            # Log that notification would be sent but no email provided
            self.logger.log_activity(
                f"New request notification prepared for {request_id} but no email address provided",
                action_type='automation'
            )
            return {'success': False, 'reason': 'No email address provided'}

