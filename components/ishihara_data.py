"""
Ishihara Plate Data - Real Test Standards
"""

ISHIHARA_PLATES = [
    {
        "plate_number": 0,
        "description": "Plate 1: Number 12",
        "correct_answer": "12",
        "type": "normal",
        "protanopia_answer": "12",
        "deuteranopia_answer": "12"
    },
    {
        "plate_number": 1,
        "description": "Plate 2: Number 8",
        "correct_answer": "8",
        "type": "normal",
        "protanopia_answer": "3",
        "deuteranopia_answer": "3"
    },
    {
        "plate_number": 2,
        "description": "Plate 3: Number 29",
        "correct_answer": "29",
        "type": "normal",
        "protanopia_answer": "70",
        "deuteranopia_answer": "70"
    },
    {
        "plate_number": 3,
        "description": "Plate 4: Number 5",
        "correct_answer": "5",
        "type": "normal",
        "protanopia_answer": "2",
        "deuteranopia_answer": "2"
    },
    {
        "plate_number": 4,
        "description": "Plate 5: Number 3",
        "correct_answer": "3",
        "type": "transformation",
        "protanopia_answer": "X",
        "deuteranopia_answer": "X"
    },
    {
        "plate_number": 5,
        "description": "Plate 6: Number 15",
        "correct_answer": "15",
        "type": "normal",
        "protanopia_answer": "17",
        "deuteranopia_answer": "17"
    },
    {
        "plate_number": 6,
        "description": "Plate 7: Number 74",
        "correct_answer": "74",
        "type": "normal",
        "protanopia_answer": "21",
        "deuteranopia_answer": "21"
    },
    {
        "plate_number": 7,
        "description": "Plate 8: Number 6",
        "correct_answer": "6",
        "type": "transformation",
        "protanopia_answer": "X",
        "deuteranopia_answer": "X"
    }
]

def get_plate_data(plate_number):
    """Get plate data by number"""
    if 0 <= plate_number < len(ISHIHARA_PLATES):
        return ISHIHARA_PLATES[plate_number]
    return ISHIHARA_PLATES[0]

def analyze_results(answers):
    """Analyze Ishihara test results based on real standards"""
    if len(answers) != len(ISHIHARA_PLATES):
        return None
    
    correct_count = 0
    detailed_results = []
    
    for i, answer in enumerate(answers):
        plate_data = ISHIHARA_PLATES[i]
        correct_answer = plate_data["correct_answer"]
        is_correct = answer.strip() == correct_answer
        
        if is_correct:
            correct_count += 1
        
        detailed_results.append({
            "Plate": i + 1,
            "Your Answer": answer if answer else "(skipped)",
            "Correct Answer": correct_answer,
            "Result": "✓" if is_correct else "✗"
        })
    
    total_count = len(ISHIHARA_PLATES)
    percentage = (correct_count / total_count) * 100
    
    # Determine color vision type based on pattern of answers
    if percentage >= 80:
        result = "Normal Colour Vision"
    elif percentage >= 40:
        result = "Mild Colour Vision Deficiency"
    else:
        result = "Significant Colour Vision Deficiency"
    
    # More detailed analysis could be done here based on specific patterns
    # For now, we'll use the basic percentage-based classification
    
    return {
        "result": result,
        "percentage": percentage,
        "correct_count": correct_count,
        "total_count": total_count,
        "detailed_results": detailed_results
    }
