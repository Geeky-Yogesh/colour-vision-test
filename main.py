"""
Colour Vision Test Application
Main Streamlit Application with Sidebar Navigation
"""

import streamlit as st
from components.ui import main_menu
from components.tests import ishihara_test
from components.results import show_results
from components.webcam import webcam_test
from components.distance_guide import distance_settings_page
from components.performance_tracker import performance_tracker
from components.config import configure_page, init_session_state

def sidebar_navigation():
    """Create sidebar navigation"""
    with st.sidebar:
        st.title("🎨 Navigation")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", width='stretch'):
            st.session_state.current_test = None
            st.rerun()
        
        if st.button("🔢 Ishihara Test", width='stretch'):
            st.session_state.current_test = "ishihara"
            # Reset test state for new test
            st.session_state.ishihara_current_round = 0
            st.session_state.ishihara_answers = []
            st.session_state.ishihara_shown_values = []
            st.session_state.results_saved = False
            st.rerun()
        
        if st.button(" Results", width='stretch'):
            st.session_state.current_test = "results"
            st.rerun()
        
        if st.button(" Webcam Test", width='stretch'):
            st.session_state.current_test = "webcam"
            st.rerun()
        
        if st.button(" Distance Settings", width='stretch'):
            st.session_state.current_test = "distance"
            st.rerun()
        
        if st.button(" Performance Tracker", width='stretch'):
            st.session_state.current_test = "performance"
            st.rerun()
        
        st.markdown("---")
        
        # Session info
        st.subheader("")
        st.info(f"""
        **Current Test:** {st.session_state.current_test or 'None'}
        
        **Tests Completed:** {len(st.session_state.test_results)}
        """)
        
        # Clear session button
        if st.button("🗑️ Clear Session", width='stretch'):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_session_state()
            st.rerun()
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        **Colour Vision Test App**
        
        This application provides:
        - Random Ishihara Plates Test
        - Results tracking
        
        **Version:** 1.0.0
        
        ---
        *For educational purposes only*
        """)

def main():
    """Main application logic"""
    # Configure page settings
    configure_page()
    
    # Initialize session state using the proper function from config
    init_session_state()
    
    # Create sidebar navigation
    sidebar_navigation()
    
    # Main content area
    if st.session_state.current_test is None:
        main_menu()
    elif st.session_state.current_test == "ishihara":
        ishihara_test()
    elif st.session_state.current_test == "results":
        show_results()
    elif st.session_state.current_test == "webcam":
        webcam_test()
    elif st.session_state.current_test == "distance":
        distance_settings_page()
    elif st.session_state.current_test == "performance":
        performance_tracker.show_performance_tracker()
    else:
        st.error("Unknown test type")
        st.session_state.current_test = None
        st.rerun()

if __name__ == "__main__":
    main()
