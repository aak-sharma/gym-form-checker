import mediapipe as mp
import cv2
import numpy as np


class PoseExtractor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        print("✅ PoseExtractor initialized")

    def extract_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        
        if results.pose_landmarks is None:
            return None
        
        if not results.pose_landmarks.landmark:
            return None
        
        landmarks = []
        h, w, _ = frame.shape
        
        for landmark in results.pose_landmarks.landmark:
            x_pixel = landmark.x * w
            y_pixel = landmark.y * h
            z_depth = landmark.z
            
            landmarks.append({
                'x': x_pixel,
                'y': y_pixel,
                'z': z_depth,
                'confidence': landmark.visibility
            })
        
        return landmarks
    
    def get_landmark_by_name(self, landmarks, name):
        landmark_names = {
            0: "NOSE",
            1: "LEFT_EYE",
            2: "RIGHT_EYE",
            3: "LEFT_EAR",
            4: "RIGHT_EAR",
            11: "LEFT_SHOULDER",
            12: "RIGHT_SHOULDER",
            13: "LEFT_ELBOW",
            14: "RIGHT_ELBOW",
            15: "LEFT_WRIST",
            16: "RIGHT_WRIST",
            23: "LEFT_HIP",
            24: "RIGHT_HIP",
            25: "LEFT_KNEE",
            26: "RIGHT_KNEE",
            27: "LEFT_ANKLE",
            28: "RIGHT_ANKLE",
        }
        
        idx = None
        for landmark_id, landmark_name in landmark_names.items():
            if landmark_name == name:
                idx = landmark_id
                break
        
        if idx is not None and idx < len(landmarks):
            return landmarks[idx]
        return None
    
    def draw_skeleton(self, frame, landmarks, highlight_joints=None):
        if landmarks is None:
            return frame
        
        h, w, _ = frame.shape
        
        connections = [
            (11, 13), (13, 15),
            (12, 14), (14, 16),
            (11, 12),
            (11, 23), (12, 24),
            (23, 25), (25, 27),
            (24, 26), (26, 28),
            (23, 24),
        ]
        
        for start_idx, end_idx in connections:
            if start_idx >= len(landmarks) or end_idx >= len(landmarks):
                continue
            
            start = landmarks[start_idx]
            end = landmarks[end_idx]
            
            start_pos = (int(start['x']), int(start['y']))
            end_pos = (int(end['x']), int(end['y']))
            
            cv2.line(frame, start_pos, end_pos, color=(0, 255, 0), thickness=2)
        
        for idx, landmark in enumerate(landmarks):
            x = int(landmark['x'])
            y = int(landmark['y'])
            
            if highlight_joints and idx in highlight_joints:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            
            cv2.circle(frame, (x, y), radius=5, color=color, thickness=-1)
        
        return frame


if __name__ == "__main__":
    print("\n" + "="*60)
    print("POSE EXTRACTOR TEST")
    print("="*60)
    print("Starting webcam...")
    print("Press 'q' to quit")
    print("="*60 + "\n")
    
    extractor = PoseExtractor()
    cap = cv2.VideoCapture(0)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Webcam: {width}x{height} @ {fps} FPS\n")
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        landmarks = extractor.extract_landmarks(frame)
        
        if landmarks:
            frame = extractor.draw_skeleton(frame, landmarks)
            avg_confidence = sum([lm['confidence'] for lm in landmarks]) / len(landmarks)
            cv2.putText(frame, f"Confidence: {avg_confidence:.1%}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            shoulder = extractor.get_landmark_by_name(landmarks, "LEFT_SHOULDER")
            if shoulder:
                cv2.putText(frame, f"Shoulder: ({shoulder['x']:.0f}, {shoulder['y']:.0f})", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        else:
            cv2.putText(frame, "No pose detected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.putText(frame, f"Frame: {frame_count}", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Pose Extractor Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n✅ Test completed!")
