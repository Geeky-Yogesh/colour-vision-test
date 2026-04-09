"""
Webcam Component - Live Color Vision Testing
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from .distance_guide import DistanceGuide

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
    
    # Sidebar controls
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
    
    # Show distance reminder for webcam testing
    DistanceGuide.show_distance_reminder("Webcam Color Test")
    
    # Main content area
    if st.session_state.webcam_active:
        display_webcam_feed(test_mode)
    else:
        st.info("Click 'Start Camera' to begin the webcam test.")
    
    # Display captured frame and analysis
    if st.session_state.captured_frame is not None:
        display_analysis(test_mode)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    if col1.button(" Back to Menu"):
        st.session_state.webcam_active = False
        st.session_state.captured_frame = None
        st.session_state.color_analysis = None
        st.session_state.current_test = None
        st.rerun()

def display_webcam_feed(test_mode):
    """Display live webcam feed with test overlays"""
    
    # Create placeholder for video
    video_placeholder = st.empty()
    
    # Instructions based on test mode
    if test_mode == "Color Recognition":
        st.subheader("Color Recognition Test")
        st.write("Look at the colored objects around you and identify their colors.")
        
        # Color challenge
        target_color = st.selectbox(
            "Find an object with this color:",
            ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
        )
        
        if st.button("I found it!"):
            capture_frame()
            
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
            capture_frame()
            
    elif test_mode == "Live Analysis":
        st.subheader("Live Color Analysis")
        st.write("Real-time color analysis of your environment.")
        
        if st.button("Analyze Current Frame"):
            capture_frame()
    
    # Simulate webcam feed (in real implementation, this would use actual webcam)
    display_simulated_feed(video_placeholder)

def display_simulated_feed(placeholder):
    """Display simulated webcam feed (replace with actual webcam implementation)"""
    
    # Create a simulated frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some colored regions to simulate environment
    frame[100:200, 100:200] = [255, 0, 0]  # Red square
    frame[150:250, 300:400] = [0, 255, 0]  # Green square
    frame[200:300, 200:300] = [0, 0, 255]  # Blue square
    
    # Add text overlay
    cv2.putText(frame, "Live Feed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Position camera for best view", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Convert to RGB for display
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Display frame
    placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

def capture_frame():
    """Capture current frame for analysis"""
    # In real implementation, this would capture from actual webcam
    # For now, create a simulated captured frame
    
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some colored regions
    frame[100:200, 100:200] = [255, 0, 0]  # Red
    frame[150:250, 300:400] = [0, 255, 0]  # Green
    frame[200:300, 200:300] = [0, 0, 255]  # Blue
    
    st.session_state.captured_frame = frame
    perform_color_analysis(frame)

def perform_color_analysis(frame):
    """Analyze colors in the captured frame"""
    
    # Convert to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Reshape for analysis
    pixels = frame_rgb.reshape(-1, 3)
    
    # Calculate color statistics
    mean_color = np.mean(pixels, axis=0)
    std_color = np.std(pixels, axis=0)
    
    # Find dominant colors (simplified)
    unique_colors = np.unique(pixels, axis=0)
    color_counts = []
    
    for color in unique_colors[:10]:  # Top 10 colors
        if not np.array_equal(color, [0, 0, 0]):  # Skip black
            count = np.sum(np.all(pixels == color, axis=1))
            color_counts.append({
                'color': f'rgb({color[0]},{color[1]},{color[2]})',
                'count': count,
                'percentage': (count / len(pixels)) * 100
            })
    
    # Sort by count
    color_counts.sort(key=lambda x: x['count'], reverse=True)
    
    # Store analysis results
    st.session_state.color_analysis = {
        'mean_color': mean_color,
        'std_color': std_color,
        'dominant_colors': color_counts[:5],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def display_analysis(test_mode):
    """Display captured frame and color analysis"""
    
    st.subheader(" Analysis Results")
    
    # Display captured frame
    if st.session_state.captured_frame is not None:
        frame_rgb = cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, channels="RGB", caption="Captured Frame", use_column_width=True)
    
    # Display color analysis
    if st.session_state.color_analysis is not None:
        analysis = st.session_state.color_analysis
        
        # Color statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Mean Red", f"{analysis['mean_color'][0]:.1f}")
            st.metric("Mean Green", f"{analysis['mean_color'][1]:.1f}")
            st.metric("Mean Blue", f"{analysis['mean_color'][2]:.1f}")
        
        with col2:
            st.metric("Red Std Dev", f"{analysis['std_color'][0]:.1f}")
            st.metric("Green Std Dev", f"{analysis['std_color'][1]:.1f}")
            st.metric("Blue Std Dev", f"{analysis['std_color'][2]:.1f}")
        
        # Dominant colors visualization
        if analysis['dominant_colors']:
            st.subheader("Dominant Colors")
            
            # Create color bar chart
            colors = [c['color'] for c in analysis['dominant_colors']]
            percentages = [c['percentage'] for c in analysis['dominant_colors']]
            labels = [f"Color {i+1}" for i in range(len(colors))]
            
            fig = go.Figure(data=[
                go.Bar(x=labels, y=percentages, marker_color=colors)
            ])
            fig.update_layout(
                title="Color Distribution",
                xaxis_title="Colors",
                yaxis_title="Percentage (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Test results based on mode
        if test_mode == "Color Recognition":
            st.success("Color recognition test completed! Analysis shows color distribution.")
        elif test_mode == "Color Matching":
            st.info("Color matching analysis completed. Compare with reference colors.")
        elif test_mode == "Live Analysis":
            st.info("Live color analysis completed. Environment color profile generated.")
        
        # Save results
        if st.button("Save Results"):
            save_webcam_results(test_mode)

def save_webcam_results(test_mode):
    """Save webcam test results to session state"""
    
    if st.session_state.color_analysis:
        result = {
            "test_type": f"Webcam {test_mode}",
            "result": "Completed",
            "score": "Analysis Available",
            "timestamp": st.session_state.color_analysis['timestamp'],
            "details": {
                "mean_color": st.session_state.color_analysis['mean_color'].tolist(),
                "dominant_colors": len(st.session_state.color_analysis['dominant_colors'])
            }
        }
        
        st.session_state.test_results.append(result)
        st.success("Results saved successfully!")
        
        # Clear captured data
        st.session_state.captured_frame = None
        st.session_state.color_analysis = None
        st.rerun()
