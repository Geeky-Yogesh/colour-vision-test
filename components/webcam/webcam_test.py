"""
Main Webcam Test Module - Orchestrates webcam color vision and face tracking testing
"""

import streamlit as st
from .webcam_capture import WebcamCapture
from .color_analysis import ColorAnalysis
from .webcam_ui import WebcamUI
from ..distance_guide import DistanceGuide

def webcam_test():
    """Main webcam color vision and face tracking test"""
    st.title(" Webcam Live Testing")
    st.markdown("---")
    
    # Initialize session state for webcam
    if 'webcam_active' not in st.session_state:
        st.session_state.webcam_active = False
    if 'captured_frame' not in st.session_state:
        st.session_state.captured_frame = None
    if 'color_analysis' not in st.session_state:
        st.session_state.color_analysis = None
    if 'face_metrics' not in st.session_state:
        st.session_state.face_metrics = None
    if 'face_tracking_enabled' not in st.session_state:
        st.session_state.face_tracking_enabled = True
    if 'webcam_capture_instance' not in st.session_state:
        st.session_state.webcam_capture_instance = WebcamCapture()
    
    # Show sidebar controls
    test_mode = WebcamUI.show_sidebar_controls()
    
    # Show distance reminder for webcam testing
    DistanceGuide.show_distance_reminder("Webcam Test")
    
    # Main content area
    if st.session_state.webcam_active:
        # Create placeholder for video
        video_placeholder = st.empty()
        
        # Show test instructions
        WebcamUI.show_test_instructions(test_mode)
        
        # Get webcam capture instance
        webcam_capture = st.session_state.webcam_capture_instance
        
        # Try real webcam first, fallback to simulated
        try:
            webcam_capture.display_real_webcam_feed(
                video_placeholder, 
                enable_face_tracking=st.session_state.face_tracking_enabled
            )
        except Exception as e:
            st.warning("Webcam not available. Using simulated feed.")
            webcam_capture.display_simulated_feed(
                video_placeholder, 
                enable_face_tracking=st.session_state.face_tracking_enabled
            )
    else:
        st.info("Click 'Start Camera' to begin the webcam test.")
    
    # Display captured frame and analysis
    if st.session_state.captured_frame is not None:
        ColorAnalysis.display_analysis(test_mode)
    
    # Navigation buttons
    WebcamUI.show_navigation_buttons()
