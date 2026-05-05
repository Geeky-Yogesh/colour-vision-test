import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime
from .tritan_logic import TritanLogic
from ..performance_tracker.score_tracker import ScoreTracker

def tritan_test_page():
    st.title("💠 Tritan (Blue-Yellow) Test")
    st.markdown("This test screens for Tritanopia using specific blue-yellow confusion colors.")
    
    # --- 1. INITIALIZE TRACKING ---
    ScoreTracker.initialize_session()
    if 'tritan_round' not in st.session_state or st.session_state.tritan_round == 0:
        if st.session_state.get('tritan_round', 0) == 0:
            ScoreTracker.start_session("Tritan (Blue-Yellow)")

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
        st.session_state.tritan_shown.append(random.randint(1, 99))
    
    target = st.session_state.tritan_shown[curr]
    bg_dots, num_dots = TritanLogic.get_plate(target)
    
    fig = go.Figure()
    for dots in [bg_dots, num_dots]:
        x, y, s, c = zip(*dots)
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=s, color=c, line=dict(width=0)), hoverinfo='none'))

    fig.update_layout(
        width=500, height=500, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        yaxis=dict(
            visible=False, 
            range=[0, 100], 
            fixedrange=True, 
            scaleanchor="x", # This keeps the circle perfectly round
            scaleratio=1
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, config={'displayModeBar': False})

    with st.form(key=f"tr_form_{curr}"):
        ans = st.text_input("Enter the number you see:", key=f"tr_input_{curr}")
        if st.form_submit_button("Submit"):
            # --- 2. RECORD INDIVIDUAL PLATE ---
            target = st.session_state.tritan_shown[curr]
            is_correct = str(ans).strip() == str(target).strip()
            
            ScoreTracker.add_plate_result(
                plate_number=curr + 1,
                shown_value=str(target),
                user_answer=str(ans),
                is_correct=is_correct
            )
            
            st.session_state.tritan_answers.append(ans)
            st.session_state.tritan_round += 1
            st.rerun()

def show_results(total):
    # Calculate accuracy for display
    correct = sum(1 for s, a in zip(st.session_state.tritan_shown, st.session_state.tritan_answers) if str(s) == str(a))
    accuracy = (correct / total) * 100
    diagnosis = "Normal" if accuracy >= 80 else "Deficient"
    
    st.success("🎉 Test Completed!")
    st.metric("Tritan Accuracy", f"{accuracy:.1f}%")
    
    # Detailed Results
    st.write("### 📊 Test Results Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Correct Answers:** {correct}/{total}")
        st.write(f"**Accuracy:** {accuracy:.1f}%")
        st.write(f"**Diagnosis:** {diagnosis}")
    
    with col2:
        if diagnosis == "Normal":
            st.success("✅ Normal Colour Vision")
        else:
            st.warning("⚠️ Tritan Deficiency Detected")
    
    # Show detailed results
    st.write("### 📋 Detailed Results")
    results_df = []
    for i, (shown, answer) in enumerate(zip(st.session_state.tritan_shown, st.session_state.tritan_answers)):
        is_correct = str(shown) == str(answer)
        results_df.append({
            "Plate": i + 1,
            "Shown": shown,
            "Your Answer": answer,
            "Correct": "✅" if is_correct else "❌"
        })
    
    import pandas as pd
    df = pd.DataFrame(results_df)
    st.dataframe(df, width='stretch')
    
    # --- 3. SAVE TO HISTORY AND END SESSION ---
    if not st.session_state.tritan_results_saved:
        st.session_state.test_results.append({
            "test_type": "Tritan (Blue-Yellow)",
            "result": diagnosis,
            "score": f"{accuracy:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        ScoreTracker.end_session() # This finalizes all the plates we added
        st.session_state.tritan_results_saved = True

    if st.button("Finish and Back to Menu"):
        st.session_state.tritan_round = 0
        st.session_state.tritan_results_saved = False
        st.session_state.current_test = None
        st.rerun()
