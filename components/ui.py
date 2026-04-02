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
        if st.button("🔢 Ishihara Plates Test", width='stretch', type="primary"):
            st.session_state.current_test = "ishihara"
            st.session_state.ishihara_current_index = 0
            st.session_state.ishihara_answers = []
            # Generate new random order
            import random
            all_plates = list(range(8))
            st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
            st.rerun()
    
    with col2:
        if st.button("📊 View Results", width='stretch'):
            st.session_state.current_test = "results"
            st.rerun()
    
    # Information
    st.markdown("---")
    st.markdown("### About Colour Vision Tests")
    
    st.markdown("""
    **Ishihara Plates Test:**
    - Identifies red-green colour blindness
    - Uses dot patterns with hidden numbers
    - Quick screening test (8 plates)
    
    This test helps detect common forms of colour vision deficiency by presenting 
    patterns of colored dots that form numbers visible to people with normal colour vision 
    but difficult or impossible to see for those with colour blindness.
    """)
    
    st.warning("""
    **Disclaimer:** This application is for educational and screening purposes only. 
    It is not a substitute for professional medical diagnosis. 
    Consult an eye care professional for accurate assessment.
    """)
