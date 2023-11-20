import image_generator
import sys
import click
import argparse
import pynput
import time
from pynput.mouse import Controller, Button

def gestion_option():
    parser = argparse.ArgumentParser(description="Exemple de programme avec des options en tiret.")
    parser.add_argument("-u", "--url", help="Add the URL at the Iamge")
    parser.add_argument("-f", "--file", help="Add the PATH of the Iamge")
    parser.add_argument("-s", "--size", help="Add the size of the Iamge")
    parser.add_argument("-p", "--pixel_space", help="Add the pixel space of the Iamge")
    parser.add_argument("-sp", "--speed", help="Add the speed of the Iamge in second")
    parser.add_argument("-pos", "--position", help="Add the start position of the Iamge")

    args = parser.parse_args()

    if args.url and args.file:
        print("You can't use -u and -f at the same time")
        sys.exit(0)

    if args.size != None:
        if len(args.size.split(",")) == 2:
            args.size = args.size.split(",")
            args.size = tuple([int(x) for x in args.size])
        else:
            print("You need to add two numbers for the size")
            sys.exit(0)
        if args.size[0] < 0 or args.size[1] < 0:
            print("You need to add two positive numbers for the size")
            sys.exit(0)
        if args.size[0] > 950 or args.size[1] > 530:
            print("You need to add two numbers under 950 and 530 for the size")
            sys.exit(0)

        if args.position != None:
            if len(args.position.split(",")) == 2:
                args.position = args.position.split(",")
                args.position = tuple([int(x) for x in args.position])
            else:
                print("You need to add two numbers for the position")
                sys.exit(0)
            print(args.position)
            if args.position[0] < 0 or args.position[1] < 0:
                print("You need to add two positive numbers for the position")
                sys.exit(0)
            if args.position[0] > 950 or args.position[1] > 530:
                print("You need to add two numbers under 950 and 530 for the position")
                sys.exit(0)
            args.position = (args.position[0] + 580, args.position[1] + 340)
        
        if args.position and args.size == None or args.position == None and args.size == None:
            print("You need to use -s and -pos at the same time")
            sys.exit(0)

    if args.pixel_space == None:
        args.pixel_space = 1

    if args.speed == None:
        args.speed = 0.001
    return args

def create_list():
    color_file = "color/colorPalette"
    pos_color_file = "color/posColor"
    color_list = image_generator.read_file(color_file, 3)
    pos_color_list = image_generator.read_file(pos_color_file, 2)
    return color_list, pos_color_list

def generate_resize_image(image_path, instance_click, coo, method=1):
    if method == 1:
        size_image = instance_click.calculate_size_image(coo[0], coo[1])
        instance_click.resize_image(image_path, size_image)
    elif method == 2:
        instance_click.resize_image(image_path, coo)
    
    image = image_generator.load_image(image_path)
    resize_image_path = "images/resize.png"
    resize_image = image_generator.load_image(resize_image_path)
    return resize_image

def find_color(color, color_list):
    for i in range(len(color_list)):
        if color == color_list[i]:
            return i
    return -1

def draw_image(coo, image, pixel_space, lists, speed):
    width, height = image.size
    mouse = pynput.mouse.Controller()

    pixel_space = int(pixel_space)
    for i in range(len(lists[0])):
        if i != 3:
            mouse.position = (lists[1][i][0], lists[1][i][1])
            mouse.click(pynput.mouse.Button.left, 1)
            for y in range(0, height, pixel_space):
                for x in range(0, width, pixel_space):
                    try:
                        pixel = image.getpixel((x, y))
                        if pixel == tuple(lists[0][i]):
                            while pixel == tuple(lists[0][i]):
                                x += 1
                                pixel = image.getpixel((x, y))
                                mouse.position = (x + coo[0][0], y + coo[0][1])
                                mouse.press(Button.left)
                            time.sleep(speed)
                            mouse.release(Button.left)
                    except IndexError:
                        x = min(x, width - 1)
                        y = min(y, height - 1)
                        pixel = image.getpixel((x, y))

                        if pixel == lists[0][i]:
                            while pixel == tuple(lists[0][i]):
                                x += 1
                                pixel = image.getpixel((x, y))
                                mouse.position = (x + coo[0][0], y + coo[0][1])
                                mouse.press(Button.left)
                            time.sleep(speed)
                            mouse.release(Button.left)

def draw_image2(coo, image, pixel_space, lists, speed):
    width, height = image.size
    mouse = pynput.mouse.Controller()

    pixel_space = int(pixel_space)
    for i in range(len(lists[0])):
        if i != 3:
            mouse.position = (lists[1][i][0], lists[1][i][1])
            mouse.click(pynput.mouse.Button.left, 1)
            for y in range(0, height, pixel_space):
                for x in range(0, width, pixel_space):
                    try:
                        pixel = image.getpixel((x, y))
                        if pixel == tuple(lists[0][i]):
                            while pixel == tuple(lists[0][i]):
                                x += 1
                                pixel = image.getpixel((x, y))
                                mouse.position = (x + coo[0], y + coo[1])
                                mouse.press(Button.left)
                            time.sleep(speed)
                            mouse.release(Button.left)
                    except IndexError:
                        x = min(x, width - 1)
                        y = min(y, height - 1)
                        pixel = image.getpixel((x, y))

                        if pixel == lists[0][i]:
                            while pixel == tuple(lists[0][i]):
                                x += 1
                                pixel = image.getpixel((x, y))
                                mouse.position = (x + coo[0], y + coo[1])
                                mouse.press(Button.left)
                            time.sleep(speed)
                            mouse.release(Button.left)

def main():
    args = gestion_option()
    list_from_file = create_list()
    mouse_click_instance = click.MouseClick()

    if args.url:
        image = image_generator.load_image_from_url(args.url)
        image.save("images/image.png")
        image_path = "images/image.png"
    else:
        image_path = args.file
        print(image_path)

    if args.size != None:
        time.sleep(5)
        print(list(args.size))
        resize_image = generate_resize_image(image_path, mouse_click_instance, list(args.size), 2)
    else:
        mouse_click_instance.run_listener()
        coo = mouse_click_instance.get_coo()
        print(coo)
        resize_image = generate_resize_image(image_path, mouse_click_instance, coo)

    quantized_image = image_generator.quantize_image(resize_image, 18, list_from_file[0])
    quantized_image.save("images/quantized_image.png")
    print("Image quantized has been created")

    image_generator.create_image_with_sampled_colors("images/quantized_image.png", int(args.pixel_space))
    sampled = image_generator.load_image("images/output_image.png")

    if args.position != None:
        print(list(args.position))
        draw_image2(list(args.position), sampled, args.pixel_space, list_from_file, args.speed)
    else:
        draw_image(coo, sampled, args.pixel_space, list_from_file, args.speed)

if __name__ == "__main__":
    main()