"""
Quick MediaPipe test
"""
print("Step 1: Import mediapipe...")
import mediapipe
print(f"✅ MediaPipe imported: {mediapipe.__version__}")

print("\nStep 2: Check if 'solutions' exists...")
print(f"Has solutions? {hasattr(mediapipe, 'solutions')}")

print("\nStep 3: Try to import solutions...")
try:
    from mediapipe import solutions
    print("✅ Solutions imported!")
    
    print("\nStep 4: Try to access pose...")
    pose = solutions.pose
    print("✅ Pose module found!")
    
except AttributeError as e:
    print(f"❌ Error: {e}")
    print("\nDEBUG INFO:")
    print(f"MediaPipe location: {mediapipe.__file__}")
    print(f"Available attributes: {dir(mediapipe)[:10]}...")