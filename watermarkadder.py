from PIL import Image, ImageDraw
import cv2

def imagereader(image, watermark, result):
    """ Функция определяющая цвет фона и выполняющая imageconverter """

    src = cv2.imread(watermark, cv2.IMREAD_UNCHANGED)
    width = image.size[0]
    height = image.size[1]
    dsize = (width, height)
    output = cv2.resize(src, dsize)
    cv2.imwrite(watermark, output)
    img = Image.open(watermark)
    pix = image.load()
    pixtrg = img.load()
    draw = ImageDraw.Draw(image)
    background = pix[0, 0]
    for i in range(width):
        for j in range(height):
            if pix[i, j][0] >= background[0]-5:
                draw.point((i, j), (pixtrg[i, j][0], pixtrg[i, j][1], pixtrg[i, j][2]))
    image.save(result, 'png')

