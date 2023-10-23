import cv2
from PIL import Image
from click import MouseClick
import pyautogui
from pynput.mouse import Button, Controller
import time

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image:", image_path)
        return None

    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def quantize_image(image, palette_size=16, custom_palette=None):
    if custom_palette is None:
        quantized_image = image.quantize(colors=palette_size)
    else:
        custom_palette_obj = Image.new('P', (1, 1))
        custom_palette_obj.putpalette([x for color in custom_palette for x in color])
        quantized_image = image.quantize(colors=palette_size, palette=custom_palette_obj)

    return quantized_image.convert('RGB')

def process_image(image):
    if image is None:
        return
    custom_palette = [
        (0, 0, 0),        # Black
        (255, 255, 255),  # White
        (0, 128, 0),      # Pine Green
        (255, 215, 0),    # Gold
        (255, 255, 0),    # Yellow
        (169, 169, 169),  # Dark
        (128, 128, 128),  # Gray
        (192, 192, 192),  # Silver
        (128, 0, 32),     # Burgundy
        (255, 0, 0),      # Red
        (142, 69, 133),   # Plum
        (255, 192, 203),  # Pink
        (0, 0, 255),      # Blue
        (0, 255, 255),    # Cyan
        (165, 42, 42),    # Brown
        (255, 165, 0),    # Orange
        (255, 127, 80),   # Coral
        (245, 245, 220)   # Beige
    ]

    quantized_image = quantize_image(image, palette_size=16, custom_palette=custom_palette)
    return quantized_image

def get_pixel_colors(image_path):
    image = Image.open(image_path)
    pixel_colors = {}

    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            pixel_colors[(x, y)] = pixel

    return pixel_colors

def click_after_delay(pos, pixel_colors):
    mouse = Controller()
    for pixel_position, color in pixel_colors.items():
        if (color == (0, 255, 255)):
            #print(f"Pixel at position {pixel_position}")
            mouse.position = (int(pixel_position[0]) + int(pos[0]), int(pixel_position[1]) + int(pos[1]))
            time.sleep(0.001)  # Attendre pendant 0.1 seconde (ajuster si nécessaire)
            mouse.click(Button.left, 1)


def main():
    image_path = "eiffel.jpg"
    image = load_image(image_path)
    mouse_click_instance = MouseClick()
    mouse_click_instance.run_listener()
    coo = mouse_click_instance.get_coo()
    if coo:
        size_image = mouse_click_instance.calculate_size_image(coo[0], coo[1])
        print(size_image)
        mouse_click_instance.resize_image(image_path, size_image)

    resize_image_path = ("resize.png")
    resize_image = load_image(resize_image_path)
    quantized_image = process_image(resize_image)
    quantized_image.save("quantized_image.png")
    print("Image quantized has been created")
    
    quantized_image_path = ("quantized_image.png")
    pixel_colors = get_pixel_colors(quantized_image_path)
    click_after_delay(coo[0], pixel_colors)

if __name__ == "__main__":
    main()