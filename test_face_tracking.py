#!/usr/bin/env python3
"""
Test script for face tracking functionality
"""

import cv2
import numpy as np
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.webcam.face_tracking import FaceTracker

def test_face_tracking():
    """Test face tracking with webcam"""
    print("🎥 Starting Face Tracking Test...")
    print("Press 'q' to quit, 'r' to reset tracking")
    
    # Initialize face tracker
    tracker = FaceTracker()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Unable to access webcam")
        return
    
    print("✅ Webcam initialized successfully")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break
        
        # Detect face
        face_data = tracker.detect_face(frame)
        
        if face_data:
            # Draw tracking overlay
            frame = tracker.draw_tracking_overlay(frame, face_data)
            
            # Get metrics
            metrics = face_data['metrics']
            print(f"📍 Position: ({metrics.x:.1f}, {metrics.y:.1f}) | Movement: ({metrics.dx:.1f}, {metrics.dy:.1f}) | Tilt: {metrics.tilt_angle:.1f}°")
        else:
            cv2.putText(frame, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display frame
        cv2.imshow('Face Tracking Test', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            tracker.reset_tracking()
            print("🔄 Tracking reset")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    tracker.release()
    print("✅ Test completed")

if __name__ == "__main__":
    test_face_tracking()
