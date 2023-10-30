import image_generator
import sys
import click
import PIL
import argparse

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

    if args.size == None:
        args.size = 1

    print(args)
    return args

def create_list():
    color_file = "color/colorPalette"
    pos_color_file = "color/posColor"
    color_list = image_generator.read_file(color_file, 3)
    pos_color_list = image_generator.read_file(pos_color_file, 2)
    return color_list, pos_color_file

def generate_resize_image(image_path, instance_click, coo):
    size_image = instance_click.calculate_size_image(coo[0], coo[1])
    print(size_image)
    instance_click.resize_image(image_path, size_image)
    image = image_generator.load_image(image_path)
    resize_image_path = "images/resize.png"
    resize_image = image_generator.load_image(resize_image_path)
    return resize_image

def main():
    args = gestion_option()
    list_from_file = create_list()
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

    image_generator.create_image_with_sampled_colors("images/quantized_image.png", args.pixel_space)
    sampled = image_generator.load_image("images/output_image.png")

if __name__ == "__main__":
    main()