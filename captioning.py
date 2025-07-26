import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import numpy as np
from typing import List

class FrameCaptioner:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        """Initialize BLIP model for image captioning"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)
    
    def caption_frame(self, frame: np.ndarray) -> str:
        """Generate caption for a single frame"""
        # Convert numpy array to PIL Image
        image = Image.fromarray(frame)
        
        # Process image
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        
        # Generate caption
        with torch.no_grad():
            out = self.model.generate(**inputs, max_length=50, num_beams=5)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
        
        return caption
    
    def caption_frames(self, frames: List[np.ndarray]) -> List[str]:
        """Generate captions for multiple frames"""
        captions = []
        for i, frame in enumerate(frames):
            try:
                caption = self.caption_frame(frame)
                captions.append(f"Frame {i+1}: {caption}")
            except Exception as e:
                captions.append(f"Frame {i+1}: Error generating caption - {str(e)}")
        
        return captions