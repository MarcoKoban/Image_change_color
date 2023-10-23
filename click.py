# click.py

from pynput.mouse import Listener
from PIL import Image

class MouseClick:
    coo = []

    def __init__(self):
        self.custom_palette = {
            (489, 430),  # Black
            (534, 430),  # White
            (583, 430),  # Pine Green
            (479, 480),  # Gold
            (537, 480),  # Yellow
            (582, 480),  # Dark
            (480, 530),  # Gray
            (537, 530),  # Silver
            (582, 530),  # Burgundy
            (483, 585),  # Red
            (536, 585),  # Plum
            (576, 585),  # Pink
            (490, 630),  # Blue
            (530, 630),  # Cyan
            (585, 630),  # Brown
            (472, 685),  # Orange
            (528, 685),  # Coral
            (587, 685)   # Beige
        }

    def on_click(self, x, y, button, pressed):
        if button == button.left and pressed:
            print(f"Coordinates number {len(self.coo) + 1} are ({x}, {y})")
            self.coo.append((x, y))

            if len(self.coo) == 2:
                self.listener.stop()

    def calculate_size_image(self, coo1, coo2):
        x = abs(coo1[0] - coo2[0])
        y = abs(coo1[1] - coo2[1])
        return x, y

    def run_listener(self):
        with Listener(on_click=self.on_click) as self.listener:  # Stockez la référence du listener dans self.listener
            self.listener.join()

    def resize_image(self, image_path, size_image):
        image = Image.open(image_path)
        max_size = (size_image[0], size_image[1])
        image.thumbnail(max_size)
        image.save('resize.png')

    def get_coo(self):
        return self.coo
