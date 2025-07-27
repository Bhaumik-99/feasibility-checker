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

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```
Then:
1. 📤 Upload a video file or enter a YouTube URL  
2. ▶️ Click "Analyze Video" to start the analysis  
3. 📊 Review the comprehensive feasibility report  

## 🗂️ Project Structure

- `app.py` – 🎛️ Main Streamlit web interface  
- .streamlit/secrets.toml - API keys
- `video_utils.py` – 🎞️ Video processing and frame extraction  
- `captioning.py` – 🧠 AI-powered frame captioning using BLIP  
- `summarizer.py` – ✍️ Story generation using BART  
- `feasibility.py` – ⚖️ LLM-based feasibility analysis  
- `analyzer.py` – 🕵️ Motion analysis and deepfake detection  
- `requirements.txt` – 📦 Python dependencies  

## 🧰 Technologies Used

- 🖼️ **Computer Vision**: OpenCV, optical flow analysis  
- 🤖 **AI Models**: BLIP (captioning), BART (summarization), Gemini (reasoning & vision)  
- 🌐 **Web Interface**: Streamlit  
- 📹 **Video Processing**: yt-dlp for YouTube downloads  
- 🔬 **Deep Learning**: PyTorch, Transformers  
- 🧠 **Multimodal AI**: Google Gemini for text + image analysis  

## 🧪 Example Analysis

The system provides:  
- ✅/❌ Feasibility verdict with explanation  
- 📈 Technical authenticity score  
- 🚨 Motion anomaly detection  
- 🖼️ Frame-by-frame visual analysis  
- 🤔 "Why real" vs "Why fake" reasoning  

## ⚠️ Limitations

- 🌐 Requires good internet connection for model downloads  
- ⚡ GPU recommended for faster processing  
- 🔑 Gemini API key needed for best feasibility analysis *(free tier available)*  
- 🕒 Large videos may take significant time to process  
- 📉 Gemini has daily usage limits on free tier  

## 💎 Why Gemini?

- 🆓 **Free tier**: Generous free usage limits  
- 🔍 **Multimodal**: Can analyze both text and images simultaneously  
- ⚡ **Fast**: Quick response times for analysis  
- 🎯 **Accurate**: Excellent reasoning capabilities for feasibility assessment  
- 🛠️ **Easy setup**: Simple API key from Google AI Studio 
