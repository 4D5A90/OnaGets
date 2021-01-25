import re
from onagets import utils
from timeit import default_timer as timer

colorDict = {"r": 0, "g": 1, "v": 1, "b": 2}


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


def __decodeASCII(config):
    image = config['bruteforceFile']['data'][config['imageOffset']                                             :config['chunkSize']]
    imageName = config['bruteforceFile']['path']
    channels = config['channels']
    lsbValues = {}

    # initialisation du dictionnaire pour chaques canaux
    for channel in channels:
        lsbValues[channel] = ""

    start = timer()
    print("[i] Démarrage du Bruteforce LSB... ")
    for channel in channels:
        print(
            f"[i] [{round(timer() - start, 2)}s] Bruteforce en cours sur le channel {channel}")
        lsbValues[channel] = str(lsbValues[channel]) + \
            str(__getPixelsValue(image, channel))

    print(
        f"[i] Bruteforce terminé en {round(timer() - start, 2)}s ! Extraction de tout les strings...")
    for dcodChannel, value in lsbValues.items():
        strings = __binToString([value[i:i+8]
                                 for i in range(0, len(value), 8)], config['minStringLen'])
        if len(config['saveDirectory']) <= 0:
            utils.saveStringsAsFile(strings, imageName, dcodChannel)
        else:
            utils.saveStringAsFileInDirectory(
                strings, imageName, config['saveDirectory'], dcodChannel)

    end = timer()
    print(f"[i] Extraction terminé ! Total : {end - start} secondes")

    # showString = utils.getAnswer(
    #     input("Voulez vous afficher tout les strings trouvé en fonctions des canaux ?"))


def start(config):
    __decodeASCII(config)
