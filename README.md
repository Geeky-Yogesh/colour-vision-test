# Colour Vision Test

A Python application that implements colour vision tests to help detect colour vision deficiencies.

## Features

### 1. Ishihara Plates Test
- Simulates the classic Ishihara colour plate test
- Users identify numbers hidden within dot patterns
- Detects red-green colour blindness
- Provides detailed analysis of results

### 2. Performance Tracker
- Comprehensive analytics dashboard
- Progress monitoring over time
- Session comparison and trends
- Personalized recommendations
- Export capabilities for data analysis

### 3. Real-Time Webcam Distance Calibration
- Live camera feed with distance detection
- Real-time position monitoring during tests
- Color-coded distance indicators (Green/Orange/Yellow)
- Sidebar monitor for continuous distance tracking
- Automatic calibration for accurate measurements

### 4. Results Management
- Stores test results with timestamps
- View detailed results and analysis
- Track performance over multiple tests

## Requirements

- Python 3.8 or higher
- Streamlit 1.28.0 or higher
- Plotly 5.15.0 or higher
- Pandas 1.5.0 or higher
- NumPy 1.24.0 or higher
- OpenCV (cv2) for computer vision
- MediaPipe for face detection
- streamlit-webrtc for real-time video processing
- fpdf for PDF report generation
- tornado for webRTC support
- streamlit-sortables for UI components

## Installation

### Using uv (Recommended):
```bash
# Install dependencies and run the application
uv run streamlit run main.py
```

### Using pip:
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
streamlit run main.py
```

### Manual Installation:
If you encounter dependency issues, you can install packages manually:
```bash
pip install streamlit plotly pandas numpy opencv-python mediapipe fpdf streamlit-webrtc tornado streamlit-sortables
```

## How to Use

### Starting the Application
Run the script and you'll see the main menu with options:
- Ishihara Plates Test
- Performance Tracker
- View Results
- Webcam Distance Calibration
- Distance Settings

### Ishihara Plates Test
1. Click "Ishihara Plates Test"
2. Look at each colour plate
3. Type the number you see in the input box
4. Click "Next" or press Enter to proceed
5. Skip plates if you cannot see any number
6. View your results at the end

### Performance Tracker
1. Click "Performance Tracker" from main menu or sidebar
2. View comprehensive analytics across all test sessions
3. Monitor progress with interactive charts
4. Compare performance over time
5. Export data for external analysis

### Webcam Distance Calibration
1. Click "Webcam Test" from the sidebar
2. Click "Start" to enable your camera
3. Position yourself until the indicator turns **Green** (65-85cm range)
4. The system provides real-time feedback:
   - **Orange**: Too Close (< 65cm)
   - **Green**: Perfect Distance (65-85cm)
   - **Yellow**: Too Far (> 85cm)
5. Click "I am positioned correctly" to start the test
6. During Ishihara tests, a sidebar monitor ensures you maintain proper distance

### Viewing Results
- Click "View Results" from the main menu
- See all previous test results with dates and details
- Results are stored during the session

## Test Interpretation

### Ishihara Test Results
- **Normal Colour Vision**: 80%+ correct answers
- **Mild Colour Vision Deficiency**: 40-79% correct answers
- **Significant Colour Vision Deficiency**: <40% correct answers


## Troubleshooting

### Common Issues and Solutions

#### Build Errors
If you encounter build errors with hatchling, ensure the `pyproject.toml` file includes the correct build configuration:

```toml
[tool.hatch.build.targets.wheel]
packages = ["components"]
```

#### Missing Dependencies
If you see `ModuleNotFoundError` for any of the following packages:
- `fpdf`: Install with `pip install fpdf`
- `streamlit_webrtc`: Install with `pip install streamlit-webrtc`
- `tornado`: Install with `pip install tornado`
- `streamlit_sortables`: Install with `pip install streamlit-sortables`

#### PDF Generation Issues
If you encounter PDF generation errors, ensure you're using a compatible version of fpdf. The application has been tested with fpdf 1.7.2.

#### Webcam Access Issues
- Ensure your browser has camera permissions
- Check that no other applications are using the camera
- Try refreshing the page if webcam doesn't initialize

#### Performance Issues
- Close unnecessary browser tabs
- Ensure good lighting conditions for webcam distance detection
- Use a modern browser (Chrome, Firefox, Safari) for best performance

## Important Notes

- This application is for educational and screening purposes only
- It is not a substitute for professional medical diagnosis
- For accurate colour vision assessment, consult an eye care professional
- Test results may be affected by monitor settings and ambient lighting

## Technical Details

### File Structure
```
Colour-Vision/
├── main.py                     # Main application entry point
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── components/                 # Modular components
    ├── __init__.py             # Package initialization
    ├── config.py               # Page configuration and session state
    ├── colour_vision_test.py   # Core test logic
    ├── ui.py                   # Main menu and navigation
    ├── tests.py                # Test implementations
    ├── results.py              # Results display and analysis
    ├── webcam_live.py          # Real-time webcam distance calibration
    └── distance_guide.py       # Distance settings and calibration
```

### Key Components
- **main.py**: Application entry point and main logic
- **ColourVisionTest**: Core test algorithms and color generation
- **UI Components**: Streamlit-based interface elements
- **Test Components**: Ishihara test implementation
- **Results Component**: Data visualization and analysis

### Technology Stack
- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and visualizations
- **Pandas**: Data manipulation and analysis
- **OpenCV**: Computer vision and face detection
- **MediaPipe**: Advanced face landmark detection
- **streamlit-webrtc**: Real-time video streaming

### Colour Generation
The application uses the `colorsys` module to generate realistic colour distributions for the tests, simulating the actual colour patterns used in professional colour vision tests.

### Distance Detection Algorithm
The webcam component uses computer vision to estimate user distance:
- **Face Detection**: OpenCV Haar cascade classifier detects faces
- **Distance Calculation**: Uses the formula `Distance = (Known_Face_Width × Focal_Length) / Pixel_Width`
- **Real-time Processing**: Processes video frames at 30 FPS for smooth feedback
- **Calibration**: Focal length is calibrated for accurate distance measurements

## Contributing

Feel free to contribute improvements, bug fixes, or additional test types. Please ensure:
- Code follows Python PEP 8 guidelines
- New features include appropriate error handling
- GUI elements are intuitive and accessible

## License

This project is open source and available under the MIT License.

## Disclaimer

This software is provided for educational purposes only and should not be used as a medical diagnostic tool. Always consult with qualified healthcare professionals for medical concerns about colour vision.
