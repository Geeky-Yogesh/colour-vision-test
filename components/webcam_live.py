import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Handle different MediaPipe versions
try:
    mp_face_mesh = mp.solutions.face_mesh
    HAS_MEDIAPIPE_FACE_MESH = True
except AttributeError:
    # Fallback if MediaPipe face_mesh is not available
    HAS_MEDIAPIPE_FACE_MESH = False

class AdvancedVisionProcessor(VideoProcessorBase):
    def __init__(self):
        # Calibration constants
        self.REAL_EYE_DISTANCE_CM = 6.4  # Average adult interpupillary distance
        self.FOCAL_LENGTH = 850          # Calibrated for typical laptop webcams
        
        # Smoothing buffers (averages the last 5 frames for stability)
        self.dist_history = deque(maxlen=5)
        self.gaze_history = deque(maxlen=5)
        
        # Initialize face mesh if available
        if HAS_MEDIAPIPE_FACE_MESH:
            self.face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True, # Enables iris and eye-lid tracking
                min_detection_confidence=0.6,
                min_tracking_confidence=0.6
            )
            self.use_advanced = True
        else:
            # Fallback to OpenCV face detection
            self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.use_advanced = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        
        status_color = (0, 0, 255) # Default Red
        dist_text = "No Face Detected"
        gaze_text = "---"

        if self.use_advanced:
            # Advanced MediaPipe Face Mesh processing
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(img_rgb)

            if results.multi_face_landmarks:
                mesh_coords = results.multi_face_landmarks[0].landmark
                
                # --- 1. ACCURATE DISTANCE (Inter-ocular) ---
                # Landmark 33: Left Eye Inner, 263: Right Eye Inner
                p1 = mesh_coords[33]
                p2 = mesh_coords[263]
                
                # Calculate pixel distance between eyes
                eye_dist_px = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2) * w
                
                # Distance Formula: D = (Real_W * Focal) / Pixel_W
                current_dist = (self.REAL_EYE_DISTANCE_CM * self.FOCAL_LENGTH) / eye_dist_px
                self.dist_history.append(current_dist)
                avg_dist = sum(self.dist_history) / len(self.dist_history)

                # --- 2. HEAD POSE / GAZE FIXATION ---
                # We track the Nose Tip (1) relative to the Eye Midpoint
                nose = mesh_coords[1]
                eye_midpoint_x = (p1.x + p2.x) / 2
                
                # Rotation Check: Is the nose centered between the eyes?
                # head_offset > 0.05 means the user is looking away or tilted
                head_offset = abs(nose.x - eye_midpoint_x)
                self.gaze_history.append(head_offset)
                avg_gaze = sum(self.gaze_history) / len(self.gaze_history)

                # --- 3. LOGIC FOR VALIDATION ---
                is_dist_ok = 65 <= avg_dist <= 85
                is_gaze_ok = avg_gaze < 0.04 # Tight threshold for center gaze
                
                if is_dist_ok and is_gaze_ok:
                    status_color = (0, 255, 0) # Green (Perfect)
                    dist_text = f"Distance: {avg_dist:.1f} cm (Good)"
                    gaze_text = "Gaze: Fixated"
                else:
                    status_color = (0, 165, 255) # Orange (Adjusting)
                    dist_text = f"Distance: {avg_dist:.1f} cm"
                    gaze_text = "Gaze: LOOK AT CENTER" if not is_gaze_ok else "Gaze: OK"

                # --- 4. VISUAL FEEDBACK OVERLAYS ---
                # Draw Face Mesh Outline (subtle)
                for idx in [33, 263, 1, 61, 291]: # Eyes, Nose, Mouth Corners
                    pt = mesh_coords[idx]
                    cv2.circle(img, (int(pt.x*w), int(pt.y*h)), 2, status_color, -1)

                # Draw Status Box
                cv2.rectangle(img, (10, 10), (420, 100), (0,0,0), -1) # Background
                cv2.putText(img, dist_text, (20, 45), cv2.FONT_HERSHEY_DUPLEX, 0.7, status_color, 1)
                cv2.putText(img, gaze_text, (20, 85), cv2.FONT_HERSHEY_DUPLEX, 0.7, status_color, 1)
                
                # Guide Circle
                cv2.circle(img, (w//2, h//2), 120, (255, 255, 255), 1)
        else:
            # Fallback to basic OpenCV face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                x, y, face_w, face_h = faces[0]
                
                # Basic distance estimation using face width
                current_dist = (14.5 * 850) / face_w  # Average face width 14.5cm
                self.dist_history.append(current_dist)
                avg_dist = sum(self.dist_history) / len(self.dist_history)
                
                # Basic validation logic
                if 65 <= avg_dist <= 85:
                    status_color = (0, 255, 0) # Green
                    dist_text = f"Distance: {avg_dist:.1f} cm (Good)"
                    gaze_text = "Position: OK"
                else:
                    status_color = (0, 165, 255) # Orange
                    dist_text = f"Distance: {avg_dist:.1f} cm"
                    gaze_text = "Position: ADJUST"
                
                # Draw basic feedback
                cv2.rectangle(img, (x, y), (x + face_w, y + face_h), status_color, 2)
                cv2.rectangle(img, (10, 10), (350, 80), (0,0,0), -1)
                cv2.putText(img, dist_text, (20, 35), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_color, 1)
                cv2.putText(img, gaze_text, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 0.6, status_color, 1)

        # Draw Status Box
        cv2.rectangle(img, (10, 10), (420, 100), (0,0,0), -1) # Background
        cv2.putText(img, dist_text, (20, 45), cv2.FONT_HERSHEY_DUPLEX, 0.7, status_color, 1)
        cv2.putText(img, gaze_text, (20, 85), cv2.FONT_HERSHEY_DUPLEX, 0.7, status_color, 1)
        
        # Guide Circle
        cv2.circle(img, (w//2, h//2), 120, (255, 255, 255), 1)

        return frame.from_ndarray(img, format="bgr24")

def webcam_live_page():
    st.title("🔬 Advanced Vision Calibration")
    st.markdown("""
    **Validation Requirements:**
    1. **Distance:** Must be between **65cm and 85cm**.
    2. **Fixation:** You must look directly at the center of the screen.
    3. **Lighting:** Ensure your face is evenly lit.
    """)

    webrtc_streamer(
        key="vision-validator",
        video_processor_factory=AdvancedVisionProcessor,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        media_stream_constraints={"video": True, "audio": False},
    )

    if st.button("🚀 Start Professional Assessment"):
        st.session_state.current_test = "ishihara"
        st.rerun()
