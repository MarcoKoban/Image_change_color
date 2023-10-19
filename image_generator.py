import cv2
import numpy as np

rgb_values = [
    (0, 0, 0),        # Black
    (255, 255, 255),  # White
    (0, 128, 0),      # Pine Green
    (255, 215, 0),    # Gold
    (255, 255, 0),    # Yellow
    (169, 169, 169),  # Dark Gray
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

def load_image(image):
    if image is not None:
        height, width, channels = image.shape
        matrix = []
        for y in range(height):
            for x in range(width):
                b, g, r = image[y, x]
                matrix.append([b, g, r])
        return np.array(matrix)
    else:
        print("Impossible de charger l'image.")
        return None

def find_closest_color(pixel, colors):
    pixel = np.array(pixel)
    colors = np.array(colors)
    distances = np.linalg.norm(colors - pixel, axis=1)
    closest_color_index = np.argmin(distances)
    return colors[closest_color_index]

def create_new_image(image_matrix, image):
    if image_matrix is not None:
        for i in range(len(image_matrix)):
            image_matrix[i] = find_closest_color(image_matrix[i], rgb_values)

        new_image = image_matrix.reshape(image.shape)
        return new_image

def main():
    image = cv2.imread("wario.jpg")
    image_matrix = load_image(image)
    new_image = create_new_image(image_matrix, image)

    cv2.imwrite("output_image.jpg", new_image)
    cv2.imshow("Original Image", image)
    cv2.imshow("Processed Image", new_image)

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # Pressing the 'ESC' key (27) closes the windows
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
