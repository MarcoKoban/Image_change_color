from pynput import mouse
from PIL import Image

coo = []

def on_click(x, y, button, pressed):
    global coo
    if button == mouse.Button.left and pressed:
        print(f"Left mouse button clicked at coordinates: ({x}, {y})")
        coo.append((x, y))

        if len(coo) == 2:
            print(coo)
            listener.stop()

def calculate_size_image(coo1, coo2):
    if coo1[0] > coo2[0]:
        x = coo1[0] - coo2[0]
    else:
        x = coo2[0] - coo1[0]
    if coo1[1] > coo2[1]:
        y = coo1[1] - coo2[1]
    else:
        y = coo2[1] - coo1[1]
    return x, y

def resize_image(image_path, size_image):
    image = Image.open(image_path) 
    MAX_SIZE = (size_image[0], size_image[1]) 
    image.thumbnail(MAX_SIZE)  
    image.save('test.png') 

def main():
    global listener
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
    size_image = calculate_size_image(coo[0], coo[1])
    print(size_image)
    image_path = "eiffel.jpg"
    resize_image(image_path, size_image)

if __name__ == "__main__":
    main()
