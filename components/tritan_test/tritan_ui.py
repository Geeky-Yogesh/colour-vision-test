import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime
from .tritan_logic import TritanLogic
from ..performance_tracker.score_tracker import ScoreTracker

def tritan_test_page():
    st.title("💠 Tritan (Blue-Yellow) Test")
    st.markdown("This test screens for Tritanopia using specific blue-yellow confusion colors.")

    TOTAL_ROUNDS = 6
    
    if 'tritan_round' not in st.session_state:
        st.session_state.tritan_round, st.session_state.tritan_shown, st.session_state.tritan_answers = 0, [], []

    if st.session_state.tritan_round >= TOTAL_ROUNDS:
        show_results(TOTAL_ROUNDS)
        return

    curr = st.session_state.tritan_round
    st.progress((curr + 1) / TOTAL_ROUNDS)
    st.write(f"### Plate {curr + 1} of {TOTAL_ROUNDS}")

    if len(st.session_state.tritan_shown) <= curr:
        st.session_state.tritan_shown.append(random.randint(1, 9))
    
    target = st.session_state.tritan_shown[curr]
    bg_dots, num_dots = TritanLogic.get_plate(target)
    
    fig = go.Figure()
    for dots in [bg_dots, num_dots]:
        x, y, s, c = zip(*dots)
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=s, color=c, line=dict(width=0)), hoverinfo='none'))

    fig.update_layout(
        width=500, height=500, showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        # FIX FOR BULGING:
        yaxis=dict(visible=False, range=[0, 100], fixedrange=True, scaleanchor="x", scaleratio=1), 
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, config={'displayModeBar': False})

    with st.form(key=f"tr_form_{curr}"):
        ans = st.text_input("Enter the number you see:", key=f"tr_input_{curr}")
        if st.form_submit_button("Submit"):
            st.session_state.tritan_answers.append(ans)
            st.session_state.tritan_round += 1
            st.rerun()

def show_results(total):
    correct = sum(1 for s, a in zip(st.session_state.tritan_shown, st.session_state.tritan_answers) if str(s) == str(a))
    accuracy = (correct / total) * 100
    diagnosis = "Normal" if accuracy >= 80 else "Deficient"
    
    st.metric("Tritan Accuracy", f"{accuracy:.1f}%")
    
    # --- NEW SAVING LOGIC (Outside the button) ---
    if not st.session_state.tritan_results_saved:
        # 1. Update Global Results History
        st.session_state.test_results.append({
            "test_type": "Tritan (Blue-Yellow)",
            "result": diagnosis,
            "score": f"{accuracy:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # 2. Update Performance Tracker (ScoreTracker)
        ScoreTracker.initialize_session()
        ScoreTracker.start_session("Tritan (Blue-Yellow)")
        # Record the overall accuracy (as 0.0 to 1.0)
        ScoreTracker.add_score(accuracy / 100, {"diagnosis": diagnosis})
        ScoreTracker.end_session()
        
        st.session_state.tritan_results_saved = True
    # ----------------------------------------------

    if st.button("Finish and Back to Menu"):
        # Reset Tritan state for next time
        st.session_state.tritan_round = 0
        st.session_state.tritan_shown = []
        st.session_state.tritan_answers = []
        st.session_state.tritan_results_saved = False # Reset flag
        st.session_state.current_test = None
        st.rerun()
