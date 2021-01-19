from PIL import Image
import os
from time import sleep


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
    return pixels, nom_image, pic.width, pic.height


def saveStringsAsFile(data, name, channel):
    base = os.path.basename(name)
    ogFileName = os.path.splitext(base)[0]
    f = open(f"./{ogFileName}_{channel.replace(',', '')}.txt", "a")
    f.write(data)
    f.close()


def getAnswer(answer):
    ans = answer.lower()
    if ans == "o" or ans == "y":
        return True
    elif ans == "n":
        return False
    else:
        return None


def getIntAnswer(answer):
    if isStringInt(answer):
        return int(answer)
    else:
        return 5


def isStringInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# clear console fonction


def clear():
    # windows
    if os.name == 'nt':
        _ = os.system('cls')
    # mac ou linux
    else:
        _ = os.system('clear')

    sleep(2)
