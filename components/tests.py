import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime
from .colour_vision_test import ColourVisionTest

def ishihara_test():
    """Ishihara test with dynamic random numbers and high-density rendering"""
    st.title("🔢 Random Ishihara Plates Test")
    
    # Configuration
    TOTAL_ROUNDS = 8 
    
    # 1. Check if test is finished
    if st.session_state.ishihara_current_round >= TOTAL_ROUNDS:
        show_random_ishihara_results(TOTAL_ROUNDS)
        return

    curr_round = st.session_state.ishihara_current_round
    
    # 2. Progress UI
    st.progress((curr_round + 1) / TOTAL_ROUNDS)
    st.write(f"### Plate {curr_round + 1} of {TOTAL_ROUNDS}")

    # 3. Generate Random Number for this round (if not already generated)
    if len(st.session_state.ishihara_shown_values) <= curr_round:
        # Generate a random number 1-99
        target_num = random.randint(1, 99)
        st.session_state.ishihara_shown_values.append(target_num)
    
    target_number = st.session_state.ishihara_shown_values[curr_round]

    # 4. Generate the High-Density Dot Pattern
    bg_dots, num_dots = ColourVisionTest.create_dot_pattern(target_number)
    
    fig = go.Figure()

    # Draw Background Trace
    bx, by, bs, bc = zip(*bg_dots)
    fig.add_trace(go.Scatter(
        x=bx, y=by, mode='markers', 
        marker=dict(size=bs, color=bc, line=dict(width=0)), 
        hoverinfo='none'
    ))
    
    # Draw Number Trace
    nx, ny, ns, nc = zip(*num_dots)
    fig.add_trace(go.Scatter(
        x=nx, y=ny, mode='markers', 
        marker=dict(size=ns, color=nc, line=dict(width=0)), 
        hoverinfo='none'
    ))
    
    # 5. Fixed Layout to remove distortion and white space
    fig.update_layout(
        width=500, height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    # Display the plate
    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=False)

    # 6. Input Form
    with st.form(key=f"ishihara_round_{curr_round}"):
        st.write("What number is hidden in the plate?")
        user_input = st.text_input("Enter number:", key=f"input_{curr_round}", placeholder="e.g. 12")
        
        col1, col2 = st.columns(2)
        if col1.form_submit_button("Submit & Next", width='stretch'):
            st.session_state.ishihara_answers.append(user_input)
            st.session_state.ishihara_current_round += 1
            st.rerun()
            
        if col2.form_submit_button("I can't see a number", width='stretch'):
            st.session_state.ishihara_answers.append("None")
            st.session_state.ishihara_current_round += 1
            st.rerun()

    if st.button("Reset Test"):
        st.session_state.ishihara_current_round = 0
        st.session_state.ishihara_answers = []
        st.session_state.ishihara_shown_values = []
        st.rerun()

def show_random_ishihara_results(total_rounds):
    """Calculate and display results for the random test"""
    st.subheader(" Test Summary")
    
    shown = st.session_state.ishihara_shown_values
    answers = st.session_state.ishihara_answers
    
    correct_count = 0
    detailed_data = []
    
    for i in range(len(answers)):
        u_ans = str(answers[i]).strip()
        s_val = str(shown[i]).strip()
        
        # Robust comparison (int comparison to handle '08' vs '8')
        is_match = False
        try:
            if int(u_ans) == int(s_val):
                is_match = True
        except ValueError:
            if u_ans.lower() == s_val.lower():
                is_match = True
                
        if is_match:
            correct_count += 1
            
        detailed_data.append({
            "Plate": i + 1,
            "Shown": s_val,
            "Your Answer": u_ans if u_ans else "(blank)",
            "Status": " Correct" if is_match else " Incorrect"
        })

    accuracy = (correct_count / total_rounds) * 100
    
    # Visual metrics
    col1, col2 = st.columns(2)
    col1.metric("Correct Answers", f"{correct_count} / {total_rounds}")
    col2.metric("Accuracy", f"{accuracy:.1f}%")

    # Diagnosis logic
    if accuracy >= 85:
        diagnosis = "Normal Colour Vision"
        st.success(f"Result: {diagnosis}")
    elif accuracy >= 60:
        diagnosis = "Mild Colour Vision Deficiency"
        st.warning(f"Result: {diagnosis}")
    else:
        diagnosis = "Significant Colour Vision Deficiency"
        st.error(f"Result: {diagnosis}")

    # Detailed Table
    st.table(detailed_data)

    # Save to session history (only once)
    if not st.session_state.results_saved:
        st.session_state.test_results.append({
            "test_type": "Random Ishihara",
            "result": diagnosis,
            "score": f"{accuracy:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.session_state.results_saved = True

    if st.button("Finish and Back to Menu"):
        st.session_state.ishihara_current_round = 0
        st.session_state.ishihara_answers = []
        st.session_state.ishihara_shown_values = []
        st.session_state.results_saved = False
        st.session_state.current_test = None
        st.session_state.test_results = []
        st.rerun()
