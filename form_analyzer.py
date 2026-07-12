class FormAnalyzer:
    EXERCISE_RULES = {
        'SQUAT': {
            'required_angles': {
                'left_knee': {'min': 70, 'max': 100, 'name': 'Left Knee'},
                'right_knee': {'min': 70, 'max': 100, 'name': 'Right Knee'},
            },
            'tips': {
                'left_knee': 'Keep knees at 90° angle. Avoid going too deep.',
                'right_knee': 'Knees should track over toes.',
            }
        },
        'PUSH_UP': {
            'required_angles': {
                'left_elbow': {'min': 60, 'max': 90, 'name': 'Left Elbow'},
                'right_elbow': {'min': 60, 'max': 90, 'name': 'Right Elbow'},
            },
            'tips': {
                'left_elbow': 'Lower until elbows are at ~90°. Keep body straight.',
                'right_elbow': 'Elbows close to body. Don\'t flare out too much.',
            }
        },
        'DEADLIFT': {
            'required_angles': {
                'left_knee': {'min': 60, 'max': 110, 'name': 'Left Knee'},
                'right_knee': {'min': 60, 'max': 110, 'name': 'Right Knee'},
                'left_hip': {'min': 40, 'max': 90, 'name': 'Left Hip'},
                'right_hip': {'min': 40, 'max': 90, 'name': 'Right Hip'},
            },
            'tips': {
                'left_knee': 'Keep knees slightly bent, don\'t lock.',
                'left_hip': 'Hip hinge: bend at hips, keep back straight.',
            }
        },
        'BICEP_CURL': {
            'required_angles': {
                'left_elbow': {'min': 30, 'max': 160, 'name': 'Left Elbow'},
                'right_elbow': {'min': 30, 'max': 160, 'name': 'Right Elbow'},
            },
            'tips': {
                'left_elbow': 'Full range of motion: straighten at bottom, curl at top.',
                'right_elbow': 'Keep elbow tucked to your side. Don\'t swing the weight.',
            }
        },
        'SHOULDER_PRESS': {
            'required_angles': {
                'left_elbow': {'min': 60, 'max': 180, 'name': 'Left Elbow'},
                'right_elbow': {'min': 60, 'max': 180, 'name': 'Right Elbow'},
            },
            'tips': {
                'left_elbow': 'Press straight up. Full extension at top.',
                'right_elbow': 'Avoid arching back. Keep core tight.',
            }
        },
        'PLANK': {
            'required_angles': {
                'left_hip': {'min': 160, 'max': 180, 'name': 'Left Hip'},
                'right_hip': {'min': 160, 'max': 180, 'name': 'Right Hip'},
            },
            'tips': {
                'left_hip': 'Keep body in straight line. Don\'t sag hips down.',
                'right_hip': 'Engage core. Shoulders over wrists.',
            }
        },
        'LUNGE': {
            'required_angles': {
                'left_knee': {'min': 70, 'max': 100, 'name': 'Left Knee'},
                'right_knee': {'min': 70, 'max': 100, 'name': 'Right Knee'},
                'left_hip': {'min': 70, 'max': 110, 'name': 'Left Hip'},
                'right_hip': {'min': 70, 'max': 110, 'name': 'Right Hip'},
            },
            'tips': {
                'left_knee': 'Front knee should be 90°. Back knee almost touching ground.',
                'right_knee': 'Keep knee tracking over ankle.',
                'left_hip': 'Torso upright. Don\'t lean forward.',
                'right_hip': 'Drop hips straight down.',
            }
        },
        'LATERAL_RAISE': {
            'required_angles': {
                'left_elbow': {'min': 160, 'max': 180, 'name': 'Left Elbow'},
                'right_elbow': {'min': 160, 'max': 180, 'name': 'Right Elbow'},
            },
            'tips': {
                'left_elbow': 'Keep arms nearly straight. Slight bend at elbow.',
                'right_elbow': 'Raise until arms parallel to ground.',
            }
        },
        'BENCH_PRESS': {
            'required_angles': {
                'left_elbow': {'min': 60, 'max': 100, 'name': 'Left Elbow'},
                'right_elbow': {'min': 60, 'max': 100, 'name': 'Right Elbow'},
            },
            'tips': {
                'left_elbow': 'Lower bar to chest level. Full extension at top.',
                'right_elbow': 'Elbows at 45° angle from body.',
            }
        },
    }
    
    @staticmethod
    def get_available_exercises():
        """Return list of available exercises"""
        return list(FormAnalyzer.EXERCISE_RULES.keys())
    
    @staticmethod
    def analyze_form(exercise_name, angles, confidence=0.8):
        if exercise_name not in FormAnalyzer.EXERCISE_RULES:
            return {'error': f'Exercise {exercise_name} not supported. Available: {FormAnalyzer.get_available_exercises()}'}
        
        rules = FormAnalyzer.EXERCISE_RULES[exercise_name]
        issues = []
        tips = []
        
        for angle_name, angle_value in angles.items():
            if angle_name not in rules['required_angles']:
                continue
            
            angle_rule = rules['required_angles'][angle_name]
            min_val = angle_rule['min']
            max_val = angle_rule['max']
            
            if angle_value < min_val:
                issues.append({
                    'joint': angle_rule['name'],
                    'actual': angle_value,
                    'expected_min': min_val,
                    'expected_max': max_val,
                    'severity': 'WARNING',
                    'message': f"{angle_rule['name']} angle too small: {angle_value:.1f}° (should be {min_val}-{max_val}°)"
                })
                tips.append(rules['tips'].get(angle_name, 'Adjust your form.'))
            
            elif angle_value > max_val:
                issues.append({
                    'joint': angle_rule['name'],
                    'actual': angle_value,
                    'expected_min': min_val,
                    'expected_max': max_val,
                    'severity': 'WARNING',
                    'message': f"{angle_rule['name']} angle too large: {angle_value:.1f}° (should be {min_val}-{max_val}°)"
                })
                tips.append(rules['tips'].get(angle_name, 'Adjust your form.'))
        
        return {
            'is_good_form': len(issues) == 0,
            'issues': issues,
            'tips': list(set(tips)),
            'exercise': exercise_name,
            'timestamp': None
        }
    
    @staticmethod
    def generate_report(analysis):
        report = f"\n{'='*50}\n"
        report += f"Exercise: {analysis['exercise']}\n"
        report += f"Form Status: {'✅ GOOD' if analysis['is_good_form'] else '⚠️ NEEDS CORRECTION'}\n"
        report += f"{'='*50}\n"
        
        if analysis['issues']:
            report += "\nIssues Found:\n"
            for i, issue in enumerate(analysis['issues'], 1):
                report += f"{i}. {issue['message']}\n"
        else:
            report += "\n✅ Form looks good!\n"
        
        if analysis['tips']:
            report += "\nSuggestions to Improve:\n"
            for i, tip in enumerate(analysis['tips'], 1):
                report += f"• {tip}\n"
        
        return report


