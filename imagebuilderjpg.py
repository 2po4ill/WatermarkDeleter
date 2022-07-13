from PIL import ImageDraw


def imagereader(image):
    """ Функция определяющая цвет фона и выполняющая imageconverter """

    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    reds = pix[0, 0][0]
    greens = pix[0, 0][1]
    blues = pix[0, 0][2]
    draw = ImageDraw.Draw(image)
    if reds == blues and blues == greens and greens == 235:
        imageconverter(draw, width, height, pix, True)
    elif reds == blues and blues == greens and greens == 255:
        imageconverter(draw, width, height, pix, False)


def imageconverter(draw, width, height, pix, mode):
    """ Функция перерисовывующая пиксели вотермарки в цвет фона и сохраняющая получившийся picture """

    if mode:
        for i in range(width):
            for j in range(height):
                redn = pix[i, j][0]
                greenn = pix[i, j][1]
                bluen = pix[i, j][2]
                if redn > 231 and greenn > 231 and bluen > 231:
                    draw.point((i, j), (231, 231, 231))
    else:
        for i in range(width):
            for j in range(height):
                redn = pix[i, j][0]
                greenn = pix[i, j][1]
                bluen = pix[i, j][2]
                if redn >= 228 and greenn >= 228 and bluen >= 228 and redn != 255 and greenn != 255 and bluen != 255:
                    draw.point((i, j), (255, 255, 255))
