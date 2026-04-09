"""
Performance Tracker Main Module - Entry point for performance tracking features
"""

import streamlit as st
from .performance_ui import PerformanceUI
from .score_tracker import ScoreTracker

def show_performance_tracker():
    """Main performance tracking interface"""
    PerformanceUI.show_performance_dashboard()
    
    # Navigation buttons
    PerformanceUI.show_navigation_buttons()