if __name__ == "__main__":
    print("\n" + "="*50)
    print("FORM ANALYZER TEST - ALL EXERCISES")
    print("="*50 + "\n")
    
    print("Available exercises:")
    for ex in FormAnalyzer.get_available_exercises():
        print(f"  - {ex}")
    print()
    
    # Test BICEP_CURL
    print("TEST 1: BICEP_CURL - Good Form")
    print("-" * 50)
    angles = {
        'left_elbow': 45,   # Good (between 30-160)
        'right_elbow': 50
    }
    analysis = FormAnalyzer.analyze_form('BICEP_CURL', angles)
    print(FormAnalyzer.generate_report(analysis))
    
    # Test SHOULDER_PRESS - Bad Form
    print("TEST 2: SHOULDER_PRESS - Bad Form")
    print("-" * 50)
    angles = {
        'left_elbow': 30,   # Too low
        'right_elbow': 45
    }
    analysis = FormAnalyzer.analyze_form('SHOULDER_PRESS', angles)
    print(FormAnalyzer.generate_report(analysis))
    
    # Test PLANK - Good Form
    print("TEST 3: PLANK - Good Form")
    print("-" * 50)
    angles = {
        'left_hip': 170,    # Good (between 160-180)
        'right_hip': 172
    }
    analysis = FormAnalyzer.analyze_form('PLANK', angles)
    print(FormAnalyzer.generate_report(analysis))
    
    # Test LUNGE - Bad Form
    print("TEST 4: LUNGE - Bad Form")
    print("-" * 50)
    angles = {
        'left_knee': 120,   # Too high
        'right_knee': 85,
        'left_hip': 60,     # Too low
        'right_hip': 95
    }
    analysis = FormAnalyzer.analyze_form('LUNGE', angles)
    print(FormAnalyzer.generate_report(analysis))
