from ..colour_vision_test import ColourVisionTest

class TritanLogic:
    @staticmethod
    def get_plate(number):
        # Uses your existing generator with Tritan colors
        return ColourVisionTest.create_dot_pattern(number, mode="tritan")
