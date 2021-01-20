import re
from onagets import utils
from timeit import default_timer as timer

colorDict = {"r": 0, "g": 1, "v": 1, "b": 2}

# def __getLSB(pix):  # si la valeur du canal est paire alors le lsb est 0 sinon c'est 1
#     return pix % 2
# def __getColor(channel):  # en fonction du channel on recupère la position de cette couleur dans le pixel (R, G, B) => (0, 1, 2)
#     return colorDict[channel]


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


def __getPixelsValue(pixels, channel):
    res = ""
    for pixel in pixels:
        for color in channel:
            res += str(pixel[colorDict[color]] % 2)
    return res


def __decodeASCII(inputImage, channels):
    image, imageName, width, height = inputImage

    lsbValues = {}

    for channel in channels:  # initialisation du dictionnaire pour chaques canaux
        lsbValues[channel] = ""

    start = timer()
    print("[i] Démarrage du Bruteforce LSB... ")
    for channel in channels:
        print(
            f"[i] [{round(timer() - start, 2)}s] Bruteforce en cours sur le channel {channel}")
        lsbValues[channel] = str(lsbValues[channel]) + \
            str(__getPixelsValue(image, channel))

    print(
        f"[i] [{round(timer() - start, 2)}s] Bruteforce terminé ! Extraction de tout les strings...")
    for dcodChannel, value in lsbValues.items():
        strings = __binToString([value[i:i+8]
                                 for i in range(0, len(value), 8)])
        utils.saveStringsAsFile(strings, imageName, dcodChannel)

    end = timer()
    print(f"[i] Bruteforce terminé ! Cela à pris {end - start} secondes")


def start(config):
    inputImage = utils.loadImage(config['bruteforceFile'])
    __decodeASCII(inputImage, config['channels'])
