import image_generator
import sys
import click
import PIL
import argparse
import draw
import pynput
import time

def gestion_option():
    parser = argparse.ArgumentParser(description="Exemple de programme avec des options en tiret.")
    parser.add_argument("-u", "--url", help="Add the URL at the Iamge")
    parser.add_argument("-f", "--file", help="Add the PATH of the Iamge")
    parser.add_argument("-s", "--size", help="Add the size of the Iamge")
    parser.add_argument("-p", "--pixel_space", help="Add the pixel space of the Iamge")
    parser.add_argument("-sp", "--speed", help="Add the speed of the Iamge")
    parser.add_argument("-pos", "--position", help="Add the start position of the Iamge")

    args = parser.parse_args()

    if args.url and args.file:
        print("You can't use -u and -f at the same time")
        sys.exit(0)

    if args.pixel_space == None:
        args.pixel_space = 1

    print(args) 
    return args

def create_list():
    color_file = "color/colorPalette"
    pos_color_file = "color/posColor"
    color_list = image_generator.read_file(color_file, 3)
    pos_color_list = image_generator.read_file(pos_color_file, 2)
    return color_list, pos_color_list

def generate_resize_image(image_path, instance_click, coo):
    size_image = instance_click.calculate_size_image(coo[0], coo[1])
    print(size_image)
    instance_click.resize_image(image_path, size_image)
    image = image_generator.load_image(image_path)
    resize_image_path = "images/resize.png"
    resize_image = image_generator.load_image(resize_image_path)
    return resize_image

def find_color(color, color_list):
    for i in range(len(color_list)):
        if color == color_list[i]:
            return i
    return -1

def draw_image(coo, image, pixel_space, lists):
    print("\n\n\n")
    print(coo)
    width, height = image.size
    print(width, height)
    mouse = pynput.mouse.Controller()

    pixel_space = int(pixel_space)
    for y in range(0, height, pixel_space):
        for x in range(0, width, pixel_space):
            try:
                pixel = image.getpixel((x, y))
                pos = find_color(list(pixel), lists[0])
                #print(f"Coordonnées : ({x}, {y}), Couleur : {pixel}, Position : {find_color(list(pixel), lists[0])}, Position : {lists[1][pos]}")
                mouse.position = (lists[1][pos][0], lists[1][pos][1])
                mouse.click(pynput.mouse.Button.left, 1)
                mouse.position = (x + coo[0][0], y + coo[0][1])
                time.sleep(0.001)
                mouse.click(pynput.mouse.Button.left, 1)
                time.sleep(0.001)
            except IndexError:
                x = min(x, width - 1)
                y = min(y, height - 1)
                pixel = image.getpixel((x, y))
                pos = find_color(list(pixel), lists[0])  
                mouse.position = (lists[1][pos][0], lists[1][pos][1])
                print(mouse.position)
                mouse.click(pynput.mouse.Button.left, 1)
                mouse.position = (x + coo[0][0], y + coo[0][1])
                print(mouse.position)
                time.sleep(0.001)
                mouse.click(pynput.mouse.Button.left, 1)
                time.sleep(0.001)

                #print(f"Coordonnées : ({x}, {y}), Couleur : {pixel}, Position : {find_color(list(pixel), lists[0])}, Position : {lists[1][pos]}")

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Coordonnées du clic : ({x}, {y})')


def main():
    args = gestion_option()
    list_from_file = create_list()
    print(list_from_file[0])
    print(list_from_file[1])


    '''with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()'''

    print(list_from_file[1])
    mouse_click_instance = click.MouseClick()
    mouse_click_instance.run_listener()
    coo = mouse_click_instance.get_coo()


    if args.url:
        image = image_generator.load_image_from_url(args.url)
        image.save("images/image.png")
        image_path = "images/image.png"
    else:
        image_path = args.file
        print(image_path)

    resize_image = generate_resize_image(image_path, mouse_click_instance, coo)

    quantized_image = image_generator.quantize_image(resize_image, 18, list_from_file[0])
    quantized_image.save("images/quantized_image.png")
    print("Image quantized has been created")

    image_generator.create_image_with_sampled_colors("images/quantized_image.png", int(args.pixel_space))
    sampled = image_generator.load_image("images/output_image.png")

    draw_image(coo, sampled, args.pixel_space, list_from_file)

if __name__ == "__main__":
    main()