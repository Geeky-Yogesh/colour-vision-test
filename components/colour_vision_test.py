"""
Colour Vision Test Core Logic
"""

import random
import colorsys
import os
from datetime import datetime
from .ishihara_data import get_plate_data

class ColourVisionTest:
    @staticmethod
    def get_ishihara_plate(plate_number):
        """Get real Ishihara plate data"""
        return get_plate_data(plate_number)
    
    @staticmethod
    def create_dot_pattern(plate_number):
        """Create realistic Ishihara-style dot pattern with coordinate correction"""
        import random
        
        # Get real plate data
        plate_data = get_plate_data(plate_number)
        number = plate_data["correct_answer"]
        
        # 1. Generate background dots
        background_dots = []
        for _ in range(500): 
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            size = random.uniform(1.5, 4.0)
            
            green_shades = [
                (46, 125, 50), (60, 179, 113), (85, 107, 47), 
                (34, 139, 34), (0, 128, 0), (50, 150, 50)
            ]
            color_rgb = random.choice(green_shades)
            color = '#%02x%02x%02x' % color_rgb
            background_dots.append((x, y, size, color))
        
        # 2. Generate number dots
        number_dots = []
        num_str = str(number)
        
        for i, digit in enumerate(num_str):
            offset_x = i * 35
            digit_positions = ColourVisionTest._create_digit_cluster(digit)
            
            for base_x, base_y in digit_positions:
                x = base_x + offset_x + random.uniform(-1, 1)
                
                # FIX: Flip the Y coordinate for Plotly's coordinate system
                # base_y is ~15 to ~60. 75 - base_y puts the digit in the top half of the 0-100 scale.
                y = (75 - base_y) + random.uniform(-1, 1)
                
                size = random.uniform(3.0, 5.5)
                
                red_shades = [
                    (255, 0, 0), (255, 69, 0), (220, 20, 60), 
                    (255, 140, 0), (255, 165, 0), (255, 99, 71)
                ]
                color_rgb = random.choice(red_shades)
                color = '#%02x%02x%02x' % color_rgb
                number_dots.append((x, y, size, color))
        
        return background_dots, number_dots
    
    @staticmethod
    def get_ishihara_plate_image(plate_number):
        """Get actual Ishihara plate image path"""
        # Try to find the image file
        image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images", "ishihara_plates")
        
        # Common naming patterns for Ishihara plates
        possible_names = [
            f"plate_{plate_number}.png",
            f"plate_{plate_number}.jpg", 
            f"ishihara_{plate_number}.png",
            f"ishihara_{plate_number}.jpg",
            f"{plate_number}.png",
            f"{plate_number}.jpg"
        ]
        
        for name in possible_names:
            image_path = os.path.join(image_dir, name)
            if os.path.exists(image_path):
                return image_path
        
        # If no image found, return None to fall back to generated pattern
        return None
    
    @staticmethod
    def has_plate_image(plate_number):
        """Check if an image exists for the given plate number"""
        return ColourVisionTest.get_ishihara_plate_image(plate_number) is not None
    
    @staticmethod
    def _create_digit_cluster(digit):
        """Create dense dot cluster for a single digit"""
        import random
        
        # Define digit patterns with more dots for better visibility (Ishihara-style)
        digit_patterns = {
            '0': [
                # Top curve - more dense
                (22, 18), (25, 17), (28, 16), (31, 16), (34, 16), (37, 17), (40, 18),
                (20, 22), (45, 22), (20, 26), (45, 26), (20, 30), (45, 30),
                # Middle section
                (20, 34), (45, 34), (20, 38), (45, 38), (20, 42), (45, 42),
                # Bottom curve
                (22, 46), (25, 47), (28, 48), (31, 48), (34, 48), (37, 47), (40, 46),
                (20, 50), (25, 52), (30, 53), (35, 53), (40, 52), (45, 50),
            ],
            '1': [
                # Main vertical line with thickness
                (32, 18), (33, 18), (32, 22), (33, 22), (32, 26), (33, 26),
                (32, 30), (33, 30), (32, 34), (33, 34), (32, 38), (33, 38),
                (32, 42), (33, 42), (32, 46), (33, 46), (32, 50), (33, 50),
                (32, 54), (33, 54),
                # Base
                (30, 56), (31, 57), (32, 58), (33, 58), (34, 57), (35, 56),
            ],
            '2': [
                # Top horizontal
                (20, 18), (24, 17), (28, 16), (32, 16), (36, 17), (40, 18), (44, 19),
                # Right curve down (more pronounced)
                (45, 22), (45, 26), (45, 30), (45, 34), (45, 36),
                # Middle diagonal curve (more distinctive)
                (43, 38), (40, 36), (36, 34), (32, 33), (28, 34), (24, 36), (20, 38),
                # Left side down (straight)
                (20, 42), (20, 46), (20, 50), (20, 54),
                # Bottom horizontal
                (20, 56), (24, 57), (28, 57), (32, 57), (36, 57), (40, 56), (44, 55),
            ],
            '3': [
                # Top horizontal
                (20, 18), (24, 17), (28, 16), (32, 16), (36, 17), (40, 18), (44, 19),
                # Right curve down (more pronounced)
                (45, 22), (45, 26), (45, 30), (45, 34), (45, 36),
                # Middle horizontal curve (more distinctive)
                (43, 38), (40, 36), (36, 34), (32, 33), (28, 34), (24, 36), (20, 38),
                # Right curve down again (more pronounced)
                (45, 42), (45, 46), (45, 50), (45, 54),
                # Bottom horizontal
                (44, 56), (40, 57), (36, 57), (32, 57), (28, 57), (24, 56), (20, 55),
            ],
            '4': [
                # Left vertical (taller)
                (20, 16), (20, 20), (20, 24), (20, 28), (20, 32), (20, 36),
                # Middle horizontal (thicker and centered)
                (20, 40), (24, 39), (28, 38), (32, 38), (36, 39), (40, 40), (44, 40),
                # Right vertical (taller)
                (45, 16), (45, 20), (45, 24), (45, 28), (45, 32), (45, 36), (45, 40), (45, 44), (45, 48), (45, 52), (45, 56),
            ],
            '5': [
                # Top horizontal (straight and prominent)
                (20, 18), (24, 18), (28, 18), (32, 18), (36, 18), (40, 18), (44, 18),
                # Left vertical (short)
                (20, 22), (20, 26),
                # Middle horizontal (straight and prominent)
                (20, 30), (24, 30), (28, 30), (32, 30), (36, 30), (40, 30), (44, 30),
                # Right vertical down (straight, no curve)
                (45, 34), (45, 38), (45, 42), (45, 46), (45, 50),
                # Bottom horizontal (straight)
                (44, 54), (40, 55), (36, 55), (32, 55), (28, 55), (24, 55), (20, 55),
            ],
            '6': [
                # Top curve (more pronounced)
                (25, 16), (28, 15), (32, 15), (36, 15), (40, 16), (43, 18),
                # Left vertical down (straight)
                (20, 22), (20, 26), (20, 30), (20, 34),
                # Middle curve (more distinctive)
                (20, 38), (24, 36), (28, 34), (32, 33), (36, 34), (40, 36), (44, 38),
                # Bottom curve (full circle)
                (43, 42), (40, 46), (36, 50), (32, 52), (28, 50), (24, 46), (21, 42),
                (20, 46), (20, 50), (20, 54),
                # Bottom closing curve
                (24, 56), (28, 57), (32, 57), (36, 57), (40, 56), (43, 54),
            ],
            '7': [
                # Top horizontal (straight)
                (20, 16), (24, 16), (28, 16), (32, 16), (36, 16), (40, 16), (44, 16),
                # Diagonal down (steeper and clearer)
                (42, 20), (40, 24), (38, 28), (36, 32), (34, 36), (32, 40), (30, 44), (28, 48), (26, 52), (24, 56),
                # Small horizontal base
                (22, 58), (26, 58), (30, 58),
            ],
            '8': [
                # Top curve (more pronounced)
                (25, 16), (28, 15), (32, 15), (36, 15), (40, 16), (43, 18),
                # Upper sides
                (20, 22), (45, 22), (20, 26), (45, 26),
                # Middle horizontal curve (more distinctive)
                (20, 30), (24, 28), (28, 27), (32, 27), (36, 28), (40, 30), (45, 30),
                # Lower sides
                (20, 34), (45, 34), (20, 38), (45, 38),
                # Bottom curve (more pronounced)
                (25, 42), (28, 43), (32, 43), (36, 43), (40, 42), (43, 40),
                # Lower sides again
                (20, 46), (45, 46), (20, 50), (45, 50),
                # Bottom closing curve
                (24, 54), (28, 55), (32, 55), (36, 55), (40, 54), (43, 52),
            ],
            '9': [
                # Top curve (more pronounced)
                (25, 16), (28, 15), (32, 15), (36, 15), (40, 16), (43, 18),
                # Upper sides
                (20, 22), (45, 22), (20, 26), (45, 26),
                # Middle curve (more distinctive)
                (20, 30), (24, 28), (28, 27), (32, 27), (36, 28), (40, 30), (45, 30),
                # Lower sides
                (20, 34), (45, 34), (20, 38), (45, 38),
                # Right vertical down (straight)
                (45, 42), (45, 46), (45, 50), (45, 54),
                # Bottom curve (partial)
                (40, 56), (36, 57), (32, 57), (28, 57), (24, 56), (21, 54),
            ]
        }
        
        return digit_patterns.get(digit, [])
    
    @staticmethod
    def get_farnsworth_colors():
        """Get Farnsworth D-15 test colors"""
        colors = [
            {"name": "Red", "hex": "#FF0000"},
            {"name": "Orange", "hex": "#FF7F00"},
            {"name": "Yellow", "hex": "#FFFF00"},
            {"name": "Yellow-Green", "hex": "#7FFF00"},
            {"name": "Green", "hex": "#00FF00"},
            {"name": "Green-Cyan", "hex": "#00FF7F"},
            {"name": "Cyan", "hex": "#00FFFF"},
            {"name": "Cyan-Blue", "hex": "#007FFF"},
            {"name": "Blue", "hex": "#0000FF"},
            {"name": "Blue-Magenta", "hex": "#7F00FF"},
            {"name": "Magenta", "hex": "#FF00FF"},
            {"name": "Magenta-Red", "hex": "#FF007F"}
        ]
        
        shuffled = colors.copy()
        random.shuffle(shuffled)
        return colors, shuffled
    
    @staticmethod
    def analyze_ishihara_results(answers):
        """Analyze Ishihara test results"""
        correct_answers = ["12", "8", "29", "5", "3", "15", "74", "6"]
        
        correct_count = 0
        detailed_results = []
        
        for i, (answer, correct) in enumerate(zip(answers, correct_answers)):
            is_correct = answer == correct
            if is_correct:
                correct_count += 1
            detailed_results.append({
                "Plate": i + 1,
                "Your Answer": answer if answer else "(skipped)",
                "Correct Answer": correct,
                "Result": "✓" if is_correct else "✗"
            })
        
        total_count = len(correct_answers)
        percentage = (correct_count / total_count) * 100
        
        if percentage >= 80:
            result = "Normal Colour Vision"
        elif percentage >= 40:
            result = "Mild Colour Vision Deficiency"
        else:
            result = "Significant Colour Vision Deficiency"
        
        return {
            "result": result,
            "percentage": percentage,
            "correct_count": correct_count,
            "total_count": total_count,
            "detailed_results": detailed_results
        }
    
    @staticmethod
    def analyze_farnsworth_results(user_order, correct_order):
        """Analyze Farnsworth D-15 test results"""
        correct_pairs = 0
        total_pairs = len(correct_order) - 1
        
        for i in range(total_pairs):
            try:
                user_index = user_order.index(correct_order[i])
                next_user_index = user_order.index(correct_order[i + 1])
                if abs(user_index - next_user_index) == 1:
                    correct_pairs += 1
            except ValueError:
                pass
        
        score = (correct_pairs / total_pairs) * 100 if total_pairs > 0 else 0
        
        if score >= 90:
            result = "Normal Colour Vision"
        elif score >= 70:
            result = "Mild Colour Vision Deficiency"
        else:
            result = "Significant Colour Vision Deficiency"
        
        return {
            "result": result,
            "score": score,
            "correct_pairs": correct_pairs,
            "total_pairs": total_pairs
        }
