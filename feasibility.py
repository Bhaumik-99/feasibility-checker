import google.generativeai as genai
import os
from typing import Dict, Any
import streamlit as st
from PIL import Image
import numpy as np

class FeasibilityAnalyzer:
    def __init__(self):
        """Initialize feasibility analyzer with Gemini API"""
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            self.vision_model = None
    
    def analyze_feasibility(self, story: str, motion_data: dict = None, sample_frames: list = None) -> Dict[str, Any]:
        """Analyze if the story/scene is realistically feasible using Gemini"""
        
        prompt = f"""
        Analyze the following video scene description and determine if it's realistically possible in real life:

        Scene: "{story}"

        Motion Analysis Data: {motion_data if motion_data else "Not available"}

        Please provide your analysis in the following format:
        VERDICT: [Feasible/Not Feasible/Questionable]
        EXPLANATION: [Brief explanation of your reasoning]
        LOOKS_REAL: [Aspects that make this appear realistic or believable]
        LOOKS_FAKE: [Aspects that suggest this might be fake, CGI, or impossible]

        Consider physics laws, human capabilities, animal behavior, and real-world constraints in your analysis.
        """
        
        try:
            if self.model:
                # Use Gemini for text analysis
                response = self.model.generate_content(prompt)
                return self._parse_response(response.text)
            else:
                # Fallback analysis without API
                return self._fallback_analysis(story, motion_data)
                
        except Exception as e:
            st.warning(f"Gemini API error: {str(e)}. Using fallback analysis.")
            return self._fallback_analysis(story, motion_data)
    
    def analyze_with_frames(self, story: str, frames: list, motion_data: dict = None) -> Dict[str, Any]:
        """Enhanced analysis using both text and visual data with Gemini Vision"""
        
        if not self.vision_model or not frames:
            return self.analyze_feasibility(story, motion_data)
        
        try:
            # Select key frames for analysis (max 5 for API limits)
            selected_frames = frames[::max(1, len(frames)//5)][:5]
            
            # Convert frames to PIL Images
            pil_images = []
            for frame in selected_frames:
                if isinstance(frame, np.ndarray):
                    pil_image = Image.fromarray(frame)
                    pil_images.append(pil_image)
            
            prompt = f"""
            Analyze this video sequence for realistic feasibility. I'm providing both a text description and key frames.

            Text Description: "{story}"
            Motion Analysis: {motion_data if motion_data else "Not available"}

            Please examine the images and text together to determine:
            1. Are the events shown physically possible in real life?
            2. Do the visuals match the described events?
            3. Are there any inconsistencies in physics, lighting, or object behavior?
            4. Could this be achieved with practical effects, CGI, or special editing?

            Provide your analysis in this format:
            VERDICT: [Feasible/Not Feasible/Questionable]
            EXPLANATION: [Your detailed reasoning based on both visual and textual evidence]
            LOOKS_REAL: [Visual and contextual elements that support authenticity]
            LOOKS_FAKE: [Visual artifacts, impossibilities, or suspicious elements]
            """
            
            # Prepare content for multimodal analysis
            content = [prompt]
            content.extend(pil_images)
            
            response = self.vision_model.generate_content(content)
            return self._parse_response(response.text)
            
        except Exception as e:
            st.warning(f"Gemini Vision API error: {str(e)}. Falling back to text-only analysis.")
            return self.analyze_feasibility(story, motion_data)
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format"""
        lines = response_text.strip().split('\n')
        result = {
            'verdict': '❓ Unknown',
            'explanation': 'Analysis unavailable',
            'looks_real': 'No analysis available',
            'looks_fake': 'No analysis available'
        }
        
        for line in lines:
            if line.startswith('VERDICT:'):
                verdict = line.replace('VERDICT:', '').strip()
                if 'Not Feasible' in verdict:
                    result['verdict'] = '❌ Not Feasible'
                elif 'Feasible' in verdict:
                    result['verdict'] = '✅ Feasible'
                else:
                    result['verdict'] = '❓ Questionable'
            elif line.startswith('EXPLANATION:'):
                result['explanation'] = line.replace('EXPLANATION:', '').strip()
            elif line.startswith('LOOKS_REAL:'):
                result['looks_real'] = line.replace('LOOKS_REAL:', '').strip()
            elif line.startswith('LOOKS_FAKE:'):
                result['looks_fake'] = line.replace('LOOKS_FAKE:', '').strip()
        
        return result
    
    def _fallback_analysis(self, story: str, motion_data: dict = None) -> Dict[str, Any]:
        """Fallback analysis using simple heuristics"""
        story_lower = story.lower()
        
        # Simple keyword-based analysis
        impossible_keywords = ['fly', 'floating', 'teleport', 'magic', 'supernatural', 'dragon', 'unicorn']
        questionable_keywords = ['shark', 'tiger', 'explosion', 'fire', 'jump']
        
        impossible_count = sum(1 for word in impossible_keywords if word in story_lower)
        questionable_count = sum(1 for word in questionable_keywords if word in story_lower)
        
        # Motion analysis consideration
        motion_suspicious = False
        if motion_data and motion_data.get('anomaly_ratio', 0) > 0.3:
            motion_suspicious = True
        
        if impossible_count > 0 or motion_suspicious:
            verdict = '❌ Not Feasible'
            explanation = 'Contains elements that appear physically impossible or have suspicious motion patterns.'
        elif questionable_count > 1:
            verdict = '❓ Questionable'
            explanation = 'Contains elements that are unusual but potentially possible with special circumstances.'
        else:
            verdict = '✅ Feasible'
            explanation = 'Appears to show realistic, physically possible events.'
        
        return {
            'verdict': verdict,
            'explanation': explanation,
            'looks_real': 'Natural lighting, consistent physics, smooth camera movement.',
            'looks_fake': 'Unusual events, potential motion anomalies, or impossible scenarios.'
        }