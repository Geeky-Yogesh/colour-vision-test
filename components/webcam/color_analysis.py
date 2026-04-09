"""
Color Analysis Module - Analyze colors from webcam frames
"""

import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import cv2
from datetime import datetime

class ColorAnalysis:
    """Handle color analysis from captured frames"""
    
    @staticmethod
    def perform_color_analysis(frame):
        """Analyze colors in the captured frame"""
        
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if hasattr(frame, 'shape') else frame
        
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
    
    @staticmethod
    def display_analysis(test_mode):
        """Display captured frame and color analysis"""
        
        st.subheader(" Analysis Results")
        
        # Display captured frame
        if st.session_state.captured_frame is not None:
            frame_rgb = cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, channels="RGB", caption="Captured Frame", use_container_width=True)
        
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
                ColorAnalysis.save_webcam_results(test_mode)
    
    @staticmethod
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
