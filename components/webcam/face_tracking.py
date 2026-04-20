"""
Face Tracking Module - Real-time face detection and head movement analysis
Uses MediaPipe Face Mesh for accurate landmark tracking with Kalman filtering for stability
"""

import cv2
import numpy as np
from collections import deque
import math
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass

# Try to use MediaPipe if available, otherwise fallback to OpenCV
try:
    import mediapipe as mp
    # Try to access face mesh (works in older versions)
    try:
        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        USE_MEDIAPIPE = True
    except AttributeError:
        USE_MEDIAPIPE = False
except ImportError:
    USE_MEDIAPIPE = False

@dataclass
class FaceMetrics:
    """Data class for face tracking metrics"""
    x: float
    y: float
    width: float
    height: float
    dx: float  # Movement in X direction
    dy: float  # Movement in Y direction
    tilt_angle: float  # Head tilt angle in degrees
    confidence: float
    timestamp: float

class KalmanFilter:
    """Simple Kalman filter for smoothing face tracking"""
    
    def __init__(self, process_variance=1e-3, measurement_variance=1e-1):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimated_value = 0
        self.estimated_variance = 1
        self.kalman_gain = 0
    
    def update(self, measurement):
        """Update filter with new measurement"""
        # Prediction
        self.estimated_variance += self.process_variance
        
        # Update
        self.kalman_gain = self.estimated_variance / (self.estimated_variance + self.measurement_variance)
        self.estimated_value += self.kalman_gain * (measurement - self.estimated_value)
        self.estimated_variance *= (1 - self.kalman_gain)
        
        return self.estimated_value

