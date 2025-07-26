import streamlit as st
import tempfile
import os
from video_utils import VideoProcessor
from captioning import FrameCaptioner
from summarizer import StorySummarizer
from feasibility import FeasibilityAnalyzer
from analyzer import ComprehensiveAnalyzer
import matplotlib.pyplot as plt
from PIL import Image

def main():
    st.set_page_config(
        page_title="Video Feasibility Checker",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Video Feasibility Checker")
    st.markdown("Upload a video or provide a YouTube link to analyze whether the events shown are realistically possible.")
    
    # Initialize components with better error handling
    @st.cache_resource
    def load_captioner():
        try:
            return FrameCaptioner()
        except Exception as e:
            st.error(f"Failed to load captioning model: {str(e)}")
            return None
    
    @st.cache_resource  
    def load_summarizer():
        try:
            return StorySummarizer()
        except Exception as e:
            st.error(f"Failed to load summarization model: {str(e)}")
            return None
    
    if 'video_processor' not in st.session_state:
        st.session_state.video_processor = VideoProcessor()
        
    if 'captioner' not in st.session_state:
        with st.spinner("Loading AI captioning model..."):
            st.session_state.captioner = load_captioner()
            
    if 'summarizer' not in st.session_state:
        with st.spinner("Loading summarization model..."):
            st.session_state.summarizer = load_summarizer()
            
    if 'feasibility_analyzer' not in st.session_state:
        st.session_state.feasibility_analyzer = FeasibilityAnalyzer()
        
    if 'comprehensive_analyzer' not in st.session_state:
        st.session_state.comprehensive_analyzer = ComprehensiveAnalyzer()
    
    # Input section
    st.header("📥 Input Video")
    
    # Add a test button for debugging
    if st.button("🧪 Test System (Debug)"):
        st.write("✅ Streamlit is working")
        st.write(f"✅ Video processor: {type(st.session_state.video_processor).__name__}")
        st.write(f"✅ Captioner: {type(st.session_state.captioner).__name__ if st.session_state.captioner else 'Failed'}")
        st.write(f"✅ Summarizer: {type(st.session_state.summarizer).__name__ if st.session_state.summarizer else 'Failed'}")
        st.write(f"✅ Feasibility analyzer: {type(st.session_state.feasibility_analyzer).__name__}")
        st.write(f"✅ Comprehensive analyzer: {type(st.session_state.comprehensive_analyzer).__name__}")
        
        # Test with a dummy frame
        import numpy as np
        dummy_frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        st.image(dummy_frame, caption="Test image generated", width=100)
        
        st.success("🎉 All systems operational!")
    
    st.divider()
    
    input_method = st.radio("Choose input method:", ["Upload Video File", "YouTube URL"])
    
    video_path = None
    
    if input_method == "Upload Video File":
        uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'mkv'])
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                video_path = tmp_file.name
    else:
        youtube_url = st.text_input("Enter YouTube URL:")
        
        # Add URL validation
        if youtube_url:
            st.write(f"🔗 URL entered: {youtube_url}")
            
            # Validate YouTube URL format
            valid_patterns = [
                'youtube.com/watch?v=',
                'youtu.be/',
                'm.youtube.com/watch?v=',
                'www.youtube.com/watch?v='
            ]
            
            is_valid = any(pattern in youtube_url.lower() for pattern in valid_patterns)
            
            if not is_valid:
                st.warning("⚠️ Please enter a valid YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)")
            else:
                st.success("✅ Valid YouTube URL format")
        
        if youtube_url and st.button("📥 Download Video", key="yt_download"):
            st.write("🚀 Download button clicked!")
            
            # Show the URL being processed
            st.info(f"Processing: {youtube_url}")
            
            with st.spinner("Downloading video..."):
                try:
                    # Add debug info
                    st.write("🔍 Starting download process...")
                    
                    video_path = st.session_state.video_processor.download_youtube_video(youtube_url)
                    
                    if video_path and os.path.exists(video_path):
                        st.success("✅ Video downloaded successfully!")
                        st.write(f"📁 File: {video_path}")
                        st.write(f"📊 Size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
                        
                        # Store in session state so it persists
                        st.session_state.downloaded_video_path = video_path
                        
                    else:
                        st.error("❌ Download failed - no file created")
                        video_path = None
                        
                except Exception as e:
                    st.error(f"❌ Download error: {str(e)}")
                    video_path = None
        
        # Check if we have a downloaded video in session state
        if 'downloaded_video_path' in st.session_state:
            if os.path.exists(st.session_state.downloaded_video_path):
                video_path = st.session_state.downloaded_video_path
                st.success(f"✅ Using downloaded video: {os.path.basename(video_path)}")
            else:
                # Clean up if file no longer exists
                del st.session_state.downloaded_video_path
    
    # Analysis section
    if video_path and st.button("🔍 Analyze Video"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Extract frames
            status_text.text("🎞️ Extracting frames...")
            progress_bar.progress(10)
            
            frames = st.session_state.video_processor.extract_frames(video_path)
            st.success(f"✅ Extracted {len(frames)} frames")
            progress_bar.progress(20)
            
            # Display sample frames
            if frames:
                st.header("🎞️ Sample Frames")
                cols = st.columns(min(5, len(frames)))
                for i, frame in enumerate(frames[:5]):
                    with cols[i]:
                        st.image(frame, caption=f"Frame {i+1}", use_column_width=True)
            
            # Step 2: Motion Analysis
            status_text.text("🏃 Analyzing motion patterns...")
            progress_bar.progress(30)
            
            try:
                motion_data = st.session_state.video_processor.calculate_optical_flow(video_path)
                
                st.header("🏃 Motion Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Frames", motion_data['total_frames'])
                with col2:
                    st.metric("Motion Anomalies", len(motion_data['anomalies']))
                with col3:
                    st.metric("Anomaly Ratio", f"{motion_data['anomaly_ratio']:.2%}")
                
                if motion_data['anomalies']:
                    st.warning("⚠️ Suspicious motion patterns detected!")
                    with st.expander("View Motion Anomalies"):
                        for anomaly in motion_data['anomalies'][:5]:
                            st.write(f"Frame {anomaly['frame']}: Mean motion = {anomaly['mean_motion']:.2f}")
                            
            except Exception as e:
                st.warning(f"Motion analysis failed: {str(e)}")
                motion_data = {'anomalies': [], 'total_frames': len(frames), 'anomaly_ratio': 0.0}
            
            progress_bar.progress(50)
            
            # Step 3: Frame Captioning
            status_text.text("📝 Generating frame captions...")
            
            try:
                captions = st.session_state.captioner.caption_frames(frames)
                
                st.header("📝 Frame Analysis")
                with st.expander("View All Frame Captions"):
                    for caption in captions:
                        st.write(caption)
                        
            except Exception as e:
                st.error(f"Frame captioning failed: {str(e)}")
                captions = [f"Frame {i+1}: Unable to generate caption" for i in range(len(frames))]
            
            progress_bar.progress(70)
            
            # Step 4: Story Summarization
            status_text.text("📚 Creating story summary...")
            
            try:
                story = st.session_state.summarizer.create_story_from_captions(captions)
                st.header("📚 Story Summary")
                st.info(story)
            except Exception as e:
                st.error(f"Story summarization failed: {str(e)}")
                story = " ".join(captions)  # Fallback to combined captions
            
            progress_bar.progress(80)
            
            # Step 5: Comprehensive Analysis
            status_text.text("🔬 Performing technical analysis...")
            
            try:
                tech_analysis = st.session_state.comprehensive_analyzer.analyze_video_authenticity(frames, motion_data)
                
                st.header("🔬 Technical Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Authenticity Score", f"{tech_analysis['authenticity_score']:.2f}")
                with col2:
                    st.metric("Assessment", tech_analysis['overall_assessment'])
                
                # Face analysis details
                face_data = tech_analysis['face_analysis']
                if face_data['total_faces_detected'] > 0:
                    st.write(f"**Faces Detected:** {face_data['total_faces_detected']}")
                    st.write(f"**Suspicious Faces:** {face_data['suspicious_faces']}")
                    if face_data['common_issues']:
                        st.write(f"**Common Issues:** {', '.join(face_data['common_issues'])}")
                        
            except Exception as e:
                st.error(f"Technical analysis failed: {str(e)}")
                tech_analysis = {
                    'authenticity_score': 0.5,
                    'overall_assessment': 'Analysis unavailable',
                    'face_analysis': {'total_faces_detected': 0, 'suspicious_faces': 0, 'common_issues': []}
                }
            
            progress_bar.progress(90)
            
            # Step 6: Feasibility Analysis with Gemini
            status_text.text("🎯 Analyzing feasibility with AI...")
            
            try:
                # Use enhanced analysis with frames if available
                feasibility_result = st.session_state.feasibility_analyzer.analyze_with_frames(
                    story, frames[:5], motion_data  # Pass first 5 frames for visual analysis
                )
                
                st.header("🎯 Feasibility Analysis")
                # Display verdict with appropriate styling
                verdict = feasibility_result['verdict']
                if "✅" in verdict:
                    st.success(f"**{verdict}**")
                elif "❌" in verdict:
                    st.error(f"**{verdict}**")
                else:
                    st.warning(f"**{verdict}**")
                
                st.write(f"**Explanation:** {feasibility_result['explanation']}")
                
                # Two-column analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Why This May Look Real")
                    st.write(feasibility_result['looks_real'])
                
                with col2:
                    st.subheader("❌ Why This May Be Fake")
                    st.write(feasibility_result['looks_fake'])
                    
            except Exception as e:
                st.error(f"Feasibility analysis failed: {str(e)}")
                feasibility_result = {
                    'verdict': '❓ Analysis Failed',
                    'explanation': f'Could not complete analysis: {str(e)}',
                    'looks_real': 'Analysis unavailable',
                    'looks_fake': 'Analysis unavailable'
                }
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Final Summary
            st.header("📊 Final Assessment")
            
            # Create summary metrics
            metrics = {
                'Feasibility': feasibility_result['verdict'],
                'Technical Authenticity': tech_analysis['overall_assessment'],
                'Motion Anomalies': f"{motion_data['anomaly_ratio']:.1%}",
                'Frames Analyzed': len(frames)
            }
            
            cols = st.columns(len(metrics))
            for i, (key, value) in enumerate(metrics.items()):
                with cols[i]:
                    st.metric(key, value)
            
            # Overall conclusion
            st.subheader("🏁 Conclusion")
            if "Not Feasible" in feasibility_result['verdict'] or tech_analysis['authenticity_score'] < 0.5:
                st.error("⚠️ This video likely contains unrealistic or manipulated content.")
            elif "Questionable" in feasibility_result['verdict'] or tech_analysis['authenticity_score'] < 0.7:
                st.warning("⚠️ This video contains questionable elements that warrant further investigation.")
            else:
                st.success("✅ This video appears to show realistic, feasible events.")
        
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.exception(e)
            
            # Show debug information
            with st.expander("🐛 Debug Information"):
                st.write(f"Video path: {video_path}")
                st.write(f"Video exists: {os.path.exists(video_path) if video_path else 'No path'}")
                if video_path and os.path.exists(video_path):
                    st.write(f"File size: {os.path.getsize(video_path)} bytes")
        
        finally:
            # Cleanup temporary files
            if video_path and os.path.exists(video_path):
                try:
                    os.unlink(video_path)
                except Exception as cleanup_error:
                    st.warning(f"Could not cleanup temporary file: {cleanup_error}")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
    
    # Instructions and Information
    with st.sidebar:
        st.header("ℹ️ How It Works")
        st.markdown("""
        1. **Upload** a video or provide YouTube URL
        2. **Extract** key frames every 2 seconds
        3. **Analyze** motion patterns for anomalies
        4. **Caption** each frame using AI
        5. **Summarize** into coherent story
        6. **Assess** technical authenticity
        7. **Evaluate** real-world feasibility
        """)
        
        st.header("🔧 Configuration")
        if st.button("🔄 Reset Models"):
            for key in ['captioner', 'summarizer', 'feasibility_analyzer', 'comprehensive_analyzer']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        st.header("⚙️ API Setup")
        st.markdown("""
        For best results, set your Gemini API key:
        - Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        - Add `GEMINI_API_KEY` to your environment
        - Or add it to Streamlit secrets
        
        **Advantages of Gemini:**
        - Free tier with generous limits
        - Excellent multimodal capabilities
        - Can analyze both text and images
        - Fast and accurate reasoning
        
        Without API key, fallback analysis will be used.
        """)

if __name__ == "__main__":
    main()