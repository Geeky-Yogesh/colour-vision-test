import random
import math

class ColourVisionTest:
    @staticmethod
    def create_dot_pattern(number):
        background_dots = []
        number_dots = []
        CENTER = 50
        RADIUS = 45 

        # Generate inverted number for colorblind people (different from main number)
        # Ensure inverted_number is always different from 'number'
        possible_inverted_numbers = [i for i in range(1, 10) if i != number]
        inverted_number = random.choice(possible_inverted_numbers) if possible_inverted_numbers else (number % 9) + 1

        # 1. Background Dots (Greens/Yellow-Greens) - some will form inverted number
        for _ in range(1200):  # Reduced density to avoid interference
            angle = random.uniform(0, 2 * math.pi)
            r = RADIUS * math.sqrt(random.uniform(0, 1))
            x = CENTER + r * math.cos(angle)
            y = CENTER + r * math.sin(angle)
            
            # Check if this position should be part of inverted number (only 15% chance)
            is_inverted_dot = False
            if random.random() < 0.15:  # Only 15% of dots check for inverted number
                inv_points = ColourVisionTest._get_large_digit_points(str(inverted_number))
                for bx, by in inv_points:
                    # Position inverted number on the right side to avoid interference
                    offset_x_inv = 15 if len(str(inverted_number)) == 1 else 8
                    if math.sqrt((x - (bx + offset_x_inv))**2 + (y - by)**2) < 2.0:
                        is_inverted_dot = True
                        break
            
            if is_inverted_dot:
                # Use darker greens for inverted number
                color = random.choice([
                    '#006400',  # Dark Green
                    '#228B22',  # Forest Green  
                    '#2E7D32',  # Dark Green
                    '#1B5E20'   # Very Dark Green
                ])
                background_dots.append((x, y, random.uniform(2.0, 3.5), color))
            else:
                # Regular background colors
                color = random.choice([
                    '#228B22',  # Forest Green
                    '#2E7D32',  # Dark Green
                    '#388E3C',  # Medium Green
                    '#43A047',  # Light Green
                    '#4CAF50',  # Lime Green
                    '#66BB6A',  # Light Lime Green
                    '#81C784'   # Pale Green
                ])
                background_dots.append((x, y, random.uniform(2, 4), color))
        
        # 2. Number Dots (Red/Oranges)
        num_str = str(number)
        for i, digit in enumerate(num_str):
            # Spacing for double digits
            offset_x = -16 if len(num_str) > 1 and i == 0 else 16 if len(num_str) > 1 else 0
            
            points = ColourVisionTest._get_large_digit_points(digit)
            
            for bx, by in points:
                # Add more dots for better density and clarity
                for _ in range(3):  # Reduced from 8 to 3 for less density
                    x = bx + offset_x + random.uniform(-2, 2)  # Reduced randomness for cleaner shapes
                    y = by + random.uniform(-2, 2)
                    
                    # Ensure dot stays inside the circular plate
                    if math.sqrt((x-50)**2 + (y-50)**2) < RADIUS:
                        # Use different red shades for different digits to improve separation
                        if i == 0:  # First digit
                            color = random.choice([
                                '#FF0000',  # Pure Red
                                '#DC143C',  # Crimson
                                '#B22222',  # Fire Brick
                            ])
                        else:  # Second digit
                            color = random.choice([
                                '#FF4500',  # Orange Red
                                '#FF6347',  # Tomato
                                '#CD5C5C'   # Indian Red
                            ])
                        number_dots.append((x, y, random.uniform(3, 6), color))  # Smaller dots
        
        return background_dots, number_dots

    @staticmethod
    def _get_large_digit_points(digit):
        """Improved digit patterns for better recognition - uses matrix-style digit formation"""
        # Define digits as 7x5 grids (1 = filled, 0 = empty)
        # Scale factors to fit within 25-75 range
        digit_patterns = {
            '1': [
                [0,0,1,0,0],
                [0,1,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [1,1,1,1,1]
            ],
            '2': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,1,1,1,1]
            ],
            '3': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [0,0,0,0,1],
                [0,0,1,1,0],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '4': [
                [1,0,0,1,0],
                [1,0,0,1,0],
                [1,0,0,1,0],
                [1,1,1,1,1],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,0,0,1,0]
            ],
            '5': [
                [1,1,1,1,1],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [0,0,0,0,1],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '6': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '7': [
                [1,1,1,1,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0]
            ],
            '8': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '9': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,1],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '0': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ]
        }
        
        pattern = digit_patterns.get(digit, [])
        all_points = []
        
        # Convert grid to coordinates
        # Each cell is 8x8 units, positioned to fit within 25-75 range
        start_x = 30
        start_y = 25
        cell_size = 8
        
        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell == 1:  # Fill this cell
                    # Create multiple points within each cell for density
                    center_x = start_x + col_idx * cell_size + cell_size // 2
                    # Reverse Y-coordinate to fix upside-down issue (row 0 should be at top)
                    center_y = start_y + (6 - row_idx) * cell_size + cell_size // 2  # 6 because 7 rows (0-6)
                    
                    # Add points in a small pattern within each cell
                    for dx in range(-3, 4):
                        for dy in range(-3, 4):
                            if abs(dx) + abs(dy) <= 3:  # Diamond pattern
                                x = center_x + dx
                                y = center_y + dy
                                all_points.append((x, y))
        
        return all_points