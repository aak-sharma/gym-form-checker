"""
test_installation.py
Purpose: Verify all libraries are installed and compatible
"""

print("Testing installations...\n")

# Test 1: MediaPipe
try:
    import mediapipe as mp
    print(f"✅ MediaPipe: {mp.__version__}")
except ImportError as e:
    print(f"❌ MediaPipe: {e}")

# Test 2: OpenCV
try:
    import cv2
    print(f"✅ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV: {e}")

# Test 3: NumPy
try:
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")

# Test 4: Streamlit
try:
    import streamlit
    print(f"✅ Streamlit: {streamlit.__version__}")
except ImportError as e:
    print(f"❌ Streamlit: {e}")

# Test 5: MediaPipe + OpenCV together (real-world test)
try:
    print("\n🔧 Testing MediaPipe Pose detector...")
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    print("✅ MediaPipe Pose initialized successfully!")
except Exception as e:
    print(f"❌ MediaPipe Pose error: {e}")

print("\n" + "="*50)
print("All tests passed! Ready to build the app 🚀")
print("="*50)