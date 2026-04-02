"""
Test Components - Ishihara 
Test Interface Components
"""

import streamlit as st
import plotly.graph_objects as go
from .colour_vision_test import ColourVisionTest
import os
from datetime import datetime

def ishihara_test():
    """Ishihara plates test"""
    st.title("🔢 Ishihara Plates Test")
    st.markdown("---")
    
    # Initialize random plates if not already done
    if 'ishihara_random_plates' not in st.session_state:
        import random
        all_plates = list(range(8))  # Plates 0-7
        st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
        st.session_state.ishihara_current_index = 0
    
    if st.session_state.ishihara_current_index >= 8:
        # Show results
        show_ishihara_results()
        return
    
    # Progress bar
    progress = (st.session_state.ishihara_current_index + 1) / 8
    st.progress(progress)
    st.write(f"Plate {st.session_state.ishihara_current_index + 1} of 8")
    
    # Get current random plate
    current_plate_num = st.session_state.ishihara_random_plates[st.session_state.ishihara_current_index]
    plate_info = ColourVisionTest.get_ishihara_plate(current_plate_num)
    st.subheader(plate_info["description"])
    
    # Create visual representation - try image first, fallback to generated pattern
    image_path = ColourVisionTest.get_ishihara_plate_image(current_plate_num)
    use_generated_pattern = False
    
    if image_path and os.path.exists(image_path):
        # Display actual image
        st.image(image_path, width=400, use_container_width=False)
    else:
        # Fallback to generated dot pattern
        use_generated_pattern = True
        background_dots, number_dots = ColourVisionTest.create_dot_pattern(current_plate_num)
    
    # Create scatter plot for the plate (only if using generated pattern)
    if use_generated_pattern:
        fig = go.Figure()
        
        # Add background dots
        if background_dots:
            bg_x, bg_y, bg_sizes, bg_colors = zip(*background_dots)
            fig.add_trace(go.Scatter(
                x=bg_x, y=bg_y,
                mode='markers',
                marker=dict(
                    size=bg_sizes,
                    color=bg_colors,
                    line=dict(width=0)
                ),
                name='Background',
                hoverinfo='none'
            ))
        
        # Add number dots
        if number_dots:
            num_x, num_y, num_sizes, num_colors = zip(*number_dots)
            fig.add_trace(go.Scatter(
                x=num_x, y=num_y,
                mode='markers',
                marker=dict(
                    size=num_sizes,
                    color=num_colors,
                    line=dict(width=0)
                ),
                name='Number',
                hoverinfo='none'
            ))
        
        fig.update_layout(
            width=400,
            height=400,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, width='content')
    
    # Answer input
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        answer = st.text_input("What number do you see?", key=f"answer_{st.session_state.ishihara_current_index}", max_chars=3)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Next", type="primary"):
                # Store answer with the actual plate number for correct analysis
                answer_entry = {
                    'plate_number': current_plate_num,
                    'answer': answer.strip()
                }
                st.session_state.ishihara_answers.append(answer_entry)
                st.session_state.ishihara_current_index += 1
                st.rerun()
        
        with col2:
            if st.button("Skip"):
                # Store skipped answer
                answer_entry = {
                    'plate_number': current_plate_num,
                    'answer': ""
                }
                st.session_state.ishihara_answers.append(answer_entry)
                st.session_state.ishihara_current_index += 1
                st.rerun()
        
        with col3:
            if st.button("Reset Test"):
                st.session_state.ishihara_current_index = 0
                st.session_state.ishihara_answers = []
                # Generate new random order
                import random
                all_plates = list(range(8))
                st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
                st.rerun()
    
    # Back button
    if st.button("← Back to Menu"):
        st.session_state.current_test = None
        st.rerun()

def show_ishihara_results():
    """Show Ishihara test results"""
    st.subheader("🎯 Test Results")
    
    # Convert answers back to simple list for analysis
    simple_answers = []
    for answer_entry in st.session_state.ishihara_answers:
        simple_answers.append(answer_entry['answer'])
    
    # Analyze results using real Ishihara data
    from .ishihara_data import analyze_results
    results = analyze_results(simple_answers)
    
    if not results:
        st.error("Error analyzing results")
        return
    
    # Display result
    result_color = "green" if "Normal" in results["result"] else "orange" if "Mild" in results["result"] else "red"
    st.markdown(f"### <span style='color: {result_color}'>{results['result']}</span>", unsafe_allow_html=True)
    
    # Score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{results['correct_count']}/{results['total_count']}")
    
    with col2:
        st.metric("Percentage", f"{results['percentage']:.1f}%")
    
    with col3:
        st.metric("Status", results["result"])
    
    # Detailed results with plate order info
    st.subheader("Detailed Results")
    detailed_with_order = []
    for i, (detail, answer_entry) in enumerate(zip(results["detailed_results"], st.session_state.ishihara_answers)):
        detail_with_order = detail.copy()
        detail_with_order["Plate Order"] = f"Plate {answer_entry['plate_number'] + 1}"
        detailed_with_order.append(detail_with_order)
    
    import pandas as pd
    df = pd.DataFrame(detailed_with_order)
    st.dataframe(df, width='stretch')
    
    # Save results
    result_entry = {
        "test_type": "Ishihara Plates",
        "result": results["result"],
        "percentage": results["percentage"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "details": f"{results['correct_count']}/{results['total_count']} correct"
    }
    st.session_state.test_results.append(result_entry)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Retake Test", type="primary"):
            st.session_state.ishihara_current_index = 0
            st.session_state.ishihara_answers = []
            # Generate new random order
            import random
            all_plates = list(range(8))
            st.session_state.ishihara_random_plates = random.sample(all_plates, 8)
            st.rerun()
    
    with col2:
        if st.button("← Back to Menu"):
            st.session_state.current_test = None
            st.rerun()
