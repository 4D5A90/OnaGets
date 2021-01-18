from PIL import Image
import re
import os

def __charger_image(nom_image):
    pixels = []
    pic = Image.open(nom_image)
    for y in range(0, pic.height):
        for x in range(0, pic.width):
            pixels.append(pic.getpixel((x,y)))
    return pixels, pic.width, pic.height, nom_image

def __saveStrings(data, name, channel):
    base = os.path.basename(name)
    ogFileName = os.path.splitext(base)[0]
    f = open(f"./{ogFileName}_{channel.replace(',', '')}.txt", "a")
    f.write(data)
    f.close()  
    
def __getLSB(pix): #si la valeur du canal est paire alors le lsb est 0 sinon c'est 1
    if(pix%2 == 0):
        return 0
    else:
        return 1

def getColor(channel): #en fonction du channel on recupère la position de cette couleur dans le pixel (R, G, B) => (0, 1, 2)
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
                res += str(__getLSB(pixel[getColor(color)]))
        else:
            res += str(__getLSB(pixel[getColor(channel)]))
            
    return res

  
def __binToString(binary):
    allStrings = [] #contient tout les string (suite de +5 caractères ASCII)
    letters = [] #liste temporaire qui contient les suites de caractères ASCII trouvés
    regex = "[ -~]" # regex qui match les caractères ASCII
    
    for c in binary:
        octet = chr(int(c, 2)) #on recupere la valeur décimale et on la convertie en char
        if re.search(regex, octet):
            letters.append(octet)
        else:
            if len(letters) > 5 : #pour eviter d'avoir des milliers de caractères dans la liste
                allStrings.append(''.join(letters))
                letters.clear()
            
    return '\n'.join(allStrings)
        
      
def __decodeASCII(inputImage, channels):
    image, width, height, imageName = inputImage
    
    lsbValues = {}
    decodedByChannels = {}
    octets = {}
    
    for channel in channels: #initialisation du dictionnaire pour chaques canaux 
        lsbValues[channel] = ""
    
    for channel in channels:
            lsbValues[channel] = str(lsbValues[channel]) + str(__getPixelsValue(image, channel))
            
    for dcodChannel, value in lsbValues.items():
        strings = __binToString([value[i:i+8] for i in range(0, len(value), 8)])
        __saveStrings(strings, imageName, dcodChannel)

    print()


def selectChannel(config):
    allChannels = []
    with open(config) as fp:
        line = fp.readline()
        while line:
            if not "#" in line:
                allChannels.append(line.strip())
            line = fp.readline()
    return allChannels

def bruteforce(img, channels):
    inputImage = __charger_image(img)
    __decodeASCII(inputImage, channels)

