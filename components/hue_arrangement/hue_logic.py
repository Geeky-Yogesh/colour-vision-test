import colorsys
import random

class HueLogic:
    @staticmethod
    def generate_spectrum(num_caps=16):
        """
        Generates a spectrum of colors in HSL space.
        Returns a list of dictionaries with id and hex color.
        """
        colors = []
        for i in range(num_caps):
            # We vary the hue from 0 to 0.8 (Red through Green to Blue-ish)
            # Standard FM100 uses specific trays; this simulates one tray.
            h = (i / num_caps) * 0.8 
            s = 0.6  # Saturation
            l = 0.5  # Lightness
            rgb = colorsys.hls_to_rgb(h, l, s)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append({
                "id": i,
                "hex": hex_color
            })
        return colors

    @staticmethod
    def calculate_score(user_order, correct_order):
        """
        Calculates the Total Error Score (TES).
        In the real test, TES is the sum of differences between cap positions.
        """
        total_error = 0
        for i, user_cap in enumerate(user_order):
            # Find where this cap was supposed to be
            correct_pos = next(index for index, cap in enumerate(correct_order) if cap['id'] == user_cap['id'])
            # Absolute difference in position
            total_error += abs(i - correct_pos)
        
        # Calculate a human-friendly accuracy percentage
        # max_error is a theoretical limit where everything is reversed
        max_possible_error = len(correct_order) * (len(correct_order) // 2)
        accuracy = max(0, 100 - (total_error / max_possible_error * 100))
        
        return total_error, accuracy
