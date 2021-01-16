from PIL import Image

rvbDict = {}

def __charger_image(nom_image):
    pixels = []
    pic = Image.open(f"./{nom_image}")
    for x in range(0, pic.width):
        for y in range(0, pic.height):
            pixels.append(pic.getpixel((x,y)))
    return pixels, pic.width, pic.height

def __getLSB(pix):
    if(pix%2 == 0):
        return 0
    else:
        return 1
    
def __getPixelValue(pixel):
    return str(__getLSB(pixel[0])) + str(__getLSB(pixel[1])) + str(__getLSB(pixel[2]))
    
def __decodeASCII(pixels):
    decoded = []
    for p in pixels:
        decoded.append(__getPixelValue(p))
    img_bytes = ''.join(decoded)
    octets = [img_bytes[i:i+8] for i in range(0, len(img_bytes), 8)]
    return octets

def selectChannel(config):
    with open(config) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1

def bruteforce(img, channels):
    pass

