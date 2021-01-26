from PIL import Image
import os
from time import sleep
import sys


# fonction utile dans le cas ou un fichier de config est utilisé (voir exemple : config_rvb)
def selectChannel(config):
    allChannels = []
    with open(config) as fp:
        line = fp.readline()
        while line:
            if not "#" in line:
                allChannels.append(line.strip())
            line = fp.readline()
    return allChannels


def loadImage(nom_image):
    pixels = []
    pic = Image.open(nom_image)
    for y in range(0, pic.height):
        for x in range(0, pic.width):
            pixels.append(pic.getpixel((x, y)))
    return {"data": pixels, "path": nom_image, "width": pic.width, "height": pic.height}


def saveStringsAsFile(data, name, channel):
    base = os.path.basename(name)
    ogFileName = os.path.splitext(base)[0]
    f = open(f"./{ogFileName}_{channel.replace(',', '')}.txt", "a")
    f.write(data)
    f.close()
    print(
        f"[i] Fichier {ogFileName}_{channel.replace(',', '')}.txt sauvegardé dans le même dossier que le script")


def saveStringAsFileInDirectory(data, name, path, channel):
    base = os.path.basename(name)
    ogFileName = os.path.splitext(base)[0]
    saveFile = joinPath(path, f"{ogFileName}_{channel.replace(',', '')}.txt")
    f = open(saveFile, "a")
    f.write(data)
    f.close()
    print(
        f"[i] Fichier {ogFileName}_{channel.replace(',', '')}.txt sauvegardé dans {saveFile}")


def getAnswer(answer):
    ans = answer.lower()
    if ans == "o" or ans == "y":
        return True
    elif ans == "n":
        return False
    else:
        return None


def getIntAnswer(answer, default):
    if isStringInt(answer):
        return int(answer)
    else:
        return default


def isStringInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# clear console fonction


def isPathWriteable(filepath):
    try:
        filehandle = open(filepath, 'w')
    except IOError:
        return False
    return True


def joinPath(path, join):
    return os.path.join(path, join)


def safeRemoveFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("[!] Erreur lors de la destruction du fichier temporaire")


def clear():
    sleep(2)
    # windows
    if os.name == 'nt':
        _ = os.system('cls')
    # mac ou linux
    else:
        _ = os.system('clear')
