from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/UG_encode.png"):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            red_pixel = red_channel.getpixel((i, j))
            if int(bin(red_pixel)[-1]) == 1:
                pixels[i, j] = (255,0,0)
            else:
                pixels[i, j] = (255, 255, 255)

    decoded_image.save("images/UG_decode.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/UG.png"):
    template = Image.open(template_image)

    red = template.split()[0]
    green = template.split()[1]
    blue = template.split()[2]
    size = (template.size[0], template.size[1])

    image_text = write_text(text_to_encode, template.size)
    black_and_white_pixels = image_text.convert('1')

    new_image = Image.new("RGB", size)
    pixels = new_image.load()

    for x in range(size[0]):
        for y in range(size[1]): 
            curr_pixel = bin(black_and_white_pixels.getpixel((x, y)))
            new_red_pixel = bin(red.getpixel((x, y)))[:-1] + curr_pixel[-1]
            pixels[x, y] = (
              int(new_red_pixel, 2),
              green.getpixel((x, y)),
              blue.getpixel((x, y))
            )

    new_image.save("images/UG_encode.png")

if __name__ == '__main__':
    print("Encoding the image...")
    encode_image("Hello UG!")

    print("Decoding the image...")
    decode_image()