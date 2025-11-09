from PIL import Image

if __name__ == '__main__':
    base_image_path = "images/City.png"
    img = Image.open(base_image_path)

    print(img.size)