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

### 3. Results Management
- Stores test results with timestamps
- View detailed results and analysis
- Track performance over multiple tests

## Requirements

- Python 3.8 or higher
- Streamlit 1.28.0 or higher
- Plotly 5.15.0 or higher
- Pandas 1.5.0 or higher
- NumPy 1.24.0 or higher

## Installation

### Using uv (Recommended):
```bash
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

## How to Use

### Starting the Application
Run the script and you'll see the main menu with options:
- Ishihara Plates Test
- Performance Tracker
- View Results
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

### Viewing Results
- Click "View Results" from the main menu
- See all previous test results with dates and details
- Results are stored during the session

## Test Interpretation

### Ishihara Test Results
- **Normal Colour Vision**: 80%+ correct answers
- **Mild Colour Vision Deficiency**: 40-79% correct answers
- **Significant Colour Vision Deficiency**: <40% correct answers


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
    └── results.py              # Results display and analysis
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

### Colour Generation
The application uses the `colorsys` module to generate realistic colour distributions for the tests, simulating the actual colour patterns used in professional colour vision tests.

## Contributing

Feel free to contribute improvements, bug fixes, or additional test types. Please ensure:
- Code follows Python PEP 8 guidelines
- New features include appropriate error handling
- GUI elements are intuitive and accessible

## License

This project is open source and available under the MIT License.

## Disclaimer

This software is provided for educational purposes only and should not be used as a medical diagnostic tool. Always consult with qualified healthcare professionals for medical concerns about colour vision.
