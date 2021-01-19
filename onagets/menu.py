from onagets import bruteforce as bF
from onagets import utils
import re

banner = r"""
 ____ ____ ____ _________ ____ ____ ____ ____ 
||O |||n |||a |||       |||G |||e |||t |||s ||
||__|||__|||__|||_______|||__|||__|||__|||__||
|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
"""

config = {
    "channels": [],
    "bruteforceFile": "",
    "minStringLen": 5,
    "moveOrder": "",
    "imageOffset": ""
}


def selectChannel(config):
    possibleOptions = {
        "1": ['r,g,b', 'r,b,g', 'g,r,b', 'g,b,r', 'b,r,g', 'b,g,r'],
        "2": ['b,g', 'b,r', 'g,r', 'g,b', 'r,g', 'r,b'],
        "3": ['r', 'g', 'b']
    }

    selectedChannels = []
    channelsMsg = r"""
Options prédéfinies : chaques options va tenter chaques canaux
(ex: 1,2 va bruteforce RGB - RGB - GRB - GBR - BGR - BRG - BG - BR... etc )
(ex: 2,3 va bruteforce BG - BR - GR - GB - RG - RB - R - B - G)

    [1] 3 canaux : RGB - RBG - GRB - GBR - BGR - BRG
    [2] 2 canaux : BG - BR - GR - GB - RG - RB
    [3] 1 canal : R - B - G

Sinon choissisez l'option 4 pour saisir manuellement les canaux :
(ex: canaux séparés par des virgules et chaques combinaisons séparées par des points-virgules)
    [4] Selection manuelle. Format: r,g,b;r;b,g,r

Votre choix : """

    channelChoice = input(channelsMsg)
    vpChoice = set('1234')

    if "," in channelChoice:
        if any((c in vpChoice) for c in channelChoice):
            for opt in channelChoice.split(","):
                if opt == "4":
                    manualSelection = input(
                        "\n[!] Rentrez les combinaisons séparées par des points-virgules (ex: r,g,b;r;b,g,r) : ")
                    if ";" in manualSelection:
                        for comb in manualSelection.split(";"):
                            selectedChannels.append(comb)
                    else:
                        selectedChannels.append(manualSelection)
                else:
                    print(
                        f"[+] {possibleOptions[opt]} ajouté aux canaux à bruteforce")
                    for choice in possibleOptions[opt]:
                        selectedChannels.append(choice)
    else:
        if any((c in vpChoice) for c in channelChoice):
            for choice in possibleOptions[channelChoice]:
                selectedChannels.append(choice)

    print("\n[i] Récapitulatif des canaux selectionnés :")
    for allSelected in selectedChannels:
        print(allSelected)

    input("\nAppuyez sur ENTRER pour continuer...")
    utils.clear()

    config['channels'] = selectedChannels


def bruteforce():
    global inMenu
    inMenu = None
    askChannels = None
    while(askChannels == None):
        askChannels = utils.getAnswer(input(
            "{?] Voulez vous sélectionner manuellement les canaux à bruteforce ? [oy/OY/nN] : "))
        if askChannels == True:
            selectChannel(config)
        elif askChannels == False:
            loadChannel = utils.getAnswer(input(
                "[?] Voulez vous sélectionner un fichier contenant tout les canaux à bruteforce ? [oy/OY/nN] : "))
            if loadChannel:
                config['channels'] = utils.selectChannel(
                    input("Répertoire du fichier de config : "))
                print("[i] Canaux chargés !")
            else:
                askChannels = None
        else:
            print("[!] Choix incorrect, merci de recommencer")

    config['bruteforceFile'] = input(
        "[?] Répertoire de l'image à BruteForce : ")

    config['minStringLen'] = utils.getIntAnswer(input(
        "[?] Taille minimale des string à extraire ? (défaut: 5) : "))
    #bruteFile = '/Users/hugo/BSI/dev/python/Ona Gets/images/ctf1.png'
    #config['bruteforceFile'] = "C:\\Users\\Admin\\source\\vscode\\OnaGets\\images\\ctf1.png"
    bF.start(config)


def quitter():
    global inMenu
    inMenu = None


def invalid():
    print("[!] Choix invalide !")


menu = {
    "1": ("Bruteforce", bruteforce),
    "2": ('Configuration', config),
    "3": ("Quitter", quitter)
}

print(banner)
print("==========Menu==========")
for key in sorted(menu.keys()):
    print(key+" => " + menu[key][0])
print("========================\n")

inMenu = True
while inMenu:
    #ans = input("Choisissez une option : ")
    ans = "1"
    menu.get(ans, [None, invalid])[1]()
