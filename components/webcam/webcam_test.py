"""
Main Webcam Test Module - Orchestrates webcam color vision testing
"""

import streamlit as st
from .webcam_capture import WebcamCapture
from .color_analysis import ColorAnalysis
from .webcam_ui import WebcamUI
from ..distance_guide import DistanceGuide

def webcam_test():
    """Main webcam color vision test"""
    st.title(" webcam Live Color Vision Test")
    st.markdown("---")
    
    # Initialize session state for webcam
    if 'webcam_active' not in st.session_state:
        st.session_state.webcam_active = False
    if 'captured_frame' not in st.session_state:
        st.session_state.captured_frame = None
    if 'color_analysis' not in st.session_state:
        st.session_state.color_analysis = None
    
    # Show sidebar controls
    test_mode = WebcamUI.show_sidebar_controls()
    
    # Show distance reminder for webcam testing
    DistanceGuide.show_distance_reminder("Webcam Color Test")
    
    # Main content area
    if st.session_state.webcam_active:
        # Create placeholder for video
        video_placeholder = st.empty()
        
        # Show test instructions
        WebcamUI.show_test_instructions(test_mode)
        
        # Try real webcam first, fallback to simulated
        try:
            WebcamCapture.display_real_webcam_feed(video_placeholder)
        except Exception as e:
            st.warning("Webcam not available. Using simulated feed.")
            WebcamCapture.display_simulated_feed(video_placeholder)
    else:
        st.info("Click 'Start Camera' to begin the webcam test.")
    
    # Display captured frame and analysis
    if st.session_state.captured_frame is not None:
        ColorAnalysis.display_analysis(test_mode)
    
    # Navigation buttons
    WebcamUI.show_navigation_buttons()
