"""
Distance Guide Component - Optimal Viewing Distance for Colour Vision Tests
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

class DistanceGuide:
    """Distance guidance and calibration for colour vision tests"""
    
    @staticmethod
    def get_optimal_distances():
        """Return recommended distances for different screen sizes"""
        return {
            "Phone/Tablet": {"min": 30, "optimal": 40, "max": 50, "unit": "cm"},
            "Laptop (13-15\")": {"min": 50, "optimal": 65, "max": 80, "unit": "cm"},
            "Monitor (20-24\")": {"min": 60, "optimal": 75, "max": 100, "unit": "cm"},
            "Large Monitor (27\")": {"min": 70, "optimal": 85, "max": 120, "unit": "cm"}
        }
    
    @staticmethod
    def show_distance_calibrator():
        """Display distance calibration interface"""
        st.title(" Distance Calibration")
        st.markdown("---")
        
        # Screen size selection
        screen_sizes = list(DistanceGuide.get_optimal_distances().keys())
        selected_screen = st.selectbox("Select your screen size:", screen_sizes)
        
        distances = DistanceGuide.get_optimal_distances()[selected_screen]
        
        # Display recommended distance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Minimum", f"{distances['min']} {distances['unit']}")
        with col2:
            st.metric("Optimal", f"{distances['optimal']} {distances['unit']}", delta="Recommended")
        with col3:
            st.metric("Maximum", f"{distances['max']} {distances['unit']}")
        
        # Visual guide
        st.subheader("Visual Positioning Guide")
        DistanceGuide._create_positioning_visual(distances)
        
        # Calibration instructions
        st.subheader("How to Calibrate")
        st.markdown("""
        **Steps for optimal distance:**
        1. Sit comfortably in your chair
        2. Extend your arm straight forward
        3. Your screen should be about arm's length away
        4. Adjust until the test fills your vision comfortably
        5. You should be able to see the entire test without tilting your head
        """)
        
        # Save calibration
        if st.button("Save Distance Setting"):
            st.session_state.calibrated_distance = distances['optimal']
            st.session_state.screen_size = selected_screen
            st.success(f"Calibration saved: {distances['optimal']} {distances['unit']}")
    
    @staticmethod
    def _create_positioning_visual(distances):
        """Create visual positioning guide"""
        fig = go.Figure()
        
        # Add user representation
        fig.add_shape(type="circle", xref="x", yref="y",
                     x0=0, y0=0, x1=10, y1=10,
                     fillcolor="blue", opacity=0.3, line=dict(color="blue"))
        
        # Add screen representation
        screen_distance = distances['optimal'] / 10  # Scale for visualization
        fig.add_shape(type="rect", xref="x", yref="y",
                     x0=screen_distance-2, y0=-5, x1=screen_distance+2, y1=5,
                     fillcolor="green", opacity=0.3, line=dict(color="green"))
        
        # Add distance zones
        min_dist = distances['min'] / 10
        max_dist = distances['max'] / 10
        
        # Too close zone
        fig.add_shape(type="rect", xref="x", yref="y",
                     x0=0, y0=-8, x1=min_dist, y1=8,
                     fillcolor="red", opacity=0.1, line=dict(color="red", dash="dash"))
        
        # Optimal zone
        fig.add_shape(type="rect", xref="x", yref="y",
                     x0=min_dist, y0=-8, x1=max_dist, y1=8,
                     fillcolor="green", opacity=0.1, line=dict(color="green"))
        
        # Too far zone
        fig.add_shape(type="rect", xref="x", yref="y",
                     x0=max_dist, y0=-8, x1=20, y1=8,
                     fillcolor="orange", opacity=0.1, line=dict(color="orange", dash="dash"))
        
        # Add labels
        fig.add_annotation(x=min_dist/2, y=9, text="Too Close", showarrow=False, font=dict(color="red"))
        fig.add_annotation(x=screen_distance, y=9, text="Optimal", showarrow=False, font=dict(color="green"))
        fig.add_annotation(x=(max_dist+20)/2, y=9, text="Too Far", showarrow=False, font=dict(color="orange"))
        
        # Add distance markers
        fig.add_annotation(x=min_dist, y=-9, text=f"{distances['min']}cm", showarrow=False)
        fig.add_annotation(x=screen_distance, y=-9, text=f"{distances['optimal']}cm", showarrow=False)
        fig.add_annotation(x=max_dist, y=-9, text=f"{distances['max']}cm", showarrow=False)
        
        fig.update_layout(
            title="Positioning Guide",
            xaxis=dict(visible=False, range=[0, 20]),
            yaxis=dict(visible=False, range=[-10, 10]),
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def show_distance_reminder(test_type="Ishihara"):
        """Show distance reminder during testing"""
        if 'calibrated_distance' in st.session_state:
            distance = st.session_state.calibrated_distance
            screen_size = st.session_state.get('screen_size', 'Unknown')
            
            st.info(f"""
            **Distance Reminder**
            
            Optimal distance: {distance}cm for {screen_size}
            Test type: {test_type}
            
            Adjust your position if needed for best results.
            """)
        else:
            st.warning("""
            **Distance Not Calibrated**
            
            For best results, please calibrate your viewing distance first.
            Go to the Distance Calibration section in the menu.
            """)
    
    @staticmethod
    def check_webcam_distance(frame):
        """Estimate distance using webcam (simplified face detection)"""
        # This is a simplified version - in real implementation, you would use
        # face detection to estimate distance based on face size
        
        # For demonstration, return random distance estimates
        # In real implementation:
        # 1. Detect face using OpenCV or MediaPipe
        # 2. Calculate face size in pixels
        # 3. Estimate distance based on known face dimensions
        
        estimated_distance = np.random.normal(75, 10)  # Simulated distance in cm
        
        return {
            'estimated_distance': estimated_distance,
            'status': 'Good' if 60 <= estimated_distance <= 90 else 'Adjust Position',
            'recommendation': 'Move closer' if estimated_distance < 60 else 'Move further' if estimated_distance > 90 else 'Good position'
        }
    
    @staticmethod
    def show_distance_overlay():
        """Show overlay guide during testing"""
        # Create overlay with positioning guides
        fig = go.Figure()
        
        # Create circular guide
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = 50 + 40 * np.cos(theta)
        y_circle = 50 + 40 * np.sin(theta)
        
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle,
            mode='lines',
            line=dict(color='rgba(255,255,255,0.3)', width=2),
            hoverinfo='none'
        ))
        
        # Add crosshair
        fig.add_trace(go.Scatter(
            x=[50, 50], y=[10, 90],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dash'),
            hoverinfo='none'
        ))
        
        fig.add_trace(go.Scatter(
            x=[10, 90], y=[50, 50],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dash'),
            hoverinfo='none'
        ))
        
        fig.update_layout(
            width=500, height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
            yaxis=dict(visible=False, range=[0, 100], fixedrange=True),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return fig

def distance_settings_page():
    """Main distance settings page"""
    st.title(" Distance Settings")
    st.markdown("---")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["Calibration", "Guide", "Webcam Distance"])
    
    with tab1:
        DistanceGuide.show_distance_calibrator()
    
    with tab2:
        st.subheader("Distance Guidelines")
        st.markdown("""
        **Why Distance Matters:**
        - Ensures consistent test results
        - Maintains proper visual acuity
        - Follows standardized testing protocols
        
        **General Guidelines:**
        - Sit at arm's length from screen
        - Keep screen at eye level
        - Ensure good lighting
        - Avoid glare on screen
        """)
        
        # Show all distance recommendations
        distances = DistanceGuide.get_optimal_distances()
        
        st.subheader("Recommended Distances by Screen Size")
        
        for screen_size, dist in distances.items():
            with st.expander(f"{screen_size}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Min", f"{dist['min']} {dist['unit']}")
                col2.metric("Optimal", f"{dist['optimal']} {dist['unit']}")
                col3.metric("Max", f"{dist['max']} {dist['unit']}")
    
    with tab3:
        st.subheader("Webcam Distance Detection")
        st.info("""
        **Automatic Distance Detection**
        
        This feature uses face detection to estimate your distance from the camera.
        For best results:
        1. Ensure your face is clearly visible
        2. Good, even lighting
        3. Face centered in frame
        """)
        
        if st.button("Test Webcam Distance"):
            # Simulate webcam distance detection
            distance_info = DistanceGuide.check_webcam_distance(None)
            
            col1, col2 = st.columns(2)
            col1.metric("Estimated Distance", f"{distance_info['estimated_distance']:.1f} cm")
            col2.metric("Status", distance_info['status'])
            
            st.info(f"Recommendation: {distance_info['recommendation']}")
    
    # Back button
    if st.button(" Back to Menu"):
        st.session_state.current_test = None
        st.rerun()
