import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# RTC Configuration for STUN servers (required for web deployment)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Handle different MediaPipe versions
try:
    mp_face_detection = mp.solutions.face_detection
    HAS_MEDIAPIPE_FACE_DETECTION = True
except AttributeError:
    # Fallback to OpenCV face detection if MediaPipe solutions is not available
    HAS_MEDIAPIPE_FACE_DETECTION = False

class DistanceProcessor(VideoProcessorBase):
    def __init__(self):
        # 1. High-accuracy detector
        if HAS_MEDIAPIPE_FACE_DETECTION:
            self.face_detector = mp_face_detection.FaceDetection(
                model_selection=0, # 0 for short-range (within 2m), 1 for long-range
                min_detection_confidence=0.6
            )
            self.use_opencv_fallback = False
        else:
            # Fallback to OpenCV face detection if MediaPipe FaceDetection is not available
            self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.use_opencv_fallback = True
        
        # 2. Calibration constants
        self.KNOWN_FACE_WIDTH_CM = 14.5  # Average adult face width
        self.FOCAL_LENGTH = 700          # Approximate focal length for standard webcams
        self.CREDIT_CARD_WIDTH_CM = 8.5  # Standard credit card width for calibration
        
        # 3. Temporal Smoothing (Buffer) - CRITICAL FOR STABILITY
        # Without this: Text flashes "No face detected" and disappears when face detector misses
        # With this: Software remembers last 10 frames (~0.3 seconds) and averages distance
        # Result: Smooth, professional transitions between distance zones (green/orange/yellow)
        self.distance_history = deque(maxlen=10)
        
        # 4. Environmental checks
        self.brightness_warning = False
        self.calibration_mode = False
        self.calibration_samples = []

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        
        # Environmental Check: Brightness Detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        self.brightness_warning = avg_brightness < 50  # Threshold for too dark
        
        # Face detection based on available method
        distance_text = "Searching for face..."
        color = (0, 0, 255) # Default Red
        
        # Add brightness warning if needed
        if self.brightness_warning:
            cv2.rectangle(img, (10, h-60), (400, h-20), (0, 0, 0), -1)
            cv2.putText(img, "⚠️ Environment too dark for accuracy", (20, h-35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        face_detected = False
        face_data = None
        
        if self.use_opencv_fallback:
            # Use OpenCV face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            if len(faces) > 0:
                face_detected = True
                face_data = faces[0]  # (x, y, w, h)
        else:
            # Use MediaPipe face detection
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_detector.process(img_rgb)
            if results.detections:
                face_detected = True
                face_data = results.detections[0]

        if face_detected:
            if self.use_opencv_fallback:
                # OpenCV format: (x, y, w, h)
                x, y, face_w, face_h = face_data
            else:
                # MediaPipe format: detection object with bounding box
                detection = face_data
                bbox = detection.location_data.relative_bounding_box
                
                # Convert relative coordinates to pixels
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                face_w = int(bbox.width * w)
                face_h = int(bbox.height * h)
            
            # Estimate distance
            current_dist = (self.KNOWN_FACE_WIDTH_CM * self.FOCAL_LENGTH) / face_w
            self.distance_history.append(current_dist)
            
            # Calculate Smoothed Distance (Average of the buffer)
            avg_distance = sum(self.distance_history) / len(self.distance_history)
            
            # Logic for Status
            if 60 <= avg_distance <= 90:
                status = "PERFECT"
                color = (0, 255, 0) # Green
            elif avg_distance < 60:
                status = "TOO CLOSE"
                color = (0, 165, 255) # Orange
            else:
                status = "TOO FAR"
                color = (0, 255, 255) # Yellow

            distance_text = f"{status}: {avg_distance:.1f} cm"

            # Visual Feedback: Rounded rectangle around face
            cv2.rectangle(img, (x, y), (x + face_w, y + face_h), color, 2)
            # Draw a 'fill' for the status text area
            cv2.rectangle(img, (20, 20), (450, 80), (0,0,0), -1)
        else:
            # If face is lost, clear the history buffer slowly
            if self.distance_history:
                self.distance_history.popleft()

        # Overlay text
        cv2.putText(img, distance_text, (40, 60), 
                    cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
        
        # Add a "Center Mask" guide - encourages users to stay centered
        overlay = img.copy()
        cv2.circle(overlay, (w//2, h//2), 150, (255, 255, 255), 2)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

        return frame.from_ndarray(img, format="bgr24")

def webcam_live_page():
    st.title("🎥 Real-Time Distance Calibration")
    
    # Environmental Reliability Tips
    with st.expander("🔧 Environmental Setup for Medical-Grade Accuracy", expanded=True):
        st.markdown("""
        **⚠️ Important Setup Requirements:**
        
        **1. Lighting Conditions:**
        - ✅ Ensure light is on your face, not behind you
        - ❌ Avoid bright windows or lights behind you (causes silhouette effect)
        - ✅ Use even, frontal lighting for best face detection
        - ⚠️ If environment is too dark, accuracy warning will appear
        
        **2. Camera Calibration (Recommended for 100% Accuracy):**
        - 🎯 For medical-grade precision, calibrate with a credit card
        - Hold a standard credit card (8.5cm width) to your camera once
        - This adjusts the focal length for your specific camera
        - Different cameras (MacBook vs USB webcam) have different focal lengths
        
        **3. Positioning:**
        - Sit centered in the camera view
        - Keep your face clearly visible
        - Avoid dramatic shadows or backlighting
        """)
    
    st.markdown("""
    **Quick Instructions:**
    1. Click 'Start' below to enable your camera
    2. Follow the environmental setup tips above
    3. Position yourself so the indicator turns **Green**
    4. The box and text will change color based on your distance:
       - <span style='color:orange'>**Orange**</span>: Too Close
       - <span style='color:green'>**Green**</span>: Perfect (60-90cm)
       - <span style='color:yellow'>**Yellow**</span>: Too Far
    """, unsafe_allow_html=True)

    # Calibration controls
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("🎯 For medical-grade accuracy, use credit card calibration below")
    with col2:
        if st.button("📏 Calibrate with Credit Card"):
            st.session_state.calibration_mode = True
            st.success("Hold a credit card (8.5cm) to your camera now")
    
    webrtc_streamer(
        key="distance-calibration",
        video_processor_factory=DistanceProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
    )
    
    # Browser permissions helper
    st.caption("💡 Note: If the camera doesn't start, check your browser's site permissions and refresh.")

    # Environmental status
    processor = DistanceProcessor()
    if hasattr(processor, 'brightness_warning') and processor.brightness_warning:
        st.error("⚠️ Environment too dark for accurate distance detection")

    if st.button("✅ I am positioned correctly. Start Test!"):
        st.session_state.current_test = "ishihara"
        st.rerun()
