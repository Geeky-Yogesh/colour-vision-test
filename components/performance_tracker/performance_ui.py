"""
Performance UI Module - User interface for performance tracking features
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from .score_tracker import ScoreTracker
from .progress_visualizer import ProgressVisualizer
from .result_interpreter import ResultInterpreter

class PerformanceUI:
    """Handle UI components for performance tracking"""
    
    @staticmethod
    def show_performance_dashboard():
        """Show main performance dashboard"""
        st.title("📊 Performance Tracking Dashboard")
        st.markdown("---")
        
        # Initialize tracker if needed
        from .score_tracker import ScoreTracker
        ScoreTracker.initialize_session()
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview", "📊 Progress Charts", 
            "🔍 Session Details", "📋 Interpretation", "📤 Export"
        ])
        
        with tab1:
            PerformanceUI.show_overview_tab()
        
        with tab2:
            PerformanceUI.show_progress_charts_tab()
        
        with tab3:
            PerformanceUI.show_session_details_tab()
        
        with tab4:
            PerformanceUI.show_interpretation_tab()
        
        with tab5:
            PerformanceUI.show_export_tab()
    
    @staticmethod
    def show_overview_tab():
        """Show overview tab with key metrics"""
        from .progress_visualizer import ProgressVisualizer
        from .result_interpreter import ResultInterpreter
        
        st.subheader("Performance Overview")
        
        # Key metrics
        ProgressVisualizer.show_progress_overview()
        
        st.markdown("---")
        
        # Overall interpretation
        overall = ResultInterpreter.interpret_overall_performance()
        
        if overall['status'] != 'no_data':
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Overall Assessment")
                ResultInterpreter.show_interpretation_result(overall)
            
            with col2:
                st.subheader("Quick Stats")
                st.metric("Best Score", f"{overall['best_score']:.1f}%")
                st.metric("Average", f"{overall['average_score']:.1f}%")
                st.metric("Total Tests", overall['total_tests'])
        else:
            st.info("No test data available yet. Complete some tests to see your performance analysis!")
        
        # Recent performance
        st.subheader("Recent Performance")
        ProgressVisualizer.show_overview_score_chart()
    
    @staticmethod
    def show_progress_charts_tab():
        """Show progress charts and visualizations"""
        from .progress_visualizer import ProgressVisualizer
        
        st.subheader("Progress Visualizations")
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select Chart Type:",
            ["Score Progress", "Session Comparison", "Test Type Performance", "Improvement Trend"]
        )
        
        if chart_type == "Score Progress":
            ProgressVisualizer.show_score_progress_chart()
        elif chart_type == "Session Comparison":
            ProgressVisualizer.show_session_comparison()
        elif chart_type == "Test Type Performance":
            ProgressVisualizer.show_test_type_performance()
        elif chart_type == "Improvement Trend":
            ProgressVisualizer.show_improvement_trend()
    
    @staticmethod
    def show_session_details_tab():
        """Show detailed session information"""
        from .score_tracker import ScoreTracker
        from .progress_visualizer import ProgressVisualizer
        
        st.subheader("Session Details")
        
        # Session selection
        data = st.session_state.performance_data
        completed_sessions = [s for s in data['sessions'] if s['completed']]
        
        if not completed_sessions:
            st.info("No completed sessions available.")
            return
        
        # Create session selector
        session_options = {
            f"Session {i+1} ({s['test_type']})": s['session_id'] 
            for i, s in enumerate(completed_sessions)
        }
        
        selected_session_label = st.selectbox(
            "Select Session:",
            list(session_options.keys())
        )
        
        if selected_session_label:
            session_id = session_options[selected_session_label]
            ProgressVisualizer.show_detailed_session_view(session_id)
    
    @staticmethod
    def show_interpretation_tab():
        """Show result interpretation and recommendations"""
        from .result_interpreter import ResultInterpreter
        
        st.subheader("Performance Interpretation")
        
        # Overall interpretation
        overall = ResultInterpreter.interpret_overall_performance()
        
        if overall['status'] != 'no_data':
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("### Overall Assessment")
                ResultInterpreter.show_interpretation_result(overall)
            
            with col2:
                st.write("### Performance Level")
                
                # Performance gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = overall['average_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Average Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': overall['color']},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 70], 'color': "gray"},
                            {'range': [70, 85], 'color': "lightblue"},
                            {'range': [85, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True, key="performance_gauge_chart")
        
        # Improvement suggestions
        st.write("### Personalized Recommendations")
        suggestions = ResultInterpreter.get_improvement_suggestions(overall)
        
        if suggestions:
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.info("Complete more tests to get personalized recommendations.")
    
    @staticmethod
    def show_export_tab():
        """Show export options"""
        from .score_tracker import ScoreTracker
        from .result_interpreter import ResultInterpreter
        
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Export Format")
            export_format = st.selectbox(
                "Choose Format:",
                ["CSV Data", "Performance Report", "JSON Data"]
            )
            
            if st.button("Generate Export"):
                if export_format == "CSV Data":
                    csv_data = ScoreTracker.export_data()
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"colour_vision_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                elif export_format == "Performance Report":
                    report = ResultInterpreter.generate_performance_report()
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                elif export_format == "JSON Data":
                    import json
                    json_data = json.dumps(
                        st.session_state.performance_data, 
                        indent=2, 
                        default=str
                    )
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"performance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        
        with col2:
            st.write("### Data Management")
            
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.confirm("Are you sure you want to clear all performance data? This cannot be undone."):
                    ScoreTracker.clear_all_data()
                    st.success("All performance data cleared.")
                    st.rerun()
            
            # Data summary
            data = st.session_state.performance_data
            st.write(f"""
            **Current Data Summary:**
            - Total Sessions: {len(data['sessions'])}
            - Completed Sessions: {len([s for s in data['sessions'] if s['completed']])}
            - Total Tests: {data['total_tests']}
            - Data Size: ~{len(str(data))} characters
            """)
    
    @staticmethod
    def show_quick_stats():
        """Show quick performance stats in sidebar"""
        from .result_interpreter import ResultInterpreter
        
        data = st.session_state.performance_data
        
        if data['total_tests'] > 0:
            overall = ResultInterpreter.interpret_overall_performance()
            
            st.metric("Avg Score", f"{data['average_score']:.1f}%")
            st.metric("Best Score", f"{data['best_score']:.1f}%")
            st.metric("Total Tests", data['total_tests'])
            
            # Status indicator
            if overall['color'] == 'green':
                st.success("🌟 Excellent")
            elif overall['color'] == 'blue':
                st.info("👍 Good")
            elif overall['color'] == 'orange':
                st.warning("📊 Moderate")
            else:
                st.error("📈 Needs Work")
        else:
            st.info("No data yet")
    
    @staticmethod
    def show_navigation_buttons():
        """Show navigation buttons"""
        col1, col2 = st.columns(2)
        
        if col1.button(" Back to Menu"):
            st.session_state.current_test = None
            st.rerun()
        
        if col2.button(" Refresh Data"):
            st.rerun()
