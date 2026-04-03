import random
import math

class ColourVisionTest:
    @staticmethod
    def create_dot_pattern(number):
        background_dots = []
        number_dots = []
        CENTER = 50
        RADIUS = 45 

        # 1. Background Dots (Greens/Yellow-Greens)
        # Increased to 1200 dots for better coverage
        for _ in range(1200):
            angle = random.uniform(0, 2 * math.pi)
            r = RADIUS * math.sqrt(random.uniform(0, 1))
            x = CENTER + r * math.cos(angle)
            y = CENTER + r * math.sin(angle)
            
            # Use better Ishihara green palette with more contrast
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
                # Add randomness to every segment point to create "thickness"
                for _ in range(5): 
                    x = bx + offset_x + random.uniform(-3, 3)
                    y = by + random.uniform(-3, 3)
                    
                    # Ensure dot stays inside the circular plate
                    if math.sqrt((x-50)**2 + (y-50)**2) < RADIUS:
                        # Better Ishihara-style red/orange colors with higher contrast
                        color = random.choice([
                            '#FF0000',  # Pure Red
                            '#DC143C',  # Crimson
                            '#B22222',  # Fire Brick
                            '#FF4500',  # Orange Red
                            '#FF6347',  # Tomato
                            '#CD5C5C'   # Indian Red
                        ])
                        number_dots.append((x, y, random.uniform(5, 8), color))
        
        return background_dots, number_dots

    @staticmethod
    def _get_large_digit_points(digit):
        """Large-scale coordinates for Plotly (20 to 80 range)"""
        # (x_start, y_start, x_end, y_end) for segments
        # We will interpolate points between these starts and ends
        segments = {
            '1': [(50, 20, 50, 80)],
            '2': [(25, 75, 75, 75), (75, 75, 75, 50), (75, 50, 25, 50), (25, 50, 25, 25), (25, 25, 75, 25)],
            '3': [(25, 75, 75, 75), (75, 75, 75, 25), (75, 50, 40, 50), (75, 25, 25, 25)],
            '4': [(25, 75, 25, 50), (25, 50, 75, 50), (75, 80, 75, 20)],
            '5': [(75, 75, 25, 75), (25, 75, 25, 50), (25, 50, 75, 50), (75, 50, 75, 25), (75, 25, 25, 25)],
            '6': [(25, 75, 25, 25), (25, 25, 75, 25), (75, 25, 75, 50), (75, 50, 25, 50)],
            '7': [(25, 75, 75, 75), (75, 75, 40, 20)],
            '8': [(25, 75, 75, 75), (25, 25, 75, 25), (25, 75, 25, 25), (75, 75, 75, 25), (25, 50, 75, 50)],
            '9': [(75, 25, 75, 75), (75, 75, 25, 75), (25, 75, 25, 50), (25, 50, 75, 50)],
            '0': [(25, 75, 75, 75), (25, 25, 75, 25), (25, 75, 25, 25), (75, 75, 75, 25)]
        }
        
        path = segments.get(digit, [])
        all_points = []
        
        # Interpolate points along the segments for density
        for x1, y1, x2, y2 in path:
            steps = 15
            for s in range(steps + 1):
                px = x1 + (x2 - x1) * (s / steps)
                py = y1 + (y2 - y1) * (s / steps)
                all_points.append((px, py))
        
        return all_points