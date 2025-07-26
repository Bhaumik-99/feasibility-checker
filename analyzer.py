import cv2
import numpy as np
from typing import Dict, List, Any
import torch
from torchvision import transforms
from PIL import Image

class DeepfakeDetector:
    def __init__(self):
        """Initialize deepfake detection components"""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_faces_in_frames(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Detect faces and analyze for potential deepfake indicators"""
        face_data = []
        
        for i, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            face_info = {
                'frame_idx': i,
                'face_count': len(faces),
                'faces': []
            }
            
            for (x, y, w, h) in faces:
                face_region = frame[y:y+h, x:x+w]
                
                # Simple heuristics for suspicious faces
                face_analysis = self._analyze_face_region(face_region)
                face_info['faces'].append({
                    'bbox': (x, y, w, h),
                    'analysis': face_analysis
                })
            
            face_data.append(face_info)
        
        return self._summarize_face_analysis(face_data)
    
    def _analyze_face_region(self, face_region: np.ndarray) -> Dict[str, Any]:
        """Analyze a face region for potential deepfake indicators"""
        if face_region.size == 0:
            return {'suspicious': False, 'reasons': []}
        
        # Convert to grayscale for analysis
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_RGB2GRAY)
        
        # Calculate various metrics
        blur_score = cv2.Laplacian(gray_face, cv2.CV_64F).var()
        
        # Simple texture analysis
        contrast = gray_face.std()
        brightness = gray_face.mean()
        
        suspicious_factors = []
        
        # Heuristic checks
        if blur_score < 100:
            suspicious_factors.append("Low detail/blur")
        if contrast < 20:
            suspicious_factors.append("Low contrast")
        if brightness < 50 or brightness > 200:
            suspicious_factors.append("Unusual brightness")
        
        return {
            'suspicious': len(suspicious_factors) > 1,
            'reasons': suspicious_factors,
            'metrics': {
                'blur_score': blur_score,
                'contrast': contrast,
                'brightness': brightness
            }
        }
    
    def _summarize_face_analysis(self, face_data: List[Dict]) -> Dict[str, Any]:
        """Summarize face analysis across all frames"""
        total_faces = sum(frame['face_count'] for frame in face_data)
        suspicious_faces = 0
        all_reasons = []
        
        for frame in face_data:
            for face in frame['faces']:
                if face['analysis']['suspicious']:
                    suspicious_faces += 1
                    all_reasons.extend(face['analysis']['reasons'])
        
        suspicious_ratio = suspicious_faces / max(total_faces, 1)
        
        return {
            'total_faces_detected': total_faces,
            'suspicious_faces': suspicious_faces,
            'suspicious_ratio': suspicious_ratio,
            'common_issues': list(set(all_reasons)),
            'likely_deepfake': suspicious_ratio > 0.5
        }

class ComprehensiveAnalyzer:
    def __init__(self):
        self.deepfake_detector = DeepfakeDetector()
    
    def analyze_video_authenticity(self, frames: List[np.ndarray], motion_data: dict) -> Dict[str, Any]:
        """Comprehensive analysis combining multiple detection methods"""
        
        # Face/deepfake analysis
        face_analysis = self.deepfake_detector.detect_faces_in_frames(frames)
        
        # Motion analysis summary
        motion_suspicious = motion_data.get('anomaly_ratio', 0) > 0.2
        
        # Overall assessment
        authenticity_score = 1.0
        
        # Reduce score based on findings
        if face_analysis['likely_deepfake']:
            authenticity_score -= 0.4
        if motion_suspicious:
            authenticity_score -= 0.3
        if face_analysis['suspicious_ratio'] > 0.3:
            authenticity_score -= 0.2
        
        authenticity_score = max(0, authenticity_score)
        
        return {
            'authenticity_score': authenticity_score,
            'motion_analysis': motion_data,
            'face_analysis': face_analysis,
            'overall_assessment': self._get_assessment(authenticity_score)
        }
    
    def _get_assessment(self, score: float) -> str:
        if score > 0.7:
            return "Likely authentic"
        elif score > 0.4:
            return "Questionable authenticity"
        else:
            return "Likely manipulated/fake"