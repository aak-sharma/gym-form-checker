import numpy as np


class AngleCalculator:
    @staticmethod
    def calculate_angle(point_a, point_b, point_c):
        vector_ba = np.array([
            point_a['x'] - point_b['x'],
            point_a['y'] - point_b['y']
        ])
        
        vector_bc = np.array([
            point_c['x'] - point_b['x'],
            point_c['y'] - point_b['y']
        ])
        
        angle_ba = np.arctan2(vector_ba[1], vector_ba[0])
        angle_bc = np.arctan2(vector_bc[1], vector_bc[0])
        
        angle_rad = abs(angle_ba - angle_bc)
        angle_deg = np.degrees(angle_rad)
        
        if angle_deg > 180:
            angle_deg = 360 - angle_deg
        
        return angle_deg
    
    @staticmethod
    def get_multiple_angles(landmarks):
        angles = {}
        
        if len(landmarks) > 15:
            angles['left_elbow'] = AngleCalculator.calculate_angle(
                landmarks[11],
                landmarks[13],
                landmarks[15]
            )
        
        if len(landmarks) > 16:
            angles['right_elbow'] = AngleCalculator.calculate_angle(
                landmarks[12],
                landmarks[14],
                landmarks[16]
            )
        
        if len(landmarks) > 27:
            angles['left_knee'] = AngleCalculator.calculate_angle(
                landmarks[23],
                landmarks[25],
                landmarks[27]
            )
        
        if len(landmarks) > 28:
            angles['right_knee'] = AngleCalculator.calculate_angle(
                landmarks[24],
                landmarks[26],
                landmarks[28]
            )
        
        if len(landmarks) > 24:
            angles['left_hip'] = AngleCalculator.calculate_angle(
                landmarks[11],
                landmarks[23],
                landmarks[25]
            )
            
            angles['right_hip'] = AngleCalculator.calculate_angle(
                landmarks[12],
                landmarks[24],
                landmarks[26]
            )
        
        return angles


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ANGLE CALCULATOR TEST")
    print("="*70 + "\n")
    
    print("TEST 1: Right Angle (Should be ~90°)")
    print("-" * 70)
    point_a = {'x': 100, 'y': 50}
    point_b = {'x': 100, 'y': 100}
    point_c = {'x': 150, 'y': 100}
    angle = AngleCalculator.calculate_angle(point_a, point_b, point_c)
    print(f"Angle at B: {angle:.1f}°")
    print(f"Status: {'✅ PASS' if 89 < angle < 91 else '❌ FAIL'}\n")
    
    print("TEST 2: Acute Angle (Should be ~45°)")
    print("-" * 70)
    point_a = {'x': 100, 'y': 50}
    point_b = {'x': 100, 'y': 100}
    point_c = {'x': 171, 'y': 29}
    angle = AngleCalculator.calculate_angle(point_a, point_b, point_c)
    print(f"Angle at B: {angle:.1f}°")
    print(f"Status: {'✅ PASS' if 44 < angle < 46 else '❌ FAIL'}\n")
    
    print("TEST 3: Obtuse Angle (Should be ~135°)")
    print("-" * 70)
    point_a = {'x': 100, 'y': 50}
    point_b = {'x': 100, 'y': 100}
    point_c = {'x': 29, 'y': 29}
    angle = AngleCalculator.calculate_angle(point_a, point_b, point_c)
    print(f"Angle at B: {angle:.1f}°")
    print(f"Status: {'✅ PASS' if 134 < angle < 136 else '❌ FAIL'}\n")
    
    print("TEST 4: Real-World Push-Up Elbow Angle")
    print("-" * 70)
    shoulder = {'x': 200, 'y': 150}
    elbow = {'x': 250, 'y': 200}
    wrist = {'x': 300, 'y': 250}
    elbow_angle = AngleCalculator.calculate_angle(shoulder, elbow, wrist)
    print(f"Elbow Angle: {elbow_angle:.1f}°")
    print(f"Good push-up form: 60-90°")
    print(f"Status: {'✅ GOOD FORM' if 60 < elbow_angle < 90 else '⚠️ BAD FORM'}\n")
    
    print("="*70)
    print("All tests completed!")
    print("="*70 + "\n")
