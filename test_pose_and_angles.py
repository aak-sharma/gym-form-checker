from pose_extractor import PoseExtractor
from angle_calculator import AngleCalculator
from form_analyzer import FormAnalyzer
import cv2

print("\n" + "="*60)
print("POSE + ANGLES + FORM TEST (Live Webcam)")
print("="*60)
print("Shows: Skeleton + Joint Angles + Form Analysis")
print("Press 'q' to quit\n")

extractor = PoseExtractor()
cap = cv2.VideoCapture(0)

exercise = "SQUAT"  # Change this to test different exercises

"""
exercise = "BICEP_CURL"
exercise = "SHOULDER_PRESS"
exercise = "PLANK"
exercise = "LUNGE"
exercise = "LATERAL_RAISE"
exercise = "BENCH_PRESS"
exercise = "DEADLIFT"
exercise = "PUSH_UP"
"""


frame_count = 0


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    h, w, _ = frame.shape
    landmarks = extractor.extract_landmarks(frame)
    
    # Draw semi-transparent background for text
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (400, h), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
    
    if landmarks:
        angles = AngleCalculator.get_multiple_angles(landmarks)
        analysis = FormAnalyzer.analyze_form(exercise, angles)
        
        frame = extractor.draw_skeleton(frame, landmarks)
        
        # Title with exercise name
        cv2.putText(frame, f"Exercise: {exercise}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Status box
        status = "GOOD FORM" if analysis['is_good_form'] else "FORM ISSUES"
        status_color = (0, 255, 0) if analysis['is_good_form'] else (0, 0, 255)
        
        cv2.rectangle(frame, (10, 45), (390, 85), status_color, -1)
        cv2.putText(frame, status, (20, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
        # Divider line
        cv2.line(frame, (10, 95), (390, 95), (100, 100, 100), 1)
        
        # Angles display
        y_pos = 120
        cv2.putText(frame, "JOINT ANGLES:", (10, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)
        y_pos += 30
        
        for angle_name, angle_value in angles.items():
            text = f"{angle_name}: {angle_value:.0f}°"
            cv2.putText(frame, text, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2)
            y_pos += 28
        
        # Issues section
        if analysis['issues']:
            y_pos += 10
            cv2.putText(frame, "ISSUES FOUND:", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            y_pos += 28
            
            for issue in analysis['issues'][:2]:  # Show only 2 issues
                cv2.putText(frame, f"⚠ {issue['joint']}", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                y_pos += 22
        else:
            y_pos += 10
            cv2.putText(frame, "✓ NO ISSUES", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Frame counter at bottom
        cv2.putText(frame, f"Frame: {frame_count}", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        # FPS counter
        cv2.putText(frame, "Press 'q' to quit", (w - 250, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    else:
        cv2.rectangle(frame, (10, 45), (390, 150), (0, 0, 255), -1)
        cv2.putText(frame, "NO POSE DETECTED", (20, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    cv2.imshow(f"Gym Form Checker - {exercise}", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n✅ Test completed!")
