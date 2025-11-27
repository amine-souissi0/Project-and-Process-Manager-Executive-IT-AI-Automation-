"""
Text Summarization Module
Uses NLP techniques to summarize long descriptions
"""

import re
from services.logging_service import LoggingService

class TextSummarizationService:
    """Service for summarizing long text descriptions"""
    
    def __init__(self):
        self.logger = LoggingService()
    
    def summarize(self, text, max_sentences=3):
        """
        Summarize text using extractive summarization
        
        Simple approach: Extract key sentences based on:
        - Sentence length
        - Keyword frequency
        - Position in text
        
        In production, this could use:
        - spaCy, NLTK for NLP
        - Transformers (BERT, GPT) for abstractive summarization
        - Cloud APIs (OpenAI, Google Cloud NLP)
        """
        if not text or len(text.strip()) < 50:
            return text
        
        # Clean and split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, i, len(sentences))
            scored_sentences.append((score, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(reverse=True)
        top_sentences = [s[1] for s in scored_sentences[:max_sentences]]
        
        # Reorder to maintain original order
        summary_sentences = []
        for sentence in sentences:
            if sentence in top_sentences:
                summary_sentences.append(sentence)
        
        summary = ' '.join(summary_sentences)
        
        # Log summarization
        self.logger.log_activity(
            f"Text summarized: {len(text)} chars -> {len(summary)} chars",
            action_type='automation'
        )
        
        return summary
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        # Simple sentence splitting (in production, use NLTK or spaCy)
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _score_sentence(self, sentence, position, total_sentences):
        """Score a sentence for importance"""
        score = 0
        
        # Prefer sentences at the beginning (often contain key info)
        if position < total_sentences * 0.3:
            score += 2
        
        # Prefer longer sentences (often more informative)
        if len(sentence) > 100:
            score += 1
        
        # Prefer sentences with numbers (often contain important details)
        if re.search(r'\d+', sentence):
            score += 1
        
        # Prefer sentences with question words (often indicate key concerns)
        question_words = ['what', 'when', 'where', 'who', 'why', 'how']
        if any(word in sentence.lower() for word in question_words):
            score += 1
        
        # Prefer sentences with medical/important keywords
        important_keywords = ['urgent', 'emergency', 'pain', 'surgery', 'doctor', 'hospital', 'medical']
        keyword_count = sum(1 for word in important_keywords if word in sentence.lower())
        score += keyword_count
        
        return score
    
    def extract_key_points(self, text, max_points=5):
        """Extract key points from text"""
        if not text:
            return []
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Score and rank sentences
        scored = [(self._score_sentence(s, i, len(sentences)), s) 
                 for i, s in enumerate(sentences)]
        scored.sort(reverse=True)
        
        # Extract top points
        key_points = [s[1] for s in scored[:max_points]]
        
        return key_points

