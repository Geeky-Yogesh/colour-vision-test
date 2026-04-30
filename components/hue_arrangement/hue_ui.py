import streamlit as st
from streamlit_sortables import sort_items
from datetime import datetime
from .hue_logic import HueLogic
from ..performance_tracker.score_tracker import ScoreTracker

def hue_arrangement_page():
    st.title("🌈 Hue Arrangement Test")
    st.markdown("""
    **Instructions:** 
    1. Look at the two fixed **Anchor** colors at the ends.
    2. Drag and drop the colored blocks in the middle to create a perfectly smooth color transition.
    3. Click **Submit** when you are satisfied with the gradient.
    """)

    # Initialize Session State
    if 'hue_test_caps' not in st.session_state:
        full_spectrum = HueLogic.generate_spectrum(12) # 12 caps for a quick test
        st.session_state.hue_correct_order = full_spectrum.copy()
        
        # Fix the anchors (first and last)
        anchors = [full_spectrum[0], full_spectrum[-1]]
        middle_part = full_spectrum[1:-1]
        random_middle = middle_part.copy()
        import random
        random.shuffle(random_middle)
        
        # Current state is [Start Anchor] + [Shuffled] + [End Anchor]
        st.session_state.hue_test_caps = [full_spectrum[0]] + random_middle + [full_spectrum[-1]]
        st.session_state.hue_test_submitted = False

    # Render Anchors
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="background-color:{st.session_state.hue_correct_order[0]['hex']}; 
            padding:15px; border-radius:5px; text-align:center; color:white; font-weight:bold; border:2px solid white;">
            START ANCHOR
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="background-color:{st.session_state.hue_correct_order[-1]['hex']}; 
            padding:15px; border-radius:5px; text-align:center; color:white; font-weight:bold; border:2px solid white;">
            END ANCHOR
            </div>""", unsafe_allow_html=True)

    st.write("")

    # Prepare items for the Sortable Component
    # streamlit-sortables expects a list of strings
    sortable_items = [
        f"Cap {cap['id']}" 
        for cap in st.session_state.hue_test_caps
    ]

    # Display Sortable UI (Horizontal layout)
    sorted_data = sort_items(sortable_items, direction="horizontal", key="hue_sortable_tray")

    # Display the actual color blocks below the sortable items
    st.write("**Current Arrangement:**")
    color_cols = st.columns(len(st.session_state.hue_test_caps))
    for i, item in enumerate(sorted_data):
        # Extract cap ID from the string format
        cap_id = int(item.split()[1])
        cap = next(c for c in st.session_state.hue_test_caps if c['id'] == cap_id)
        with color_cols[i]:
            st.markdown(f"""
                <div style='background-color:{cap['hex']}; height:50px; width:100%; border-radius:5px; border:1px solid #ddd;'></div>
                <small>Cap {cap_id}</small>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    btn_col1, btn_col2, btn_col3 = st.columns([1,1,1])
    
    if btn_col1.button("🚀 Submit Arrangement", use_container_width=True):
        # Reconstruct the final order based on user sorting
        final_ids = [int(item.split()[1]) for item in sorted_data]
        user_final_order = []
        for fid in final_ids:
            cap = next(c for c in st.session_state.hue_correct_order if c['id'] == fid)
            user_final_order.append(cap)
        
        # Calculate Scores
        tes, accuracy = HueLogic.calculate_score(user_final_order, st.session_state.hue_correct_order)
        
        # Show Results
        if accuracy >= 90:
            st.success(f"**Excellent Vision!** Your accuracy is {accuracy:.1f}% (TES: {tes})")
        elif accuracy >= 75:
            st.info(f"**Good Vision.** Your accuracy is {accuracy:.1f}% (TES: {tes})")
        else:
            st.error(f"**Deficiency Detected.** Accuracy: {accuracy:.1f}% (TES: {tes})")
            st.info("Large errors in hue arrangement often indicate difficulty distinguishing specific color frequencies.")

        # Update Performance Tracker
        ScoreTracker.initialize_session()
        ScoreTracker.start_session("Hue Arrangement")
        ScoreTracker.add_score(accuracy / 100, {"tes": tes})
        ScoreTracker.end_session()
        
        # Log to Results history
        st.session_state.test_results.append({
            "test_type": "Hue Arrangement",
            "result": f"TES: {tes}",
            "score": f"{accuracy:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.session_state.hue_test_submitted = True

    if btn_col2.button("🔄 Reset Test", use_container_width=True):
        if 'hue_test_caps' in st.session_state:
            del st.session_state.hue_test_caps
        st.rerun()
        
    if btn_col3.button("🏠 Exit to Menu", use_container_width=True):
        st.session_state.current_test = None
        st.rerun()
