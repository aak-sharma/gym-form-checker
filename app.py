import streamlit as st
import cv2
import tempfile
import os
from main import GymFormChecker
from form_analyzer import FormAnalyzer

# Page configuration
st.set_page_config(
    page_title="Gym Form Checker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    /* Main header */
    .header {
        font-size: 4em;
        font-weight: bold;
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        margin-bottom: 10px;
    }
    
    /* Subheader */
    .subheader-text {
        font-size: 1.3em;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    
    /* Status badges */
    .status-good {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    
    .status-bad {
        background-color: #FF6B6B;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    
    /* Exercise card */
    .exercise-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #FF6B6B;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #FF6B6B, transparent);
        margin: 30px 0;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF5555, #FF7777);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">🏋️ Gym Exercise Form Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-text">AI-Powered Real-Time Exercise Form Analysis</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Exercise selection
    exercise = st.selectbox(
        "📌 Select Exercise",
        FormAnalyzer.get_available_exercises(),
        help="Choose the exercise you want to analyze"
    )
    
    # Input method
    input_method = st.radio(
        "📥 Input Method",
        ["📤 Upload Video", "🎥 Live Webcam"],
        help="Choose how to provide your workout video"
    )
    
    st.markdown("---")
    
    # Info section
    st.markdown("### 📊 About This App")
    st.markdown("""
    This AI-powered tool analyzes your exercise form using:
    - **MediaPipe Pose Detection** for joint tracking
    - **OpenCV** for video processing
    - **Custom Form Analysis Engine** for feedback
    
    Get real-time feedback on:
    - Joint angles
    - Body alignment
    - Range of motion
    - Form consistency
    """)

# Main content area
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

# Left column - Input
with col1:
    st.markdown(f"### 🎯 Analyzing: **{exercise}**")
    
    if input_method == "📤 Upload Video":
        uploaded_file = st.file_uploader(
            "📹 Choose a video file",
            type=["mp4", "mov", "avi", "flv"],
            help="Select a video of you performing the exercise"
        )
        
        if uploaded_file is not None:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            # Display video
            st.video(uploaded_file)
            
            st.info(f"✅ Video uploaded: {uploaded_file.name}")
            
            # Analyze button
            if st.button("🔍 Analyze Form", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("⏳ Processing video...")
                    progress_bar.progress(25)
                    
                    checker = GymFormChecker(exercise)
                    output_path = "analyzed_output.mp4"
                    
                    progress_bar.progress(50)
                    report = checker.process_video(tmp_path, output_path)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    
                    # Results section
                    st.markdown("---")
                    st.markdown("### 📈 Results")
                    
                    # Download button
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="📥 Download Analyzed Video",
                            data=f.read(),
                            file_name=f"{exercise.lower()}_analyzed.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    
                    # Report
                    if report:
                        st.markdown("#### 📋 Detailed Report")
                        st.text(report)
                    
                except Exception as e:
                    st.error(f"❌ Error processing video: {e}")
                
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
    
    else:  # Live Webcam
        st.info("📸 **Live Webcam Mode**")
        st.write("Click the button below to capture frames from your webcam")
        
        camera_photo = st.camera_input("📷 Capture frame")
        
        if camera_photo:
            st.success("✅ Photo captured!")
            st.write("💡 Tip: Real-time analysis coming soon!")

# Right column - Info & Tips
with col2:
    # How it works
    st.markdown("### 📖 How It Works")
    
    steps = {
        "1️⃣ Select": "Choose your exercise from the sidebar",
        "2️⃣ Upload": "Provide your workout video",
        "3️⃣ Analyze": "AI detects joints and measures angles",
        "4️⃣ Review": "Get detailed form feedback",
    }
    
    for step, desc in steps.items():
        st.markdown(f"**{step}** {desc}")
    
    st.markdown("---")
    
    # Exercise-specific tips
    st.markdown("### 🎯 Form Guidelines")
    
    exercise_tips = {
        "SQUAT": {
            "Knees": "70-100°",
            "Depth": "Hips below knees",
            "Chest": "Keep upright",
            "Feet": "Shoulder-width apart"
        },
        "PUSH_UP": {
            "Elbows": "60-90°",
            "Body": "Straight line",
            "Core": "Engaged throughout",
            "Hands": "Shoulder-width apart"
        },
        "DEADLIFT": {
            "Back": "Neutral spine",
            "Knees": "60-110°",
            "Hips": "Hip hinge motion",
            "Shoulders": "Over bar"
        },
        "BICEP_CURL": {
            "Elbows": "30-160° range",
            "Motion": "Full range of motion",
            "Upper Arms": "Keep still",
            "Wrists": "Straight alignment"
        },
        "SHOULDER_PRESS": {
            "Elbows": "Full extension at top",
            "Core": "Tight engagement",
            "Back": "No excessive arch",
            "Path": "Straight up"
        },
        "PLANK": {
            "Body": "Straight line",
            "Shoulders": "Over wrists",
            "Core": "Fully engaged",
            "Hips": "Level with shoulders"
        },
        "LUNGE": {
            "Front Knee": "90°",
            "Back Knee": "Almost touching ground",
            "Torso": "Upright",
            "Step": "Wide enough"
        },
        "LATERAL_RAISE": {
            "Arms": "Nearly straight",
            "Height": "Parallel to ground",
            "Shoulders": "Engaged",
            "Core": "Stable"
        },
        "BENCH_PRESS": {
            "Elbows": "60-100°",
            "Bar Path": "Controlled",
            "Chest": "Full contact",
            "Back": "Slight arch"
        }
    }
    
    if exercise in exercise_tips:
        tips = exercise_tips[exercise]
        for key, value in tips.items():
            st.markdown(f"• **{key}**: {value}")
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Quick Stats")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric("Exercises Available", len(FormAnalyzer.get_available_exercises()))
    
    with col_b:
        st.metric("Joint Angles Tracked", "33 Landmarks")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #999;">
    <p>Made for fitness enthusiasts 💪 | Powered by AI | Built with Python</p>
    <p style="font-size: 0.8em;">Using MediaPipe • OpenCV • Streamlit</p>
</div>
""", unsafe_allow_html=True)
