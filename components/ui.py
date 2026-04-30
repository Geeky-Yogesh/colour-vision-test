"""
UI Components - Main Menu and Navigation
"""

import streamlit as st

def main_menu():
    """Display main menu"""
    st.title("🎨 Colour Vision Test")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔢 Ishihara Plates Test", width='stretch', type="primary", key="menu_ishihara"):
            st.session_state.current_test = "ishihara"
            st.session_state.ishihara_current_index = 0
            st.session_state.ishihara_answers = []
            # Generate new random order
            import random
            all_plates = list(range(8))
            st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
            st.rerun()
    
    with col2:
        if st.button("📊 Performance Tracker", width='stretch', key="menu_performance_main"):
            st.session_state.current_test = "performance"
            st.rerun()
    
    # Additional options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌈 Hue Arrangement Test", width='stretch', key="menu_hue"):
            st.session_state.current_test = "hue_arrangement"
            st.rerun()
    
    with col2:
        if st.button("📈 View Results", width='stretch', key="menu_results"):
            st.session_state.current_test = "results"
            st.rerun()
    
    # Third row for additional options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚙️ Distance Settings", width='stretch', key="menu_distance"):
            st.session_state.current_test = "distance"
            st.rerun()
    
    with col2:
        if st.button("📊 Performance Tracker", width='stretch', key="menu_performance_alt"):
            st.session_state.current_test = "performance"
            st.rerun()
    
    # Information
    st.markdown("---")
    st.markdown("### About Colour Vision Tests")
    
    st.markdown("""
    **Ishihara Plates Test:**
    - Identifies red-green colour blindness
    - Uses dot patterns with hidden numbers
    - Quick screening test (8 plates)
    
    **Performance Tracker:**
    - Detailed analytics of test results
    - Progress monitoring over time
    - Personalized recommendations
    
    This test helps detect common forms of colour vision deficiency by presenting 
    patterns of colored dots that form numbers visible to people with normal colour vision 
    but difficult or impossible to see for those with colour blindness.
    """)
    
    st.warning("""
    **Disclaimer:** This application is for educational and screening purposes only. 
    It is not a substitute for professional medical diagnosis. 
    Consult an eye care professional for accurate assessment.
    """)
