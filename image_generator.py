import cv2
import PIL
import requests
from io import BytesIO

def load_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            image = PIL.Image.open(BytesIO(image_data))
            return image
        else:
            print(f"Failed to retrieve the image. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image:", image_path)
        return None

    return PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def quantize_image(image, palette_size, custom_palette):
    if custom_palette is None:
        quantized_image = image.quantize(colors=palette_size)
    else:
        custom_palette_obj = PIL.Image.new('P', (16, 16))
        custom_palette_obj.putpalette([x for color in custom_palette for x in color])
        quantized_image = image.convert("RGB").quantize(colors=palette_size, palette=custom_palette_obj)

    return quantized_image

def read_file(nom_fichier, size_groupe):
    try:
        with open(nom_fichier, 'r') as fichier:
            valeurs = fichier.read().split()
            groupes = []
            for i in range(0, len(valeurs), size_groupe):
                groupe = [int(valeurs[i + j]) for j in range(size_groupe)]
                groupes.append(groupe)
            return groupes
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
        return []
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return []
    
def create_image_with_sampled_colors(input_image_path, x):
    input_image = PIL.Image.open(input_image_path)
    input_image = input_image.convert("RGB")

    width, height = input_image.size
    output_image = PIL.Image.new('RGB', (width, height))
    for i in range(0, width, x):
        for j in range(0, height, x):
            pixel_color = input_image.getpixel((i, j))
            for a in range(i, min(i + x, width)):
                for b in range(j, min(j + x, height)):
                    output_image.putpixel((a, b), pixel_color)
    output_image.save('images/output_image.png')
