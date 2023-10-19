import pynput

def on_click(x, y, button, pressed):
    if button == pynput.mouse.Button.left and pressed:
        print(f"Left mouse button clicked at coordinates: ({x}, {y})")

listener = pynput.mouse.Listener(on_click=on_click)

listener.start()

listener.join()