class FaceTracker:
    """Real-time face tracking with head movement analysis"""
    
    def __init__(self):
        # Initialize face detection based on available libraries
        if USE_MEDIAPIPE:
            # Use MediaPipe Face Mesh
            self.face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.face_cascade = None
        else:
            # Fallback to OpenCV Haar Cascade
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.face_mesh = None
        
        # For eye detection (used in tilt calculation)
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Kalman filters for smoothing
        self.kalman_x = KalmanFilter()
        self.kalman_y = KalmanFilter()
        self.kalman_width = KalmanFilter()
        self.kalman_height = KalmanFilter()
        
        # Movement tracking
        self.previous_position = None
        self.movement_history = deque(maxlen=10)  # Store last 10 positions for smoothing
        
        # Face metrics
        self.current_metrics = None
        self.face_detected = False
        
        # Landmark indices for key features
        self.landmark_indices = {
            'nose_tip': 1,
            'left_eye_center': 33,
            'right_eye_center': 263,
            'left_eye_corner': 33,
            'right_eye_corner': 263,
            'forehead_center': 10,
            'chin_center': 152
        }
    
    def detect_face(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect face and extract landmarks"""
        if USE_MEDIAPIPE and self.face_mesh is not None:
            return self._detect_with_mediapipe(frame)
        else:
            return self._detect_with_opencv(frame)
    
    def _detect_with_mediapipe(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect face using MediaPipe Face Mesh"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            
            # Extract key landmarks
            face_data = self._extract_landmarks_mediapipe(landmarks, frame.shape)
            
            if face_data:
                self.face_detected = True
                return face_data
        
        self.face_detected = False
        return None
    
    def _detect_with_opencv(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect face using OpenCV Haar Cascade"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get the largest face
            face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = face
            
            # Detect eyes within the face region for tilt calculation
            face_roi = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_roi)
            
            # Extract face data
            face_data = self._extract_landmarks_opencv(face, eyes, frame.shape)
            
            if face_data:
                self.face_detected = True
                return face_data
        
        self.face_detected = False
        return None
    
    def _extract_landmarks_mediapipe(self, landmarks, frame_shape) -> Dict[str, Any]:
        """Extract key landmarks from MediaPipe and calculate face metrics"""
        height, width = frame_shape[:2]
        
        # Get landmark coordinates
        def get_landmark_coords(index):
            landmark = landmarks.landmark[index]
            return int(landmark.x * width), int(landmark.y * height)
        
        # Extract key points
        nose_tip = get_landmark_coords(self.landmark_indices['nose_tip'])
        left_eye = get_landmark_coords(self.landmark_indices['left_eye_center'])
        right_eye = get_landmark_coords(self.landmark_indices['right_eye_center'])
        forehead = get_landmark_coords(self.landmark_indices['forehead_center'])
        chin = get_landmark_coords(self.landmark_indices['chin_center'])
        
        # Calculate bounding box
        all_x = [nose_tip[0], left_eye[0], right_eye[0], forehead[0], chin[0]]
        all_y = [nose_tip[1], left_eye[1], right_eye[1], forehead[1], chin[1]]
        
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        
        # Add padding to bounding box
        padding_x = int((x_max - x_min) * 0.2)
        padding_y = int((y_max - y_min) * 0.2)
        
        x_min = max(0, x_min - padding_x)
        x_max = min(width, x_max + padding_x)
        y_min = max(0, y_min - padding_y)
        y_max = min(height, y_max + padding_y)
        
        return self._create_face_data(x_min, y_min, x_max, y_max, nose_tip, left_eye, right_eye, landmarks)
    
    def _extract_landmarks_opencv(self, face_rect, eyes, frame_shape) -> Dict[str, Any]:
        """Extract landmarks from OpenCV detection and calculate face metrics"""
        x, y, w, h = face_rect
        
        # Calculate approximate positions for key features
        nose_tip = (x + w//2, y + h//2)
        forehead = (x + w//2, y + h//4)
        chin = (x + w//2, y + 3*h//4)
        
        # Extract eye positions
        left_eye = right_eye = nose_tip
        if len(eyes) >= 2:
            # Sort eyes by x position
            eyes_sorted = sorted(eyes, key=lambda e: e[0])
            left_eye = (x + eyes_sorted[0][0] + eyes_sorted[0][2]//2, y + eyes_sorted[0][1] + eyes_sorted[0][3]//2)
            right_eye = (x + eyes_sorted[1][0] + eyes_sorted[1][2]//2, y + eyes_sorted[1][1] + eyes_sorted[1][3]//2)
        
        return self._create_face_data(x, y, x+w, y+h, nose_tip, left_eye, right_eye, None)
    
    def _create_face_data(self, x_min, y_min, x_max, y_max, nose_tip, left_eye, right_eye, landmarks):
        """Create face data dictionary with metrics"""
        height = max(y_max - y_min, 1)
        width = max(x_max - x_min, 1)
        
        # Calculate face center
        face_center_x = (x_min + x_max) / 2
        face_center_y = (y_min + y_max) / 2
        
        # Apply Kalman filtering for stability
        smooth_x = self.kalman_x.update(face_center_x)
        smooth_y = self.kalman_y.update(face_center_y)
        smooth_width = self.kalman_width.update(width)
        smooth_height = self.kalman_height.update(height)
        
        # Calculate movement
        dx, dy = 0, 0
        if self.previous_position:
            dx = smooth_x - self.previous_position['x']
            dy = smooth_y - self.previous_position['y']
        
        # Calculate head tilt angle using eye positions
        tilt_angle = self._calculate_tilt_angle(left_eye, right_eye)
        
        # Store current position
        current_position = {
            'x': smooth_x,
            'y': smooth_y,
            'width': smooth_width,
            'height': smooth_height
        }
        
        # Update movement history
        self.movement_history.append({
            'dx': dx,
            'dy': dy,
            'tilt': tilt_angle
        })
        
        # Calculate smoothed movement metrics
        smoothed_dx = np.mean([m['dx'] for m in self.movement_history]) if self.movement_history else 0
        smoothed_dy = np.mean([m['dy'] for m in self.movement_history]) if self.movement_history else 0
        smoothed_tilt = np.mean([m['tilt'] for m in self.movement_history]) if self.movement_history else 0
        
        # Create metrics object
        self.current_metrics = FaceMetrics(
            x=smooth_x,
            y=smooth_y,
            width=smooth_width,
            height=smooth_height,
            dx=smoothed_dx,
            dy=smoothed_dy,
            tilt_angle=smoothed_tilt,
            confidence=0.8 if USE_MEDIAPIPE else 0.6,  # Different confidence levels
            timestamp=cv2.getTickCount() / cv2.getTickFrequency()
        )
        
        self.previous_position = current_position
        
        return {
            'landmarks': landmarks,
            'bounding_box': (int(x_min), int(y_min), int(x_max), int(y_max)),
            'smoothed_box': (int(smooth_x - smooth_width/2), int(smooth_y - smooth_height/2), 
                            int(smooth_x + smooth_width/2), int(smooth_y + smooth_height/2)),
            'nose_tip': nose_tip,
            'left_eye': left_eye,
            'right_eye': right_eye,
            'metrics': self.current_metrics
        }
    
    def _calculate_tilt_angle(self, left_eye: Tuple[int, int], right_eye: Tuple[int, int]) -> float:
        """Calculate head tilt angle using eye positions"""
        # Calculate angle between eyes
        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]
        
        # Calculate angle in radians and convert to degrees
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        return angle_deg
    
    def draw_tracking_overlay(self, frame: np.ndarray, face_data: Dict[str, Any]) -> np.ndarray:
        """Draw tracking overlay on frame"""
        if not face_data:
            return frame
        
        # Create a copy for drawing
        overlay_frame = frame.copy()
        
        # Draw smoothed bounding box
        x1, y1, x2, y2 = face_data['smoothed_box']
        cv2.rectangle(overlay_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw face mesh landmarks if using MediaPipe
        if 'landmarks' in face_data and face_data['landmarks'] is not None and USE_MEDIAPIPE:
            try:
                self.mp_drawing.draw_landmarks(
                    overlay_frame,
                    face_data['landmarks'],
                    self.mp_face_mesh.FACEMESH_CONTOURS,
                    None,
                    self.mp_drawing_styles.get_default_face_mesh_contours_style()
                )
            except:
                pass  # Skip if drawing fails
        
        # Draw key points
        for point_name, point in [('nose_tip', face_data['nose_tip']), 
                                 ('left_eye', face_data['left_eye']), 
                                 ('right_eye', face_data['right_eye'])]:
            cv2.circle(overlay_frame, point, 3, (255, 0, 0), -1)
        
        # Draw metrics on frame
        metrics = face_data['metrics']
        self._draw_metrics(overlay_frame, metrics, (x1, y1 - 10))
        
        return overlay_frame
    
    def _draw_metrics(self, frame: np.ndarray, metrics: FaceMetrics, position: Tuple[int, int]):
        """Draw movement metrics on frame"""
        x, y = position
        
        # Prepare text
        texts = [
            f"X: {metrics.x:.1f}  dx: {metrics.dx:.1f}",
            f"Y: {metrics.y:.1f}  dy: {metrics.dy:.1f}",
            f"Tilt: {metrics.tilt_angle:.1f}°"
        ]
        
        # Draw background rectangle for better visibility
        text_height = 25
        bg_height = len(texts) * text_height + 10
        cv2.rectangle(frame, (x - 5, y - bg_height), (x + 250, y + 5), (0, 0, 0), -1)
        
        # Draw text
        for i, text in enumerate(texts):
            text_y = y - (len(texts) - i - 1) * text_height
            cv2.putText(frame, text, (x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    def get_current_metrics(self) -> Optional[FaceMetrics]:
        """Get current face tracking metrics"""
        return self.current_metrics
    
    def is_face_detected(self) -> bool:
        """Check if face is currently detected"""
        return self.face_detected
    
    def reset_tracking(self):
        """Reset tracking state"""
        self.previous_position = None
        self.movement_history.clear()
        self.current_metrics = None
        self.face_detected = False
        
        # Reset Kalman filters
        self.kalman_x = KalmanFilter()
        self.kalman_y = KalmanFilter()
        self.kalman_width = KalmanFilter()
        self.kalman_height = KalmanFilter()
    
    def release(self):
        """Release resources"""
        if USE_MEDIAPIPE and self.face_mesh is not None:
            try:
                self.face_mesh.close()
            except:
                pass
