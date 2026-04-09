"""
Ishihara Plate Data - Real Test Standards
"""

ISHIHARA_PLATES = [
    {"plate_number": 0, "description": "Plate 1: Number 12", "correct_answer": "12"},
    {"plate_number": 1, "description": "Plate 2: Number 8", "correct_answer": "8"},
    {"plate_number": 2, "description": "Plate 3: Number 29", "correct_answer": "29"},
    {"plate_number": 3, "description": "Plate 4: Number 5", "correct_answer": "5"},
    {"plate_number": 4, "description": "Plate 5: Number 3", "correct_answer": "3"},
    {"plate_number": 5, "description": "Plate 6: Number 15", "correct_answer": "15"},
    {"plate_number": 6, "description": "Plate 7: Number 74", "correct_answer": "74"},
    {"plate_number": 7, "description": "Plate 8: Number 6", "correct_answer": "6"}
]

def get_plate_data(plate_number):
    if 0 <= plate_number < len(ISHIHARA_PLATES):
        return ISHIHARA_PLATES[plate_number]
    return ISHIHARA_PLATES[0]

def analyze_results(answers):
    from .ishihara_data import ISHIHARA_PLATES
    correct_count = 0
    detailed = []
    
    for i in range(len(ISHIHARA_PLATES)):
        correct_ans = str(ISHIHARA_PLATES[i]["correct_answer"]).strip()
        user_ans = str(answers[i]).strip() if i < len(answers) else ""
        
        # Clean comparison
        is_match = False
        try:
            if int(user_ans) == int(correct_ans):
                is_match = True
        except:
            if user_ans == correct_ans:
                is_match = True
                
        if is_match: correct_count += 1
        detailed.append({
            "Plate": i+1,
            "You": user_ans,
            "Correct": correct_ans,
            "Result": "✅" if is_match else "❌"
        })
    
    perc = (correct_count / len(ISHIHARA_PLATES)) * 100
    return {
        "percentage": perc,
        "result": "Normal" if perc >= 85 else "Deficient",
        "detailed_results": detailed,
        "correct_count": correct_count,
        "total_count": len(ISHIHARA_PLATES)
    }
    