from onagets import bruteforce as bF
from onagets import utils
import re

banner = """
 ____ ____ ____ _________ ____ ____ ____ ____
||O |||n |||a |||       |||G |||e |||t |||s ||
||__|||__|||__|||_______|||__|||__|||__|||__||
|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
"""

config = {
    "channels": [],
    "bruteforceFile": [],
    "minStringLen": 5,
    "moveOrder": "",
    "imageOffset": 0,
    "chunkSize": 0
}


def selectChannel(config):
    possibleOptions = {
        "2": ['rgb', 'rbg', 'grb', 'gbr', 'brg', 'bgr'],
        "3": ['bg', 'br', 'gr', 'gb', 'rg', 'rb'],
        "4": ['r', 'g', 'b']
    }

    selectedChannels = []
    channelsMsg = """
Options prédéfinies : chaques options va tenter chaques canaux, vous pouvez combiner chaques options
sauf avec l'option 1 qui elle, va ajouter tout les canaux et ignorer vos autres choix.
( ex: 2,3 va bruteforce RGB - RGB - GRB - GBR - BGR - BRG - BG - BR... etc )
( ex: 3,4 va bruteforce BG - BR - GR - GB - RG - RB - R - B - G)
( ex: 4,5 va bruteforce R - G - B en plus de votre selection manuelle (par ex: rgb;rbg;brg) )

    [1] Tous les cannaux ( 15 au total )
    [2] 3 canaux : RGB - RBG - GRB - GBR - BGR - BRG
    [3] 2 canaux : BG - BR - GR - GB - RG - RB
    [4] 1 canal : R - B - G
    [5] Selection manuelle. Format: rgb;r;bgr

Votre choix : """

    channelChoice = input(channelsMsg)
    vpChoice = set('12345')

    if "," in channelChoice and any((c in vpChoice) for c in channelChoice):
        if any((c in vpChoice) for c in channelChoice):
            if "1" in channelChoice:
                print("[i] Option 1 selectionnée, les autres choix seront ignorés...")
                for id, op in possibleOptions.items():
                    for cn in op:
                        selectedChannels.append(cn)
            else:
                for opt in channelChoice.split(","):
                    if opt == "5":
                        manualSelection = input(
                            "\n[!] Rentrez les combinaisons séparées par des points-virgules (ex: rgb;r;bgr) : ")
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
        if len(channelChoice) < 1:
            print("[i] Aucune option selectionnée, tous les canaux seront choisis")
            for id, op in possibleOptions.items():
                for cn in op:
                    selectedChannels.append(cn)
        if channelChoice == "5":
            manualSelection = input(
                "\n[!] Rentrez les combinaisons séparées par des points-virgules (ex: rgb;r;bgr) : ")
            if ";" in manualSelection:
                for comb in manualSelection.split(";"):
                    selectedChannels.append(comb)
            else:
                selectedChannels.append(manualSelection)
        else:
            if "1" in channelChoice:
                print("[i] Option 1 selectionnée, les autres choix seront ignorés...")
                for id, op in possibleOptions.items():
                    for cn in op:
                        selectedChannels.append(cn)
            else:
                if any((c in vpChoice) for c in channelChoice):
                    for choice in possibleOptions[channelChoice]:
                        selectedChannels.append(choice)

    print("\n[i] Récapitulatif des canaux selectionnés :")
    for allSelected in selectedChannels:
        print(allSelected)

    input("\nAppuyez sur n'importe quelle touche pour passer à l'étape suivante...")
    utils.clear()

    config['channels'] = selectedChannels


def selectOffset(config):
    config['imageOffset'] = utils.getIntAnswer(input(
        "[?] A partir de quel offset souhaitez vous travailler ? "), 0)
    config['chunkSize'] = utils.getIntAnswer(input(
        "[?] Sur une taille de ? "), config['bruteforceFile']['width'] * config['bruteforceFile']['height'])


def bruteforce():
    global inMenu
    inMenu = None
    askChannels = None
    imageLoaded = False
    chooseOffset = None
    while(askChannels == None):
        askChannels = utils.getAnswer(input(
            "[?] Voulez vous sélectionner manuellement les canaux à bruteforce ? [oy/OY/nN] : "))
        if askChannels:
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

    while not imageLoaded:
        try:
            config['bruteforceFile'] = utils.loadImage(input(
                "[?] Répertoire de l'image à BruteForce : "))
            imageLoaded = True
            print("[i] Image chargée avec succès !")
            print(
                f"   - Taille: {config['bruteforceFile']['width']} x {config['bruteforceFile']['height']}\r\n   - Pixels : {config['bruteforceFile']['width'] * config['bruteforceFile']['height']}")
        except Exception:
            print("[!] Erreur lors du chargement de l'image ! Veuillez recommencer...")

    while chooseOffset == None:
        chooseOffset = utils.getAnswer(
            input("[?] Voulez vous travailler sur un echantillon de l'image ? [oy/OY/nN] : "))
        if chooseOffset:
            selectOffset(config)
        else:
            config['chunkSize'] = config['bruteforceFile']['width'] * \
                config['bruteforceFile']['height']

    config['minStringLen'] = utils.getIntAnswer(input(
        "[?] Taille minimale des string à extraire ? (défaut: 5) : "), 5)
    # bruteFile = '/Users/hugo/BSI/dev/python/Ona Gets/images/ctf1.png'
    # config['bruteforceFile'] = "C:\\Users\\Admin\\source\\vscode\\OnaGets\\images\\ctf1.png"
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
    # ans = input("Choisissez une option : ")
    ans = "1"
    menu.get(ans, [None, invalid])[1]()
