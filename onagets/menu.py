import onagets.decodeString as dS

banner = """
 ____ ____ ____ _________ ____ ____ ____ ____ 
||O |||n |||a |||       |||G |||e |||t |||s ||
||__|||__|||__|||_______|||__|||__|||__|||__||
|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
"""

def brutefoce():
    channelFile = ("Répertoire du fichier contenant les canaux à bruteforce : ")
    dS.selectChannel(channelFile)
    print("[i] Canaux chargés !")
    bruteFile = input("Répertoire de l'image à BruteForce : ")
    
    

def config():
    global inMenu
    inMenu = None

def quitter():
    global inMenu 
    inMenu = None

def invalid():
   print("Choix invalide !")

menu = {
        "1":("Bruteforce", bruteforce),
        "2":('Configuration', config),
        "3":("Quit", quitter)
       }

print(banner)
print("==========Menu==========")
for key in sorted(menu.keys()):
     print(key+" => " + menu[key][0])
print("========================\n")

inMenu = True
while inMenu:
    ans = input("Choisissez une option : ")
    menu.get(ans,[None,invalid])[1]()