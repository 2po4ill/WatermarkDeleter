"""
Модуль реализующий удаление вотермарки на png и jpg изображениях
"""
from PIL import ImageDraw


def imagereader(image, formatim):
    """ Функция определяющая цвет фона и выполняющая imageconverter """

    pix = image.load()
    reds = pix[0, 0][0]
    draw = ImageDraw.Draw(image)
    if reds == 233 and formatim == 'png':
        imageconverter(draw, image.size, pix, True, formatim)
    elif reds == 235 and formatim == 'jpg':
        imageconverter(draw, image.size, pix, True, formatim)
    elif reds == 255 and formatim == 'png':
        imageconverter(draw, image.size, pix, False, formatim)
    elif reds == 255 and formatim == 'jpg':
        imageconverter(draw, image.size, pix, False, formatim)


def imageconverter(draw, size, pix, mode, formatim):
    """
    Функция перерисовывующая пиксели вотермарки в цвет фона и сохраняющая получившийся picture
    """

    if mode:
        for i in range(size[0]):
            for j in range(size[1]):
                redn = pix[i, j][0]
                booltr(redn, i, j, draw, formatim)
    else:
        for i in range(size[0]):
            for j in range(size[1]):
                redn = pix[i, j][0]
                if boolfal(redn, formatim):
                    draw.point((i, j), (255, 255, 255))


def boolfal(pixel, formatim):
    """ Функция определяющая нужные пиксели вотермарки """

    if formatim == 'png':
        return bool(pixel >= 235 and pixel != 255)
    return bool(pixel >= 228 and pixel != 255)


def booltr(pixel, i, j, draw, formatim):
    """ Функция перекрашивающая заданные пиксели вотермарки от формата """

    if formatim == 'png' and pixel > 233:
        draw.point((i, j), (233, 233, 233))
    elif formatim == 'jpg' and pixel > 231:
        draw.point((i, j), (231, 231, 231))
