"""
Colour Vision Test Application
Main Streamlit Application with Sidebar Navigation
"""

import streamlit as st
from components.ui import main_menu
from components.tests import ishihara_test
from components.results import show_results
from components.config import configure_page

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_test' not in st.session_state:
        st.session_state.current_test = None
    
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    
    if 'ishihara_answers' not in st.session_state:
        st.session_state.ishihara_answers = []
    
    if 'ishihara_random_plates' not in st.session_state:
        st.session_state.ishihara_random_plates = []
    
    if 'ishihara_current_index' not in st.session_state:
        st.session_state.ishihara_current_index = 0

def sidebar_navigation():
    """Create sidebar navigation"""
    with st.sidebar:
        st.title("🎨 Navigation")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_test = None
            st.rerun()
        
        if st.button("🔢 Ishihara Test", use_container_width=True):
            st.session_state.current_test = "ishihara"
            st.session_state.ishihara_current_index = 0
            st.session_state.ishihara_answers = []
            # Generate new random order
            import random
            all_plates = list(range(8))
            st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
            st.rerun()
        
        if st.button("📊 Results", use_container_width=True):
            st.session_state.current_test = "results"
            st.rerun()
        
        st.markdown("---")
        
        # Session info
        st.subheader("📋 Session Info")
        st.info(f"""
        **Current Test:** {st.session_state.current_test or 'None'}
        
        **Tests Completed:** {len(st.session_state.test_results)}
        """)
        
        # Clear session button
        if st.button("🗑️ Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_session_state()
            st.rerun()
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        **Colour Vision Test App**
        
        This application provides:
        - Ishihara Plates Test
        - Results tracking
        
        **Version:** 1.0.0
        
        ---
        *For educational purposes only*
        """)

def main():
    """Main application logic"""
    # Configure page settings
    configure_page()
    
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar navigation
    sidebar_navigation()
    
    # Main content area
    if st.session_state.current_test is None:
        main_menu()
    elif st.session_state.current_test == "ishihara":
        ishihara_test()
    elif st.session_state.current_test == "results":
        show_results()
    else:
        st.error("Unknown test type")
        st.session_state.current_test = None
        st.rerun()

if __name__ == "__main__":
    main()
