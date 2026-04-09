"""
Progress Visualizer Module - Create charts and visualizations for performance tracking
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .score_tracker import ScoreTracker

class ProgressVisualizer:
    """Handle visualization of performance data"""
    
    @staticmethod
    def show_progress_overview():
        """Display overall progress overview"""
        data = st.session_state.performance_data
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tests", data['total_tests'])
        with col2:
            st.metric("Best Score", f"{data['best_score']:.1f}%")
        with col3:
            st.metric("Average Score", f"{data['average_score']:.1f}%")
        with col4:
            completed_sessions = len([s for s in data['sessions'] if s['completed']])
            st.metric("Completed Sessions", completed_sessions)
    
    @staticmethod
    def show_score_progress_chart():
        """Display line chart of scores over time"""
        df = ScoreTracker.get_performance_history()
        
        if df.empty:
            st.info("No test data available yet. Complete some tests to see your progress!")
            return
        
        # Create line chart
        fig = px.line(
            df, 
            x='timestamp', 
            y='score',
            color='test_type',
            title="Performance Over Time",
            labels={
                'timestamp': 'Date',
                'score': 'Score (%)',
                'test_type': 'Test Type'
            },
            color_discrete_map={
                'Ishihara': '#FF6B6B',
                'Webcam Color Recognition': '#4ECDC4',
                'Webcam Color Matching': '#45B7D1',
                'Webcam Live Analysis': '#96CEB4'
            }
        )
        
        fig.update_layout(
            xaxis_title="Date & Time",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="progress_score_progress_chart")
    
    @staticmethod
    def show_overview_score_chart():
        """Display line chart for overview tab with unique key"""
        df = ScoreTracker.get_performance_history()
        
        if df.empty:
            st.info("No test data available yet. Complete some tests to see your progress!")
            return
        
        # Create line chart
        fig = px.line(
            df, 
            x='timestamp', 
            y='score',
            color='test_type',
            title="Performance Over Time",
            labels={
                'timestamp': 'Date',
                'score': 'Score (%)',
                'test_type': 'Test Type'
            },
            color_discrete_map={
                'Ishihara': '#FF6B6B',
                'Webcam Color Recognition': '#4ECDC4',
                'Webcam Color Matching': '#45B7D1',
                'Webcam Live Analysis': '#96CEB4'
            }
        )
        
        fig.update_layout(
            xaxis_title="Date & Time",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overview_score_progress_chart")
    
    @staticmethod
    def show_session_comparison():
        """Compare performance across different sessions"""
        data = st.session_state.performance_data
        completed_sessions = [s for s in data['sessions'] if s['completed'] and 'average_score' in s]
        
        if not completed_sessions:
            st.info("No completed sessions to compare.")
            return
        
        # Create session comparison chart
        session_names = [f"Session {i+1}" for i in range(len(completed_sessions))]
        avg_scores = [s['average_score'] * 100 for s in completed_sessions]
        
        fig = go.Figure(data=[
            go.Bar(
                x=session_names,
                y=avg_scores,
                marker_color=['#FF6B6B' if score >= 85 else '#FFA500' if score >= 60 else '#FF4444' for score in avg_scores]
            )
        ])
        
        fig.update_layout(
            title="Session Performance Comparison",
            xaxis_title="Test Sessions",
            yaxis_title="Average Score (%)",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="progress_session_comparison_chart")
    
    @staticmethod
    def show_test_type_performance():
        """Show performance by test type"""
        df = ScoreTracker.get_performance_history()
        
        if df.empty:
            return
        
        # Group by test type
        type_stats = df.groupby('test_type').agg({
            'score': ['mean', 'max', 'min', 'count']
        }).round(2)
        
        type_stats.columns = ['Average Score', 'Best Score', 'Worst Score', 'Test Count']
        
        # Create radar chart for test types
        if len(type_stats) > 1:
            fig = go.Figure()
            
            categories = type_stats.index.tolist()
            avg_scores = type_stats['Average Score'].tolist()
            
            fig.add_trace(go.Scatterpolar(
                r=avg_scores,
                theta=categories,
                fill='toself',
                name='Average Performance'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="Performance by Test Type"
            )
            
            st.plotly_chart(fig, use_container_width=True, key="progress_test_type_radar_chart")
        
        # Show detailed table
        st.subheader("Detailed Performance by Test Type")
        st.dataframe(type_stats, use_container_width=True)
    
    @staticmethod
    def show_improvement_trend():
        """Show improvement trend over time"""
        df = ScoreTracker.get_performance_history()
        
        if len(df) < 2:
            st.info("Need at least 2 test sessions to show improvement trend.")
            return
        
        # Calculate rolling average
        df_sorted = df.sort_values('timestamp')
        df_sorted['rolling_avg'] = df_sorted['score'].rolling(window=3, min_periods=1).mean()
        
        # Create trend chart
        fig = go.Figure()
        
        # Add individual scores
        fig.add_trace(go.Scatter(
            x=df_sorted['timestamp'],
            y=df_sorted['score'],
            mode='markers',
            name='Individual Scores',
            marker=dict(color='lightblue', size=6)
        ))
        
        # Add rolling average
        fig.add_trace(go.Scatter(
            x=df_sorted['timestamp'],
            y=df_sorted['rolling_avg'],
            mode='lines',
            name='3-Test Average',
            line=dict(color='red', width=3)
        ))
        
        fig.update_layout(
            title="Performance Trend with Moving Average",
            xaxis_title="Date & Time",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True, key="progress_improvement_trend_chart")
        
        # Calculate improvement
        first_avg = df_sorted.iloc[0]['score']
        last_avg = df_sorted.iloc[-1]['score']
        improvement = ((last_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
        
        if improvement > 0:
            st.success(f"📈 Improvement: {improvement:+.1f}%")
        elif improvement < 0:
            st.error(f"📉 Decline: {improvement:+.1f}%")
        else:
            st.info("📊 No change in performance")
    
    @staticmethod
    def show_detailed_session_view(session_id: str):
        """Show detailed view of a specific session"""
        session = ScoreTracker.get_session_details(session_id)
        
        if not session:
            st.error("Session not found.")
            return
        
        # Session overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Test Type", session['test_type'])
        with col2:
            st.metric("Average Score", f"{session.get('average_score', 0)*100:.1f}%")
        with col3:
            st.metric("Total Questions", len(session['scores']))
        
        # Detailed results
        if session['details']:
            st.subheader("Detailed Results")
            
            # Create detailed table
            details_df = pd.DataFrame(session['details'])
            
            if 'plate_number' in details_df.columns:
                # Ishihara test specific view
                details_df['Result'] = details_df['is_correct'].apply(
                    lambda x: '✅ Correct' if x else '❌ Incorrect'
                )
                
                st.dataframe(
                    details_df[['plate_number', 'shown_value', 'user_answer', 'Result']],
                    use_container_width=True
                )
            else:
                # General test view
                st.dataframe(details_df, use_container_width=True)
        
        # Score distribution
        if len(session['scores']) > 1:
            st.subheader("Score Distribution")
            
            scores = [s['score'] * 100 for s in session['scores']]
            
            fig = go.Figure(data=[
                go.Histogram(x=scores, nbinsx=10, marker_color='lightblue')
            ])
            
            fig.update_layout(
                title="Score Distribution in This Session",
                xaxis_title="Score (%)",
                yaxis_title="Frequency"
            )
            
            st.plotly_chart(fig, use_container_width=True, key="session_score_distribution_histogram")
