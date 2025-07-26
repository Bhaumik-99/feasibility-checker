from transformers import pipeline
from typing import List
import re

class StorySummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """Initialize summarization model"""
        self.summarizer = pipeline("summarization", model=model_name)
    
    def create_story_from_captions(self, captions: List[str]) -> str:
        """Convert frame captions into a coherent story"""
        # Combine all captions into a single text
        combined_text = " ".join(captions)
        
        # Clean up the text
        combined_text = re.sub(r'Frame \d+:', '', combined_text)
        combined_text = re.sub(r'\s+', ' ', combined_text).strip()
        
        # If text is too short, return as is
        if len(combined_text.split()) < 20:
            return combined_text
        
        try:
            # Summarize to create coherent narrative
            summary = self.summarizer(combined_text, 
                                    max_length=150, 
                                    min_length=30, 
                                    do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            # Fallback: return cleaned combined text
            return combined_text[:500] + "..." if len(combined_text) > 500 else combined_text