"""
Results Component - Test Results Display and Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_results():
    """Show all test results"""
    st.title("📊 Test Results")
    st.markdown("---")
    
    if not st.session_state.test_results:
        st.info("No test results yet. Complete a test to see results here.")
        if st.button("← Back to Menu"):
            st.session_state.current_test = None
            st.rerun()
        return
    
    # Summary statistics
    st.subheader("Summary")
    total_tests = len(st.session_state.test_results)
    ishihara_tests = len([r for r in st.session_state.test_results if r['test_type'] == 'Ishihara Plates'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tests", total_tests)
    with col2:
        st.metric("Ishihara Tests", ishihara_tests)
    
    # Results table
    st.subheader("All Results")
    df = pd.DataFrame(st.session_state.test_results)
    st.dataframe(df, width='stretch')
    
    # Results visualization
    if len(st.session_state.test_results) > 1:
        st.subheader("Results Over Time")
        
        # Create a chart of results
        results_df = pd.DataFrame(st.session_state.test_results)
        
        # Extract numeric scores
        scores = []
        for result in st.session_state.test_results:
            if 'percentage' in result:
                scores.append(result['percentage'])
            elif 'score' in result:
                scores.append(result['score'])
        
        if scores:
            fig = px.line(
                x=list(range(1, len(scores) + 1)),
                y=scores,
                title="Ishihara Test Scores Over Time",
                labels={"x": "Test Number", "y": "Score (%)"}
            )
            st.plotly_chart(fig, width='stretch')
    
    # Clear results button
    if st.button("🗑️ Clear All Results", type="secondary"):
        st.session_state.test_results = []
        st.rerun()
    
    # Back button
    if st.button("← Back to Menu"):
        st.session_state.current_test = None
        st.rerun()
