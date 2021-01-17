from PIL import Image

def __charger_image(nom_image):
    pixels = []
    pic = Image.open(nom_image)
    for x in range(0, pic.width):
        for y in range(0, pic.height):
            pixels.append(pic.getpixel((x,y)))
    return pixels, pic.width, pic.height

def __save_image(nom_image, hauteur, largeur, pixels, prefix= "modified_"):
    pic = Image.new('RGB', (largeur, hauteur), (255, 255, 255))
    for num_column in range(0, len(pixels)//hauteur):
        start = num_column * hauteur
        stop = start + hauteur
        column = pixels[start : stop]
        for num_ligne in range(len(column)):
            pic.putpixel((num_column, num_ligne), tuple(column[num_ligne]))
    pic.save(nom_image)

def __getLSB(pix):
    if(pix%2 == 0):
        return 0
    else:
        return 1

def getColor(channel):
    if(channel == "r"):
        return 0
    if(channel == "v" or channel == "g"):
        return 1
    if(channel == "b"):
        return 2

def __getPixelValue(pixel, channels):
    channelDict = {}
    pixelValue = []
    for colors in channels:
        for key in colors:
            pixelValue.append(str(__getLSB(pixel[getColor(key)])))
        channelDict[','.join(colors)] = pixelValue.copy()
        pixelValue.clear()
    return channelDict
    #return str(__getLSB(pixel[0])) + str(__getLSB(pixel[1])) + str(__getLSB(pixel[2]))
    
def __decodeASCII(inputImage, channels):
    image, width, height = inputImage
    
    decoded = []
    decodedByChannels = {}
    octets = []
    
    for pixels in image:
        decoded.append(__getPixelValue(pixels, channels))

    tempBits = []
    for allChannelsBytes in decoded:
        for channels, value in allChannelsBytes.items():
                for bits in value:
                    if channels in decodedByChannels:
                        decodedByChannels[channels] = str(decodedByChannels[channels]) + str(bits)
                    else:
                        decodedByChannels[channels] = bits

    for channel, channelValue in decodedByChannels.items():
       octets.append([channelValue[i:i+8] for i in range(0, len(channelValue), 8)])
       
    index = 0
    for i in octets:
        __save_image(f"./{index}.png", height, width, i)
    pass
    #octets = 
    #return octets

def selectChannel(config):
    allChannels = []
    with open(config) as fp:
        line = fp.readline()
        while line:
            if not "#" in line:
                allChannels.append(line.strip().split(","))
            line = fp.readline()
    return allChannels

def bruteforce(img, channels):
    inputImage = __charger_image(img)
    __decodeASCII(inputImage, channels)

