"""
Webcam Capture Module - Handle real and simulated webcam feeds with face tracking
"""

import cv2
import numpy as np
import streamlit as st
from .face_tracking import FaceTracker

class WebcamCapture:
    """Handle webcam capture and display"""
    
    def __init__(self):
        """Initialize webcam capture with face tracking"""
        self.face_tracker = FaceTracker()
    
    def display_real_webcam_feed(self, placeholder, enable_face_tracking=True):
        """Display real webcam feed with optional face tracking - continuous capture"""
        
        # Initialize webcam if not already initialized
        if 'webcam_cap' not in st.session_state:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                placeholder.error("Unable to access webcam. Please check permissions.")
                return None
            st.session_state.webcam_cap = cap
        else:
            cap = st.session_state.webcam_cap
        
        # Capture frame continuously
        ret, frame = cap.read()
        
        if ret:
            # Apply face tracking if enabled
            if enable_face_tracking:
                face_data = self.face_tracker.detect_face(frame)
                if face_data:
                    frame = self.face_tracker.draw_tracking_overlay(frame, face_data)
                    # Store current metrics in session state
                    st.session_state.face_metrics = face_data['metrics']
                else:
                    st.session_state.face_metrics = None
            
            # Add color vision test overlay
            from .webcam_ui import WebcamUI
            frame = WebcamUI.add_color_vision_overlay(frame)
            
            # Convert to RGB for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display frame with continuous refresh
            placeholder.image(frame_rgb, channels="RGB", width='stretch')
            
            # Store frame for capture
            st.session_state.current_frame = frame
            
            # Auto-refresh for real-time feed
            st.rerun()
            return frame
        else:
            placeholder.error("Failed to capture frame from webcam")
            return None
    
    def display_simulated_feed(self, placeholder, enable_face_tracking=True):
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
        placeholder.image(frame_rgb, channels="RGB", width='stretch')
        return frame
    
    def capture_frame(self):
        """Capture current frame for analysis"""
        # Try to capture from real webcam first
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Apply face tracking
                face_data = self.face_tracker.detect_face(frame)
                if face_data:
                    frame = self.face_tracker.draw_tracking_overlay(frame, face_data)
                    st.session_state.captured_face_metrics = face_data['metrics']
                else:
                    st.session_state.captured_face_metrics = None
                
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
    
    def get_face_tracker(self):
        """Get the face tracker instance"""
        return self.face_tracker
    
    def reset_tracking(self):
        """Reset face tracking state"""
        self.face_tracker.reset_tracking()
    
    def release_webcam(self):
        """Release webcam resource"""
        if 'webcam_cap' in st.session_state:
            st.session_state.webcam_cap.release()
            del st.session_state.webcam_cap
    
    def release(self):
        """Release resources"""
        self.release_webcam()
        if hasattr(self, 'face_tracker'):
            self.face_tracker.release()
