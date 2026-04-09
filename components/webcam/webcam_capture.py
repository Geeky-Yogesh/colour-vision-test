"""
Webcam Capture Module - Handle real and simulated webcam feeds
"""

import cv2
import numpy as np
import streamlit as st

class WebcamCapture:
    """Handle webcam capture and display"""
    
    @staticmethod
    def display_real_webcam_feed(placeholder):
        """Display real webcam feed with color vision testing"""
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            placeholder.error("Unable to access webcam. Please check permissions.")
            return None
        
        # Capture frame
        ret, frame = cap.read()
        
        if ret:
            # Add color vision test overlay
            from .webcam_ui import WebcamUI
            frame = WebcamUI.add_color_vision_overlay(frame)
            
            # Convert to RGB for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display frame
            placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Store frame for capture
            st.session_state.current_frame = frame
            return frame
        
        cap.release()
        return None
    
    @staticmethod
    def display_simulated_feed(placeholder):
        """Display simulated webcam feed (fallback if webcam not available)"""
        
        # Create a simulated frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add some colored regions to simulate environment
        frame[100:200, 100:200] = [255, 0, 0]  # Red square
        frame[150:250, 300:400] = [0, 255, 0]  # Green square
        frame[200:300, 200:300] = [0, 0, 255]  # Blue square
        
        # Add text overlay
        cv2.putText(frame, "Simulated Feed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Enable webcam for real testing", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Convert to RGB for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display frame
        placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
        return frame
    
    @staticmethod
    def capture_frame():
        """Capture current frame for analysis"""
        # Try to capture from real webcam first
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Add color test overlay
                from .webcam_ui import WebcamUI
                frame = WebcamUI.add_color_vision_overlay(frame)
                st.session_state.captured_frame = frame
                from .color_analysis import ColorAnalysis
                ColorAnalysis.perform_color_analysis(frame)
                return frame
        
        # Fallback to simulated frame if webcam not available
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add some colored regions
        frame[100:200, 100:200] = [255, 0, 0]  # Red
        frame[150:250, 300:400] = [0, 255, 0]  # Green
        frame[200:300, 200:300] = [0, 0, 255]  # Blue
        
        st.session_state.captured_frame = frame
        from .color_analysis import ColorAnalysis
        ColorAnalysis.perform_color_analysis(frame)
        return frame
