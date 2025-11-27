"""
Main Routes Module
Handles dashboard, request creation, and detail views
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from services.database_service import DatabaseService
from services.logging_service import LoggingService
from security.input_sanitizer import InputSanitizer
from automation.email_notification import EmailNotificationService
from automation.ai_triage import AITriageService
from automation.text_summarization import TextSummarizationService
from automation.sop_generator import SOPGeneratorService
from datetime import datetime
from translations import get_translation, get_all_translations
from config import Config

main_bp = Blueprint('main', __name__)

db_service = DatabaseService()
logger = LoggingService()
email_service = EmailNotificationService()
triage_service = AITriageService()
summarization_service = TextSummarizationService()
sop_service = SOPGeneratorService()

def get_language():
    """Get current language from session"""
    return session.get('language', 'en')

def generate_request_id():
    """Generate a unique request ID"""
    today = datetime.now().strftime('%Y%m%d')
    requests = db_service.load_requests()
    
    today_requests = [r for r in requests if r.get('request_id', '').startswith(f'REQ-{today}')]
    if today_requests:
        last_id = max([int(r['request_id'].split('-')[-1]) for r in today_requests if r['request_id'].split('-')[-1].isdigit()], default=0)
        next_num = last_id + 1
    else:
        next_num = 1
    
    return f"REQ-{today}-{next_num:03d}"

@main_bp.route('/')
def index():
    """Dashboard - Display all requests"""
    lang = get_language()
    t = get_all_translations(lang)
    
    requests = db_service.load_requests()
    requests.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Get filter and search parameters
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '').lower()
    priority_filter = request.args.get('priority', 'all')
    type_filter = request.args.get('type', 'all')
    
    # Apply filters
    if status_filter != 'all':
        requests = [r for r in requests if r.get('status', '').lower() == status_filter.lower()]
    
    if priority_filter != 'all':
        requests = [r for r in requests if r.get('priority', '').lower() == priority_filter.lower()]
    
    if type_filter != 'all':
        requests = [r for r in requests if r.get('request_type', '').lower() == type_filter.lower()]
    
    if search_query:
        requests = [r for r in requests if 
                   search_query in r.get('patient_name', '').lower() or
                   search_query in r.get('request_id', '').lower() or
                   search_query in r.get('description', '').lower()]
    
    # Count requests by status for statistics
    all_requests = db_service.load_requests()
    status_counts = {}
    priority_counts = {}
    type_counts = {}
    
    for req in all_requests:
        status = req.get('status', 'Unknown')
        priority = req.get('priority', 'Unknown')
        req_type = req.get('request_type', 'Unknown')
        
        status_counts[status] = status_counts.get(status, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        type_counts[req_type] = type_counts.get(req_type, 0) + 1
    
    return render_template('dashboard.html', 
                         requests=requests, 
                         status_filter=status_filter,
                         priority_filter=priority_filter,
                         type_filter=type_filter,
                         search_query=search_query,
                         status_counts=status_counts,
                         priority_counts=priority_counts,
                         type_counts=type_counts,
                         translations=t,
                         lang=lang)

@main_bp.route('/new', methods=['GET', 'POST'])
def new_request():
    """Create a new patient assistance request"""
    lang = get_language()
    t = get_all_translations(lang)
    
    if request.method == 'POST':
        # Get and sanitize form data
        patient_name = InputSanitizer.sanitize_string(request.form.get('patient_name', '').strip(), max_length=200)
        contact_info = request.form.get('contact_info', '').strip()
        request_type = InputSanitizer.validate_request_type(request.form.get('request_type', '').strip())
        priority = InputSanitizer.validate_priority(request.form.get('priority', 'Medium'))
        description = InputSanitizer.sanitize_text_area(request.form.get('description', '').strip())
        
        # Validate email or phone
        if '@' in contact_info:
            contact_info = InputSanitizer.sanitize_email(contact_info)
        else:
            contact_info = InputSanitizer.sanitize_phone(contact_info)
        
        # Validation
        if not all([patient_name, contact_info, request_type, description]):
            return render_template('new_request.html', 
                                 error='All fields are required. Please fill in all information.',
                                 translations=t,
                                 lang=lang)
        
        # Create new request
        request_id = generate_request_id()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        new_request = {
            'request_id': request_id,
            'patient_name': patient_name,
            'contact_info': contact_info,
            'request_type': request_type,
            'priority': priority,
            'description': description,
            'status': 'New',
            'timestamp': timestamp,
            'status_history': [{'status': 'New', 'timestamp': timestamp, 'note': 'Request created', 'user': session.get('username', 'System')}]
        }
        
        # Run AI Triage analysis
        triage_analysis = triage_service.analyze_request(new_request)
        new_request['ai_triage'] = triage_analysis
        new_request['recommended_priority'] = triage_analysis.get('recommended_priority', priority)
        
        # Generate text summary
        summary = summarization_service.summarize(description, max_sentences=2)
        new_request['description_summary'] = summary
        
        # Save to database first
        requests = db_service.load_requests()
        requests.append(new_request)
        db_service.save_requests(requests)
        
        # Send email notification for new request
        email_sent = False
        email_timestamp = None
        if Config.EMAIL_NOTIFICATIONS_ENABLED:
            email_result = email_service.notify_new_request(new_request)
            if email_result.get('success'):
                email_sent = True
                email_timestamp = email_result.get('timestamp')
                # Update request with email status
                new_request['email_sent'] = True
                new_request['email_timestamp'] = email_timestamp
                # Save again with email status
                requests = db_service.load_requests()
                for i, r in enumerate(requests):
                    if r.get('request_id') == request_id:
                        requests[i] = new_request
                        break
                db_service.save_requests(requests)
        
        # Log activity
        logger.log_activity(
            f"New request created: {request_id} - Patient: {patient_name} - Type: {request_type}",
            user=session.get('username', 'System')
        )
        
        # Flash message if email was sent
        if email_sent:
            from flask import flash
            flash(f'Request created successfully! Confirmation email sent to {contact_info}', 'success')
        else:
            from flask import flash
            if '@' not in contact_info:
                flash('Request created successfully! Note: No email sent - please provide an email address for notifications.', 'info')
            else:
                flash('Request created successfully!', 'success')
        
        return redirect(url_for('main.request_detail', request_id=request_id))
    
    return render_template('new_request.html', translations=t, lang=lang)

@main_bp.route('/request/<request_id>')
def request_detail(request_id):
    """Display details of a specific request"""
    lang = get_language()
    t = get_all_translations(lang)
    
    # Sanitize request ID
    request_id = InputSanitizer.sanitize_request_id(request_id)
    
    request_data = db_service.get_request_by_id(request_id)
    
    if not request_data:
        return redirect(url_for('main.index'))
    
    # Get AI triage if not already done
    if 'ai_triage' not in request_data:
        triage_analysis = triage_service.analyze_request(request_data)
        request_data['ai_triage'] = triage_analysis
    
    # Get SOP
    sop_data = sop_service.generate_sop(request_data.get('request_type'), request_id)
    
    return render_template('request_detail.html', 
                         request_data=request_data,
                         sop_data=sop_data,
                         translations=t,
                         lang=lang)

@main_bp.route('/request/<request_id>/update-status', methods=['POST'])
def update_status(request_id):
    """Update the status of a request"""
    # Sanitize request ID
    request_id = InputSanitizer.sanitize_request_id(request_id)
    
    request_data = db_service.get_request_by_id(request_id)
    
    if not request_data:
        return redirect(url_for('main.index'))
    
    new_status = InputSanitizer.validate_status(request.form.get('status', '').strip())
    note = InputSanitizer.sanitize_text_area(request.form.get('note', '').strip(), max_length=500)
    
    if not new_status:
        return redirect(url_for('main.request_detail', request_id=request_id))
    
    old_status = request_data.get('status', 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = session.get('username', 'System')
    
    # Update status
    request_data['status'] = new_status
    
    # Add to status history
    if 'status_history' not in request_data:
        request_data['status_history'] = []
    
    history_entry = {
        'status': new_status,
        'timestamp': timestamp,
        'note': note if note else f'Status changed from {old_status} to {new_status}',
        'user': user
    }
    request_data['status_history'].append(history_entry)
    
    # Save to database
    requests = db_service.load_requests()
    for i, r in enumerate(requests):
        if r.get('request_id') == request_id:
            requests[i] = request_data
            break
    
    db_service.save_requests(requests)
    
    # Trigger automation: Email notification
    if old_status != new_status and Config.EMAIL_NOTIFICATIONS_ENABLED:
        email_result = email_service.notify_status_change(request_data, old_status, new_status)
        if email_result.get('success'):
            request_data['email_sent'] = True
            request_data['email_timestamp'] = email_result.get('timestamp')
            # Update in database
            requests = db_service.load_requests()
            for i, r in enumerate(requests):
                if r.get('request_id') == request_id:
                    requests[i] = request_data
                    break
            db_service.save_requests(requests)
            
            # Flash message
            from flask import flash
            flash(f'Status updated! Email notification sent to {request_data.get("contact_info", "patient")}', 'success')
        else:
            from flask import flash
            if '@' not in request_data.get('contact_info', ''):
                flash('Status updated! Note: No email sent - patient contact info is not an email address.', 'info')
            else:
                flash('Status updated successfully!', 'success')
    
    # Log activity
    logger.log_activity(
        f"Request {request_id} status updated: {old_status} → {new_status} - Patient: {request_data.get('patient_name')}",
        user=user
    )
    
    return redirect(url_for('main.request_detail', request_id=request_id))

@main_bp.route('/api/stats')
def api_stats():
    """API endpoint for statistics (used by charts)"""
    requests = db_service.load_requests()
    status_counts = {}
    type_counts = {}
    priority_counts = {}
    
    for req in requests:
        status = req.get('status', 'Unknown')
        req_type = req.get('request_type', 'Unknown')
        priority = req.get('priority', 'Unknown')
        
        status_counts[status] = status_counts.get(status, 0) + 1
        type_counts[req_type] = type_counts.get(req_type, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    return jsonify({
        'status_counts': status_counts,
        'type_counts': type_counts,
        'priority_counts': priority_counts,
        'total': len(requests)
    })

@main_bp.route('/api/sop/<request_id>')
def download_sop(request_id):
    """Download SOP as text file"""
    request_id = InputSanitizer.sanitize_request_id(request_id)
    request_data = db_service.get_request_by_id(request_id)
    
    if not request_data:
        return jsonify({'error': 'Request not found'}), 404
    
    sop_data = sop_service.generate_sop(request_data.get('request_type'), request_id)
    sop_text = sop_service.format_sop_as_text(sop_data)
    
    from flask import Response
    return Response(
        sop_text,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename=sop_{request_id}.txt'}
    )

@main_bp.route('/set-language/<lang>')
def set_language(lang):
    """Set language preference"""
    if lang in ['en', 'id']:
        session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

