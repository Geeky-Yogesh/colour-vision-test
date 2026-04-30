import random
import math

class ColourVisionTest:
    @staticmethod
    def create_dot_pattern(number, mode="standard"):
        background_dots = []
        number_dots = []
        CENTER = 50
        RADIUS = 45 

        # PALETTE SELECTION
        if mode == "tritan":
            # Tritan Confusion Colors: Violets vs Cyans
            bg_palette = ['#9370DB', '#8A2BE2', '#9932CC', '#9400D3', '#800080', '#BA55D3']
            fg_palette = ['#00CED1', '#20B2AA', '#48D1CC', '#40E0D0', '#00FFFF']
        else:
            # Standard Ishihara Colors: Greens vs Reds
            bg_palette = ['#228B22', '#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784']
            fg_palette = ['#FF0000', '#DC143C', '#B22222', '#FF4500', '#FF6347', '#CD5C5C']

        # 1. Background Dots
        for _ in range(1200): 
            angle = random.uniform(0, 2 * math.pi)
            r = RADIUS * math.sqrt(random.uniform(0, 1))
            x = CENTER + r * math.cos(angle)
            y = CENTER + r * math.sin(angle)
            color = random.choice(bg_palette)
            background_dots.append((x, y, random.uniform(2, 4), color))
        
        # 2. Number Dots (PRESERVING YOUR LOGIC)
        num_str = str(number)
        for i, digit in enumerate(num_str):
            offset_x = -20 if len(num_str) > 1 and i == 0 else 20 if len(num_str) > 1 else 0
            points = ColourVisionTest._get_large_digit_points(digit)
            for bx, by in points:
                for _ in range(3): 
                    x = bx + offset_x + random.uniform(-2, 2)
                    y = by + random.uniform(-2, 2)
                    if math.sqrt((x-50)**2 + (y-50)**2) < RADIUS:
                        color = random.choice(fg_palette)
                        number_dots.append((x, y, random.uniform(3, 6), color))
        return background_dots, number_dots

    @staticmethod
    def _get_large_digit_points(digit):
        """Your exact original patterns - No changes made here"""
        digit_patterns = {
            '1': [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
            '2': [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]],
            '3': [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,0,1],[0,0,1,1,0],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
            '4': [[1,0,0,1,0],[1,0,0,1,0],[1,0,0,1,0],[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0]],
            '5': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
            '6': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
            '7': [[1,1,1,1,1],[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[0,1,0,0,0],[0,1,0,0,0]],
            '8': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
            '9': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,1],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
            '0': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]]
        }
        pattern = digit_patterns.get(digit, [])
        all_points = []
        start_x, start_y, cell_size = 30, 25, 6
        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    center_x = start_x + col_idx * cell_size + cell_size // 2
                    center_y = start_y + (6 - row_idx) * cell_size + cell_size // 2
                    for dx in range(-3, 4):
                        for dy in range(-3, 4):
                            if abs(dx) + abs(dy) <= 3:
                                all_points.append((center_x + dx, center_y + dy))
        return all_points