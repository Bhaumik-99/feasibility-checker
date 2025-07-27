## README.md
# 🎥 Video Feasibility Checker

A comprehensive Python application that analyzes videos to determine whether the events shown are realistically possible in real life.

## ✨ Features

- 📥 **Video Input**: Upload files or YouTube URLs  
- 🖼️ **Frame Extraction**: Extract key frames every 2 seconds  
- 🧠 **AI Captioning**: Generate natural language descriptions using BLIP  
- 📚 **Story Summarization**: Create coherent narratives using BART  
- 🎯 **Motion Analysis**: Detect anomalous motion patterns using optical flow  
- 🕵️‍♂️ **Deepfake Detection**: Basic face analysis for manipulation detection  
- ⚖️ **Feasibility Assessment**: AI-powered reasoning about real-world possibility  
- 🌐 **Web Interface**: User-friendly Streamlit application  

## ⚙️ Installation

1. 📂 **Clone the repository**
2. 📦 **Install dependencies**:
   ```bash
   pip install -r requirements.txt
```
3. Set up your Gemini API key (optional but recommended):
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
