"""
AI Triage Assistant Module
Provides intelligent suggestions based on request type and content
"""

import re
from services.logging_service import LoggingService

class AITriageService:
    """AI-powered triage and suggestion service"""
    
    def __init__(self):
        self.logger = LoggingService()
        
        # Keyword patterns for intelligent triage
        self.urgency_keywords = {
            'high': ['urgent', 'emergency', 'critical', 'immediate', 'asap', 'severe', 'acute'],
            'medium': ['soon', 'important', 'moderate', 'significant'],
            'low': ['routine', 'general', 'inquiry', 'question']
        }
        
        self.medical_keywords = {
            'pain': ['pain', 'ache', 'hurt', 'sore', 'discomfort'],
            'accident': ['accident', 'fall', 'injury', 'trauma', 'crash'],
            'surgery': ['surgery', 'operation', 'procedure', 'surgical'],
            'cancer': ['cancer', 'tumor', 'malignancy', 'oncology'],
            'cardiac': ['heart', 'cardiac', 'chest pain', 'angina', 'heart attack']
        }
    
    def analyze_request(self, request_data):
        """
        Analyze a request and provide intelligent suggestions
        
        Returns:
            dict with suggestions, priority recommendation, and next steps
        """
        request_type = request_data.get('request_type', '')
        description = request_data.get('description', '').lower()
        current_priority = request_data.get('priority', 'Medium')
        
        suggestions = []
        recommended_priority = current_priority
        next_steps = []
        workflow_suggestion = ""
        
        # Analyze request type
        if request_type == 'Medical Evacuation':
            recommended_priority = 'Urgent'
            workflow_suggestion = "High priority medical coordination workflow"
            next_steps = [
                "1. Immediate medical assessment",
                "2. Coordinate with medical team",
                "3. Arrange transportation",
                "4. Prepare medical documentation",
                "5. Coordinate with receiving hospital"
            ]
            suggestions.append("Medical evacuation requires immediate attention and coordination")
        
        elif request_type == 'Teleconsultation':
            workflow_suggestion = "Doctor assignment and scheduling workflow"
            next_steps = [
                "1. Review patient medical history",
                "2. Assign appropriate specialist",
                "3. Schedule consultation",
                "4. Send appointment confirmation",
                "5. Prepare consultation materials"
            ]
            suggestions.append("Teleconsultation can be scheduled within 24-48 hours")
        
        elif request_type == 'Hospital Booking':
            workflow_suggestion = "Hospital coordination and booking workflow"
            next_steps = [
                "1. Verify medical requirements",
                "2. Contact preferred hospital",
                "3. Check availability",
                "4. Coordinate with patient",
                "5. Confirm booking"
            ]
            suggestions.append("Hospital booking requires coordination with multiple parties")
        
        elif request_type == 'Case Inquiry':
            workflow_suggestion = "Information gathering and response workflow"
            next_steps = [
                "1. Review inquiry details",
                "2. Gather relevant information",
                "3. Prepare response",
                "4. Contact patient if needed",
                "5. Provide comprehensive answer"
            ]
        
        # Analyze description for urgency indicators
        description_lower = description.lower()
        urgency_score = 0
        
        for keyword in self.urgency_keywords['high']:
            if keyword in description_lower:
                urgency_score += 3
                suggestions.append(f"High urgency indicator detected: '{keyword}'")
        
        for keyword in self.urgency_keywords['medium']:
            if keyword in description_lower:
                urgency_score += 2
        
        # Analyze for medical keywords
        for category, keywords in self.medical_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    suggestions.append(f"Medical condition detected: {category}")
                    if category in ['accident', 'cardiac']:
                        urgency_score += 2
        
        # Adjust priority based on analysis
        if urgency_score >= 5:
            recommended_priority = 'Urgent'
        elif urgency_score >= 3:
            recommended_priority = 'High'
        elif urgency_score >= 1:
            recommended_priority = 'Medium'
        else:
            recommended_priority = 'Low'
        
        # Log AI analysis
        self.logger.log_activity(
            f"AI Triage analysis completed for request {request_data.get('request_id')}: "
            f"Recommended priority: {recommended_priority}",
            action_type='automation'
        )
        
        return {
            'recommended_priority': recommended_priority,
            'workflow_suggestion': workflow_suggestion,
            'next_steps': next_steps,
            'suggestions': suggestions,
            'urgency_score': urgency_score,
            'analysis_timestamp': self.logger.log_file  # Placeholder
        }
    
    def get_triage_summary(self, request_data):
        """Get a quick triage summary for display"""
        analysis = self.analyze_request(request_data)
        
        summary = {
            'priority': analysis['recommended_priority'],
            'workflow': analysis['workflow_suggestion'],
            'key_suggestions': analysis['suggestions'][:3]  # Top 3 suggestions
        }
        
        return summary

