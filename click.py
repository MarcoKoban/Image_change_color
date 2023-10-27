# click.py

from pynput.mouse import Listener
from PIL import Image

class MouseClick:
    coo = []

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
        with Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

    def resize_image(self, image_path, size_image):
        image = Image.open(image_path)
        max_size = (size_image[0], size_image[1])
        image.thumbnail(max_size)
        image.save('images/resize.png')

    def get_coo(self):
        return self.coo
