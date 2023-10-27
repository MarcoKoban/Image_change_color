import image_generator
import sys
import click

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
    list_from_file = create_list()
    mouse_click_instance = click.MouseClick()
    mouse_click_instance.run_listener()
    coo = mouse_click_instance.get_coo()


    if sys.argv[1] == "1":
        url = sys.argv[2]
        image = image_generator.load_image_from_url(url)
        image.save("images/image.png")
        image_path = "images/image.png"
    else:
        image_path = sys.argv[2]
        print(image_path)

    resize_image = generate_resize_image(image_path, mouse_click_instance, coo)
    quantized_image = image_generator.quantize_image(resize_image, 18, list_from_file[0])
    quantized_image.save("images/quantized_image.png")
    print("Image quantized has been created")


if __name__ == "__main__":
    main()