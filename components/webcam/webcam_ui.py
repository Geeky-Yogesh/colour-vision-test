"""
Webcam UI Module - User interface components for webcam testing
"""

import streamlit as st
import cv2

class WebcamUI:
    """Handle UI components for webcam testing"""
    
    @staticmethod
    def add_color_vision_overlay(frame):
        """Add color vision testing overlays to webcam feed"""
        
        # Add color patches for testing
        h, w = frame.shape[:2]
        
        # Add red patch
        cv2.rectangle(frame, (50, 50), (150, 150), (0, 0, 255), -1)
        cv2.putText(frame, "RED", (70, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add green patch
        cv2.rectangle(frame, (w-150, 50), (w-50, 150), (0, 255, 0), -1)
        cv2.putText(frame, "GREEN", (w-140, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Add blue patch
        cv2.rectangle(frame, (50, h-150), (150, h-50), (255, 0, 0), -1)
        cv2.putText(frame, "BLUE", (65, h-90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add instructions
        cv2.putText(frame, "Color Vision Test - Identify the colors", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return frame
    
    @staticmethod
    def show_sidebar_controls():
        """Show sidebar controls for webcam testing"""
        
        with st.sidebar:
            st.subheader(" Controls")
            
            # Webcam toggle
            if st.button(" Start/Stop Camera", width='stretch'):
                st.session_state.webcam_active = not st.session_state.webcam_active
                if not st.session_state.webcam_active:
                    st.session_state.captured_frame = None
                    st.session_state.color_analysis = None
            
            # Test mode selection
            test_mode = st.selectbox(
                "Test Mode:",
                ["Color Recognition", "Color Matching", "Live Analysis"]
            )
            
            st.markdown("---")
            st.info("""
            **Instructions:**
            1. Start the camera
            2. Position yourself in good lighting
            3. Follow the on-screen prompts
            4. Capture images when requested
            """)
        
        return test_mode
    
    @staticmethod
    def show_test_instructions(test_mode):
        """Show instructions based on test mode"""
        
        if test_mode == "Color Recognition":
            st.subheader("Color Recognition Test")
            st.write("Look at the colored objects around you and identify their colors.")
            
            # Color challenge
            target_color = st.selectbox(
                "Find an object with this color:",
                ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
            )
            
            if st.button("I found it!"):
                from .webcam_capture import WebcamCapture
                WebcamCapture.capture_frame()
                
        elif test_mode == "Color Matching":
            st.subheader("Color Matching Test")
            st.write("Match the colors shown on screen with real objects.")
            
            # Display color patches
            col1, col2, col3 = st.columns(3)
            colors = ['#FF0000', '#00FF00', '#0000FF']
            
            with col1:
                st.color_picker("Match this Red", '#FF0000', disabled=True)
            with col2:
                st.color_picker("Match this Green", '#00FF00', disabled=True)
            with col3:
                st.color_picker("Match this Blue", '#0000FF', disabled=True)
            
            if st.button("Capture for Analysis"):
                from .webcam_capture import WebcamCapture
                WebcamCapture.capture_frame()
                
        elif test_mode == "Live Analysis":
            st.subheader("Live Color Analysis")
            st.write("Real-time color analysis of your environment.")
            
            if st.button("Analyze Current Frame"):
                from .webcam_capture import WebcamCapture
                WebcamCapture.capture_frame()
    
    @staticmethod
    def show_navigation_buttons():
        """Show navigation buttons at bottom"""
        
        col1, col2 = st.columns(2)
        if col1.button(" Back to Menu"):
            st.session_state.webcam_active = False
            st.session_state.captured_frame = None
            st.session_state.color_analysis = None
            st.session_state.current_test = None
            st.rerun()
