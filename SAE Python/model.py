
#modèle du jeu
import random

NCASES = 16 #taille du plateau
NECTAR_INITIAL = 10 #nectar de départ
MAX_NECTAR = 45 #max nectar par fleur
COUT_PONTE = 5 #coût d'une abeille
TIME_OUT = 300 #nombre max de tours
TIME_KO = 5 #nombre de tours qu'une abeille KO reste KO
NFLEURS = 4 #nombre de fleur placé

#Niveau 1 
def creer_plateau():
    """
    crée un plateau vide : chaque case doit être une liste vide pour contenir plusieurs éléments
    avec les paramètres pour savoir les positions plus tard.
    On veut un truc comme ça :
    [0,0] [0,1] [0,2] ... [0,15]
    [1,0] [1,1] [1,2] ... [1,15]
    ...
    [15,0] ...            [15,15]

    On va d'ailleurs aussi stocker les ruches et fleurs ici directement
    """
    plateau = []
    for _ in range(NCASES):
        ligne = []
        for _ in range(NCASES):
            ligne.append([])  # chaque case = liste vide
        plateau.append(ligne)

    return plateau

def creer_ruche(plateau):
    """
    On veut crée les 4 ruches dans les coins de la map 
    en insérant des dictionnaires dans le plateau (list)

    Les settings donné aux ruches sont : type, id, nectar et nombre d'abeille
    """
    ruche0 = {
        "type": "ruche",
        "id": "ruche0",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche1 = {
        "type": "ruche",
        "id": "ruche1",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche2 = {
        "type": "ruche",
        "id": "ruche2",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    ruche3 = {
        "type": "ruche",
        "id": "ruche3",
        "nectar": NECTAR_INITIAL,
        "abeilles": []
    }
    # Placer les ruches dans les coins
    plateau[0][0].append(ruche0)
    plateau[0][NCASES-1].append(ruche1)
    plateau[NCASES-1][0].append(ruche2)
    plateau[NCASES-1][NCASES-1].append(ruche3)

    ruches = [ruche0, ruche1, ruche2, ruche3]
    return ruches



def creer_fleurs(NFLEURS=4):
    """
    Crée des fleurs avec leur nectar (initialisé à 0 pour l'instant qu'on va changer dans la fonction placer_fleurs) et position (initialement None)
    Le nectar est attribué entre 1 et MAX_NECTAR.
    """
    fleurs = []
    for i in range(NFLEURS):
        fleurs.append({
            "type": "fleur",
            "id": f"fleur{i}",
            "nectar": 0,
            "position": None
        })
    return fleurs



def placer_fleurs(plateau, fleurs):
    """
    Place les fleurs symétriquement sur le plateau en respectant les zones protégées (4x4) aux coins
    et l'unicité des fleurs.
    Le nectar est attribué entre 1 et MAX_NECTAR.
    """
    N = len(plateau)
    zone_protegee = 4

    for fleur in fleurs:
        position_valide = False

        while position_valide == False:
            x = random.randint(0, N//2)
            y = random.randint(0, N//2)

            # coin haut-gauche
            if x < zone_protegee and y < zone_protegee:
                continue
            else:
                position_valide = True
                nectar = random.randint(1, MAX_NECTAR)
                
                # Mettre à jour la fleur de base
                fleur["nectar"] = nectar
                fleur["position"] = (x, y)
                
                # Créer 3 autres fleurs distinctes pour les positions symétriques restantes
                fleur2 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (N-1-x, y)}
                fleur3 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (x, N-1-y)}
                fleur4 = {"type": "fleur", "id": fleur["id"], "nectar": nectar, "position": (N-1-x, N-1-y)}
                
                # Placer les 4 fleurs
                plateau[x][y].append(fleur)
                plateau[N-1-x][y].append(fleur2)
                plateau[x][N-1-y].append(fleur3)
                plateau[N-1-x][N-1-y].append(fleur4)


def creer_abeille(type_abeille, position, camp):
    """
    Crée une abeille avec son type, position, son état et son nectar (0)
    """
    abeille = {
        "type": "abeille",
        "role": type_abeille,
        "camp": camp,
        "position": position,
        "nectar": 0,
        "etat": "OK"
    }
    return abeille


def placer_abeille(plateau, abeille):
    """
    Placer les abeilles crée sur le plateau
    """
    x, y = abeille["position"]
    plateau[x][y].append(abeille)


def pondre(ruche,type_abeille,position):
    """
    Gère le nectar pour une ruche
    """
    if ruche["nectar"] >= COUT_PONTE:
        ruche["nectar"] -= COUT_PONTE
        abeille = creer_abeille(type_abeille,position,ruche["id"])
        ruche["abeilles"].append(abeille)
        return abeille
    else:
        return False

def deplacer_abeille(plateau, abeille, nouvelle_position):
    x_old, y_old = abeille["position"]
    x_new, y_new = nouvelle_position

    plateau[x_old][y_old].remove(abeille)
    abeille["position"] = (x_new, y_new)
    plateau[x_new][y_new].append(abeille)

def tour_abeille(plateau, abeille):
    """
    Joue le tour d'une abeille
    """
    if abeille["etat"] != "OK":
        return

    # pour l'instant : déplacement aléatoire (TEMPORAIRE)
    x, y = abeille["position"]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    dx, dy = random.choice(directions)

    x_new = max(0, min(NCASES-1, x + dx))
    y_new = max(0, min(NCASES-1, y + dy))

    deplacer_abeille(plateau, abeille, (x_new, y_new))

def tour_ruche(plateau, ruche):
    """
    Joue le tour complet d'une ruche
    """
    for abeille in ruche["abeilles"]:
        tour_abeille(plateau, abeille)


def tour_jeu(plateau, ruches, tour):
    print(f"--- TOUR {tour} ---")
    for ruche in ruches:
        tour_ruche(plateau, ruche)

def lancer_partie():
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)

    # pondre 1 abeille par ruche
    for ruche in ruches:
        abeille = pondre(ruche, "ouvriere", (0,0))
        if abeille:
            placer_abeille(plateau, abeille)

    for tour in range(1, TIME_OUT + 1):
        tour_jeu(plateau, ruches, tour)
    





