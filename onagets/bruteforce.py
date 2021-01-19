import re
from onagets import utils


def __getLSB(pix):  # si la valeur du canal est paire alors le lsb est 0 sinon c'est 1
    if(pix % 2 == 0):
        return 0
    else:
        return 1


def __getColor(channel):  # en fonction du channel on recupère la position de cette couleur dans le pixel (R, G, B) => (0, 1, 2)
    if(channel == "r"):
        return 0
    if(channel == "v" or channel == "g"):
        return 1
    if(channel == "b"):
        return 2


def __getPixelsValue(pixels, channel):
    res = ""
    for pixel in pixels:
        if "," in channel:
            for color in channel.split(","):
                res += str(__getLSB(pixel[__getColor(color)]))
        else:
            res += str(__getLSB(pixel[__getColor(channel)]))

    return res


def __binToString(binary, min_len=5):
    allStrings = []  # contient tout les string (suite de +5 caractères ASCII)
    letters = []  # liste temporaire qui contient les suites de caractères ASCII trouvés
    regex = "[ -~]"  # regex qui match les caractères ASCII

    for c in binary:
        # on recupere la valeur décimale et on la convertie en char
        octet = chr(int(c, 2))
        if re.search(regex, octet):
            letters.append(octet)
        else:
            if len(letters) > min_len:  # pour eviter d'avoir des milliers de caractères dans la liste
                allStrings.append(''.join(letters))
                letters.clear()

    return '\n'.join(allStrings)


def __decodeASCII(inputImage, channels):
    image, imageName = inputImage

    lsbValues = {}

    for channel in channels:  # initialisation du dictionnaire pour chaques canaux
        lsbValues[channel] = ""

    for channel in channels:
        lsbValues[channel] = str(lsbValues[channel]) + \
            str(__getPixelsValue(image, channel))

    for dcodChannel, value in lsbValues.items():
        strings = __binToString([value[i:i+8]
                                 for i in range(0, len(value), 8)])
        utils.saveStringsAsFile(strings, imageName, dcodChannel)

    print()


def start(config):
    inputImage = utils.loadImage(config['bruteforceFile'])
    __decodeASCII(inputImage, config['channels'])
