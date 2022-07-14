from PIL import Image
import cv2

def imagereader(image, watermark, result):
    """ Функция определяющая цвет фона и выполняющая imageconverter """

    src = cv2.imread(watermark, cv2.IMREAD_UNCHANGED)
    width = image.size[0]
    height = image.size[1]
    dsize = (width, height)
    output = cv2.resize(src, dsize)
    cv2.imwrite(watermark, output)
    image.convert('RGBA')
    pix = image.load()
    background = pix[0, 0]
    for i in range(height):
        for j in range(width):
            if pix[j, i] == background:
                pix[j, i] = (255, 255, 255, 0)
    img = Image.open(watermark).convert("RGBA")
    x, y = img.size
    img.paste(image, (0, 0, x, y), image)
    img.save(result, 'png')
