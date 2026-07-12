# 🏋️ Gym Exercise Form Checker

An AI-powered real-time exercise form analyzer that uses MediaPipe pose detection to provide instant feedback on your workout technique.

## 🎯 Features

✅ **Real-time Pose Detection** - Detects 33 body joint positions using MediaPipe  
✅ **Joint Angle Analysis** - Calculates angles for elbows, knees, hips, and shoulders  
✅ **Form Feedback** - Provides real-time feedback on exercise correctness  
✅ **Multiple Exercises** - Supports 9 different exercises with custom form rules  
✅ **Video Processing** - Analyze uploaded videos or use live webcam  
✅ **Web UI** - User-friendly Streamlit interface  
✅ **Offline Processing** - All processing happens locally, no cloud dependency  

## 📋 Supported Exercises

- 🦵 **SQUAT** - Knee and hip angle analysis
- 💪 **PUSH_UP** - Elbow and body alignment
- 🏋️ **DEADLIFT** - Back angle and knee tracking
- 💯 **BICEP_CURL** - Full range of motion tracking
- 🔝 **SHOULDER_PRESS** - Shoulder and elbow extension
- 🌊 **PLANK** - Body alignment and hip level
- 🚶 **LUNGE** - Front/back knee and hip angles
- 🎯 **LATERAL_RAISE** - Arm elevation tracking
- 🏆 **BENCH_PRESS** - Elbow and bar path analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Windows/Mac/Linux
- Webcam (for live testing)
- Acer Nitro 5 or any decent laptop

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/gym-form-checker.git
   cd gym-form-checker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install mediapipe==0.10.21 opencv-python==4.8.0.76 numpy==1.26.4 streamlit fastapi uvicorn
   ```

### Usage

#### Option 1: Live Webcam Test
```bash
python test_pose_and_angles.py
```
- Shows skeleton in real-time
- Displays joint angles
- Provides form feedback
- Press 'q' to quit

#### Option 2: Process Video File
Edit `main.py` and uncomment:
```python
checker = GymFormChecker("SQUAT")
checker.process_video("your_video.mp4", "output.mp4")
```

Then run:
```bash
python main.py
```

#### Option 3: Streamlit Web UI
```bash
streamlit run app.py
```
- Opens at `http://localhost:8501`
- Upload videos
- Select exercises
- Download analyzed videos

## 📁 Project Structure

```
gym-form-checker/
├── pose_extractor.py       # Extracts 33 body landmarks from video
├── angle_calculator.py     # Calculates joint angles using trigonometry
├── form_analyzer.py        # Analyzes form against exercise-specific rules
├── main.py                 # Main application combining all components
├── app.py                  # Streamlit web interface
├── test_pose_and_angles.py # Live webcam test script
├── test_installation.py    # Verify all libraries installed
└── README.md               # This file
```

## 🏗️ Architecture

```
Video Input (Webcam/File)
    ↓
[MediaPipe Pose Detection]
    ↓
Extract 33 Joint Landmarks (x, y, z coordinates)
    ↓
[Angle Calculator - NumPy Trigonometry]
    ↓
Calculate Joint Angles (elbow, knee, hip, etc.)
    ↓
[Form Analyzer - Rule-Based System]
    ↓
Compare angles to exercise-specific guidelines
    ↓
Generate Feedback & Annotated Video Output
```

## 🧠 How It Works

### 1. Pose Extraction (MediaPipe)
- Detects 33 body landmarks in real-time
- Returns (x, y, z) coordinates for each joint
- Confidence scores for each detection

### 2. Angle Calculation (NumPy)
- Calculates angles between 3 joints using vector math
- Uses `arctan2` for accurate angle measurements
- Converts radians to degrees

### 3. Form Analysis (Rule-Based)
- Compares measured angles to exercise-specific ranges
- Flags angles outside acceptable range
- Provides specific improvement tips

### 4. Visualization (OpenCV)
- Draws skeleton on video frames
- Highlights problem joints in red
- Displays angle values in real-time

## 📊 Exercise Guidelines

### SQUAT
- Knees: 70-100°
- Keep chest up, weight in heels
- Full depth: hips below knees

### PUSH_UP
- Elbows: 60-90°
- Body in straight line
- Full range of motion

### DEADLIFT
- Knees: 60-110°
- Hips: 40-90°
- Neutral spine, hip hinge motion

### PLANK
- Hips: 160-180°
- Shoulders over wrists
- Body in straight line

## 🔧 Technologies Used

- **MediaPipe** (0.10.21) - Pose detection AI model
- **OpenCV** (4.8.0.76) - Video processing
- **NumPy** (1.26.4) - Mathematical calculations
- **Streamlit** (1.28+) - Web UI framework
- **Python** (3.10+) - Programming language

## 💡 Key Learning Points

This project teaches:
- ✅ AI/ML model integration (MediaPipe)
- ✅ Computer vision with OpenCV
- ✅ Vector mathematics and trigonometry (angles)
- ✅ Real-time video processing
- ✅ Python virtual environments & dependency management
- ✅ Web UI development (Streamlit)
- ✅ Cross-platform development (Windows/Mac/Linux)
- ✅ Git & GitHub workflow

## 🎓 Resume Skills Highlighted

- AI/Machine Learning Integration
- Computer Vision & Image Processing
- Real-time Data Processing
- Python Development
- Web Application Development
- Object-Oriented Programming
- Dependency Management
- Cross-Platform Software Development
- Problem Solving & Debugging

## ⚙️ Troubleshooting

### MediaPipe not found
```bash
pip install mediapipe==0.10.21
```

### Virtual environment not activating
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### OpenCV VideoCapture issues
```bash
pip install opencv-python==4.8.0.76
```

### Dependency conflicts
```bash
pip install mediapipe==0.10.21 opencv-python==4.8.0.76 numpy==1.26.4
```

## 🚀 Future Enhancements

- [ ] Mobile app support (React Native)
- [ ] Cloud deployment (AWS/Google Cloud)
- [ ] More exercises (30+ exercises)
- [ ] 3D visualization
- [ ] Training history & progress tracking
- [ ] Integration with fitness apps
- [ ] Real-time video streaming
- [ ] Performance metrics & analytics

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Aakriti Sharma**
- GitHub: [YourGitHubProfile](https://github.com/YourUsername)
- Email: your.email@example.com

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Fork the repository
- Create feature branches
- Submit pull requests
- Report bugs/issues

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Review the console error messages
3. Open an issue on GitHub
4. Check MediaPipe documentation

## 🎯 Performance

- **Inference Time**: ~30ms per frame (on CPU)
- **GPU Acceleration**: Faster with NVIDIA GPU
- **Memory Usage**: ~200-300MB
- **FPS**: 20-30 FPS on standard laptop

## 📚 Resources

- [MediaPipe Pose Documentation](https://google.github.io/mediapipe/solutions/pose)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [NumPy Documentation](https://numpy.org/doc/)

---

**Made with ❤️ for fitness enthusiasts 💪**

*Built with MediaPipe • OpenCV • Streamlit • Python*
