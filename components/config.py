"""
Configuration and session state management
"""

import streamlit as st

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Colour Vision Test",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def init_session_state():
    """Initialize session state variables"""
    if 'current_test' not in st.session_state:
        st.session_state.current_test = None
    if 'ishihara_answers' not in st.session_state:
        st.session_state.ishihara_answers = []
    if 'ishihara_random_plates' not in st.session_state:
        st.session_state.ishihara_random_plates = []
    if 'ishihara_current_index' not in st.session_state:
        st.session_state.ishihara_current_index = 0
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    
    # New variables for random ishihara test
    if 'ishihara_current_round' not in st.session_state:
        st.session_state.ishihara_current_round = 0
    if 'ishihara_shown_values' not in st.session_state:
        st.session_state.ishihara_shown_values = []
    if 'results_saved' not in st.session_state:
        st.session_state.results_saved = False
