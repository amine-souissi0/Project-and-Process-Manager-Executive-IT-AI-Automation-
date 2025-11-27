"""
SOP (Standard Operating Procedure) Generator Module
Automatically generates SOP templates based on request type
"""

from datetime import datetime
from services.logging_service import LoggingService

class SOPGeneratorService:
    """Service for generating SOP templates"""
    
    def __init__(self):
        self.logger = LoggingService()
    
    def generate_sop(self, request_type, request_id=None):
        """
        Generate an SOP template based on request type
        
        Returns:
            dict with SOP structure including steps, documents, communication flow, timeline
        """
        sop_templates = {
            'Teleconsultation': {
                'title': 'Teleconsultation Request SOP',
                'description': 'Standard Operating Procedure for handling teleconsultation requests',
                'steps': [
                    '1. Receive and log teleconsultation request',
                    '2. Verify patient information and medical history',
                    '3. Identify appropriate specialist based on condition',
                    '4. Check specialist availability',
                    '5. Schedule consultation appointment',
                    '6. Send appointment confirmation to patient',
                    '7. Prepare consultation materials and medical records',
                    '8. Conduct teleconsultation',
                    '9. Document consultation notes',
                    '10. Follow up with patient and provide recommendations'
                ],
                'required_documents': [
                    'Patient identification',
                    'Medical history',
                    'Previous medical reports (if available)',
                    'Current medications list',
                    'Insurance information (if applicable)'
                ],
                'communication_flow': [
                    'Patient → Request Submission',
                    'Case Manager → Specialist Assignment',
                    'Case Manager → Appointment Scheduling',
                    'System → Confirmation Email/SMS',
                    'Specialist → Consultation',
                    'Case Manager → Follow-up Communication'
                ],
                'timeline': {
                    'initial_response': 'Within 2 hours',
                    'specialist_assignment': 'Within 4 hours',
                    'appointment_scheduling': 'Within 24-48 hours',
                    'consultation': 'As scheduled',
                    'follow_up': 'Within 24 hours post-consultation'
                },
                'stakeholders': [
                    'Patient',
                    'Case Manager',
                    'Medical Specialist',
                    'Administrative Staff'
                ]
            },
            'Hospital Booking': {
                'title': 'Hospital Booking Request SOP',
                'description': 'Standard Operating Procedure for hospital booking coordination',
                'steps': [
                    '1. Receive hospital booking request',
                    '2. Verify medical requirements and urgency',
                    '3. Identify suitable hospitals based on specialty',
                    '4. Contact hospital to check availability',
                    '5. Coordinate with patient on preferences',
                    '6. Confirm booking with hospital',
                    '7. Arrange pre-admission requirements',
                    '8. Send booking confirmation to patient',
                    '9. Coordinate logistics (transportation, accommodation if needed)',
                    '10. Follow up on admission and post-discharge'
                ],
                'required_documents': [
                    'Medical referral letter',
                    'Patient identification',
                    'Medical reports and test results',
                    'Insurance pre-authorization (if applicable)',
                    'Passport and visa (for international patients)'
                ],
                'communication_flow': [
                    'Patient → Booking Request',
                    'Case Manager → Hospital Coordination',
                    'Hospital → Availability Confirmation',
                    'Case Manager → Patient Consultation',
                    'Case Manager → Booking Confirmation',
                    'Hospital → Admission Process'
                ],
                'timeline': {
                    'initial_response': 'Within 4 hours',
                    'hospital_contact': 'Within 8 hours',
                    'availability_check': 'Within 24 hours',
                    'booking_confirmation': 'Within 48 hours',
                    'admission': 'As scheduled'
                },
                'stakeholders': [
                    'Patient',
                    'Case Manager',
                    'Hospital Administration',
                    'Medical Team',
                    'Insurance Provider (if applicable)'
                ]
            },
            'Medical Evacuation': {
                'title': 'Medical Evacuation Request SOP',
                'description': 'Standard Operating Procedure for emergency medical evacuation',
                'steps': [
                    '1. Receive emergency evacuation request',
                    '2. Immediate medical assessment and triage',
                    '3. Coordinate with medical team for patient condition evaluation',
                    '4. Identify receiving hospital and medical facility',
                    '5. Arrange medical transport (air ambulance if needed)',
                    '6. Prepare all medical documentation',
                    '7. Coordinate with immigration and customs',
                    '8. Arrange ground transportation at destination',
                    '9. Ensure medical team escort if required',
                    '10. Monitor patient during transport',
                    '11. Handover to receiving facility',
                    '12. Post-evacuation follow-up'
                ],
                'required_documents': [
                    'Medical reports and diagnosis',
                    'Doctor\'s recommendation for evacuation',
                    'Patient identification and passport',
                    'Insurance coverage details',
                    'Emergency contact information',
                    'Medical power of attorney (if applicable)'
                ],
                'communication_flow': [
                    'Emergency Contact → Evacuation Request',
                    'Case Manager → Medical Team Assessment',
                    'Medical Team → Transport Arrangement',
                    'Case Manager → Receiving Hospital Coordination',
                    'Transport Team → Real-time Updates',
                    'Receiving Hospital → Handover Confirmation'
                ],
                'timeline': {
                    'initial_response': 'Immediate (within 30 minutes)',
                    'medical_assessment': 'Within 2 hours',
                    'transport_arrangement': 'Within 4-6 hours',
                    'evacuation_execution': 'As soon as medically safe',
                    'handover': 'Upon arrival at destination'
                },
                'stakeholders': [
                    'Patient/Family',
                    'Emergency Medical Team',
                    'Case Manager',
                    'Transport Provider',
                    'Receiving Hospital',
                    'Immigration Authorities'
                ]
            },
            'Case Inquiry': {
                'title': 'Case Inquiry Request SOP',
                'description': 'Standard Operating Procedure for handling case inquiries',
                'steps': [
                    '1. Receive case inquiry',
                    '2. Categorize inquiry type',
                    '3. Gather relevant information',
                    '4. Research and prepare response',
                    '5. Consult with medical team if needed',
                    '6. Prepare comprehensive answer',
                    '7. Send response to inquirer',
                    '8. Follow up if additional information needed',
                    '9. Document inquiry and response',
                    '10. Close inquiry'
                ],
                'required_documents': [
                    'Inquiry details',
                    'Patient information (if applicable)',
                    'Previous correspondence (if any)'
                ],
                'communication_flow': [
                    'Inquirer → Inquiry Submission',
                    'Case Manager → Information Gathering',
                    'Case Manager → Response Preparation',
                    'Case Manager → Response Delivery',
                    'Inquirer → Follow-up (if needed)'
                ],
                'timeline': {
                    'initial_response': 'Within 4 hours',
                    'information_gathering': 'Within 24 hours',
                    'response_delivery': 'Within 48 hours',
                    'follow_up': 'As needed'
                },
                'stakeholders': [
                    'Inquirer',
                    'Case Manager',
                    'Medical Team (if consultation needed)'
                ]
            }
        }
        
        # Get template or default
        template = sop_templates.get(request_type, {
            'title': f'{request_type} Request SOP',
            'description': f'Standard Operating Procedure for {request_type} requests',
            'steps': ['1. Receive request', '2. Process request', '3. Complete request'],
            'required_documents': ['Request details', 'Patient information'],
            'communication_flow': ['Request → Processing → Completion'],
            'timeline': {'initial_response': 'Within 24 hours'},
            'stakeholders': ['Patient', 'Case Manager']
        })
        
        # Add metadata
        template['generated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        template['request_id'] = request_id
        template['request_type'] = request_type
        
        # Log SOP generation
        self.logger.log_activity(
            f"SOP generated for request type: {request_type}",
            action_type='automation'
        )
        
        return template
    
    def format_sop_as_text(self, sop_data):
        """Format SOP data as readable text"""
        text = f"""
{'='*60}
{sop_data['title']}
{'='*60}

Description: {sop_data['description']}
Generated: {sop_data.get('generated_date', 'N/A')}
Request ID: {sop_data.get('request_id', 'N/A')}

PROCEDURE STEPS:
{chr(10).join(sop_data['steps'])}

REQUIRED DOCUMENTS:
{chr(10).join(f"• {doc}" for doc in sop_data['required_documents'])}

COMMUNICATION FLOW:
{chr(10).join(f"→ {flow}" for flow in sop_data['communication_flow'])}

TIMELINE:
"""
        for key, value in sop_data.get('timeline', {}).items():
            text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        text += f"\nSTAKEHOLDERS:\n"
        text += chr(10).join(f"• {stakeholder}" for stakeholder in sop_data.get('stakeholders', []))
        text += f"\n\n{'='*60}\n"
        
        return text

