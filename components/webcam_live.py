import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2
import mediapipe as mp
import numpy as np

# RTC Configuration for STUN servers (required for web deployment)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class DistanceProcessor(VideoProcessorBase):
    def __init__(self):
        # For MediaPipe 0.10+, we need to use a different approach
        # Let's try using OpenCV's built-in face detection as fallback
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.KNOWN_FACE_WIDTH_CM = 14.0  # Average face width in cm
        # Calibrated focal length - calibrated for your camera
        # Formula: Focal_Length = (Actual_Distance × Measured_Distance) / Current_Focal_Length
        self.FOCAL_LENGTH = 800 * (80 / 65)  # Calibrated to show correct distance 

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        
        # Convert to grayscale for OpenCV face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using OpenCV
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        distance_text = "No face detected"
        color = (0, 0, 255) # Red

        if len(faces) > 0:
            # Get the first face detected
            (x, y, face_w, face_h) = faces[0]
            
            # Estimate distance based on face width using calibrated focal length
            # Distance = (Known_Width * Focal_Length) / Pixel_Width
            distance_cm = (self.KNOWN_FACE_WIDTH_CM * self.FOCAL_LENGTH) / face_w
            distance_text = f"Distance: {distance_cm:.1f} cm (Face width: {face_w}px)"
            
            # Determine Color/Status
            if 65 <= distance_cm <= 85:
                color = (0, 255, 0)  # Green (Good)
            elif distance_cm < 65:
                color = (0, 165, 255) # Orange (Too Close)
            else:
                color = (0, 255, 255) # Yellow (Too Far)

            # Draw rectangle around face
            cv2.rectangle(img, (x, y), (x + face_w, y + face_h), color, 2)
            
            # Draw center point
            center_x = x + face_w // 2
            center_y = y + face_h // 2
            cv2.circle(img, (center_x, center_y), 4, color, -1)

        # Overlay text on the live video
        cv2.putText(img, distance_text, (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Draw a guide box for where the head should be
        cv2.rectangle(img, (w//4, h//4), (3*w//4, 3*h//4), color, 2)

        return frame.from_ndarray(img, format="bgr24")

def webcam_live_page():
    st.title("🎥 Real-Time Distance Calibration")
    st.markdown("""
    **Instructions:**
    1. Click 'Start' below to enable your camera.
    2. Position yourself so the indicator turns **Green**.
    3. The box and text will change color based on your distance:
       - <span style='color:orange'>**Orange**</span>: Too Close
       - <span style='color:green'>**Green**</span>: Perfect (65-85cm)
       - <span style='color:yellow'>**Yellow**</span>: Too Far
    """, unsafe_allow_html=True)

    webrtc_streamer(
        key="distance-calibration",
        video_processor_factory=DistanceProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
    )

    if st.button("✅ I am positioned correctly. Start Test!"):
        st.session_state.current_test = "ishihara"
        st.rerun()
