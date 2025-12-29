
#modèle du jeu
import random

NCASES = 16 #taille du plateau
NECTAR_INITIAL = 10 #nectar de départ
MAX_NECTAR = 45 #max nectar par fleur
COUT_PONTE = 5 #coût d'une abeille
TIME_OUT = 300 #nombre max de tours
TIME_KO = 5 #nombre de tours qu'une abeille KO reste KO
NFLEURS = 4 #nombre de fleur placé

CAPACITE_NECTAR = {
    "bourdon": 1,
    "eclaireuse": 3,
    "ouvriere": 12
}

FORCE = {
    "eclaireuse": 1,
    "ouvriere": 1,
    "bourdon": 5
}


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
        "etat": "OK",
        "a_bouge": False,
        "tours_ko_restants": 0
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


#butinage

def fleurs_accessibles(plateau, x,y):
    """ 
    sert à répondre ceci : Quelle fleurs est accessible pour l'abeille ?
    """
    fleurs = [] #contient tous les fleurs accessibles
    for dx in [-1, 0, 1]:  #axe verticale
        for dy in [-1, 0, 1]: #axe horizontale cherche sur les 8 directions
            nx, ny = x + dx, y + dy #calcul de la position réelle de la case
            if 0 <= nx < NCASES and 0 <= ny < NCASES: #éviter de sortir du plateau
                for element in plateau[nx][ny]:
                    if element["type"] == "fleur":
                        fleurs.append(element)
    return fleurs


def gain_nectar(fleur):
    """
    défini combien de nectar l'abeille va prendre si celle ci choisi de butiner
    le paramètre passé est une fleur "accessible"
    """
    if fleur["nectar"] >= (2* MAX_NECTAR) / 3:
        return 3
    elif fleur["nectar"] > MAX_NECTAR / 3:
        return 2
    return 1 
    
def butiner(abeille, fleur):
    """
    Permet à une abeille de récolter du nectar si elle est sur 
    une fleur ou adjacente à celle-ci.
    Le surplus non transportable est perdu (vandalisme).
    """
    #Capacité max selon le rôle
    max_cap = CAPACITE_NECTAR[abeille["role"]]

    #Gain potentiel de la fleur
    gain = gain_nectar(fleur)

    #Place restante dans l'abeille
    place_restante = max_cap - abeille["nectar"]

    #Quantité réellement stockée (peut être moins que le gain)
    pris = min(gain, place_restante)

    # Mettre à jour
    abeille["nectar"] += pris
    fleur["nectar"] -= gain  #La fleur perd TOUT le gain (vandalisme si surplus)

    return pris  #retourne ce qui a été stocké (pour voir uniquement)

def peut_butiner(abeille, plateau):
    """
    Vérifie si l'abeille peut butiner et retourne les fleurs accessibles
    """
    # L'abeille ne doit pas avoir bougé ce tour
    if abeille["a_bouge"]:
        return []
    
    x, y = abeille["position"]
    return fleurs_accessibles(plateau, x, y)

def tour_butinage(abeille, plateau):
    """
    Gère le butinage d'une abeille pendant son tour
    Le joueur choisit quelle fleur butiner parmi celles accessibles
    """
    fleurs_dispo = peut_butiner(abeille, plateau)
    
    if not fleurs_dispo:
        return None  # Pas de butinage possible
    
    # ICI : Le joueur doit choisir quelle fleur
    # Pour l'instant, on prend la première (à améliorer avec interface)
    fleur_choisie = fleurs_dispo[0]
    
    # Butiner la fleur choisie
    pris = butiner(abeille, fleur_choisie)
    
    return pris

def deposer_nectar(abeille, ruche, plateau):
    """
    Si l'abeille est dans la zone 4x4 de sa ruche, elle dépose son nectar
    """
    x, y = abeille["position"]
    
    # Vérifier si dans une zone 4x4 aux coins
    zone_protegee = 4
    N = len(plateau)
    
    dans_zone = False
    # Coin haut-gauche
    if x < zone_protegee and y < zone_protegee:
        dans_zone = True
    # Coin haut-droite
    elif x < zone_protegee and y >= N - zone_protegee:
        dans_zone = True
    # Coin bas-gauche
    elif x >= N - zone_protegee and y < zone_protegee:
        dans_zone = True
    # Coin bas-droite
    elif x >= N - zone_protegee and y >= N - zone_protegee:
        dans_zone = True
    
    if dans_zone and abeille["camp"] == ruche["id"]:
        ruche["nectar"] += abeille["nectar"]
        abeille["nectar"] = 0







#ESCARMOUCHE

def trouver_opposantes(plateau, abeille):
    """ 
    Détermine s'il y a des ennemis dans son rayon (8 cases adjacentes)
    """
    opposantes = []  # Contient toutes les abeilles ennemies
    x, y = abeille["position"]
    
    for dx in [-1, 0, 1]:  #Axe vertical
        for dy in [-1, 0, 1]:  #Axe horizontal, cherche dans les 8 directions
            if dx == 0 and dy == 0:  #ignorer la case de l'abeille elle-même
                continue
                
            nx, ny = x + dx, y + dy  #Calcul de la position réelle de la case
            if 0 <= nx < NCASES and 0 <= ny < NCASES:  #éviter de sortir du plateau
                for element in plateau[nx][ny]:
                    if element["type"] == "abeille" and element["camp"] != abeille["camp"]:
                        opposantes.append(element)
    return opposantes

def calculer_force_effective(abeille, opposantes):
    """
    Calcule la force effective : FE = F(force de l'abeille) / nombre_opposantes
    """
    force = FORCE[abeille["role"]]
    nb_opposantes = len(opposantes)
    
    if nb_opposantes == 0:
        return force  #pas d'opposantes = force complète
    
    return force / nb_opposantes


def calculer_proba_esquive(abeille, opposantes, plateau):
    """
    Calcule la probabilité d'esquive d'une abeille
    proba = F / (F + somme des FE ennemies)
    """
    force = FORCE[abeille["role"]]
    
    #calculer la somme des FE des opposantes
    somme_fe_ennemies = 0
    for opposante in opposantes:
        # Pour chaque opposante, trouver ses opposantes pour calculer sa FE
        opposantes_de_opposante = trouver_opposantes(plateau, opposante)
        fe = calculer_force_effective(opposante, opposantes_de_opposante)
        somme_fe_ennemies += fe
    
    #probabilité d'esquive
    if force + somme_fe_ennemies == 0:
        return 1.0  #sécurité (ne devrait pas arriver)
    
    return force / (force + somme_fe_ennemies)

def phase_escarmouche(plateau, ruche):
    """
    Gère la phase d'escarmouche pour une ruche
    1. Calcule toutes les probas d'esquive
    2. Tire au hasard pour chaque abeille
    3. Applique les conséquences simultanément
    """
    resultats = []  #list des (abeille, esquive_reussie)
    
    for abeille in ruche["abeilles"]:
        if abeille["etat"] != "OK":
            continue
        
        #trouver les opposantes
        opposantes = trouver_opposantes(plateau, abeille)
        
        if len(opposantes) == 0:
            continue  # Pas d'escarmouche
        
        #calculer proba d'esquive
        proba = calculer_proba_esquive(abeille, opposantes, plateau)
        
        # tirer au hasard
        tirage = random.random()  # Nombre entre 0 et 1
        esquive_reussie = tirage < proba
    
    # Stocker juste True ou False dans un dictionnaire
        resultat = {
            "abeille": abeille,
            "esquive": esquive_reussie
        }
        resultats.append(resultat)
    
    # Appliquer les conséquences simultanément
    for resultat in resultats:
        abeille = resultat["abeille"]
        esquive_reussie = resultat["esquive"]
        
        if not esquive_reussie:
            # Esquive ratée !
            abeille["nectar"] = 0
            abeille["etat"] = "KO"
            abeille["tours_ko_restants"] = TIME_KO

#tour


def tour_abeille(plateau, abeille, ruche):
    """
    Joue le tour d'une abeille
    """
    # Décrémenter le compteur KO
    if abeille["etat"] == "KO":
        abeille["tours_ko_restants"] -= 1
        if abeille["tours_ko_restants"] <= 0:
            abeille["etat"] = "OK"
        return  # L'abeille reste KO ce tour
    
    if abeille["etat"] != "OK":
        return

    # Réinitialiser le flag a_bouge au début du tour
    abeille["a_bouge"] = False

    # pour l'instant : déplacement aléatoire (TEMPORAIRE)
    x, y = abeille["position"]
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    dx, dy = random.choice(directions)

    x_new = max(0, min(NCASES-1, x + dx))
    y_new = max(0, min(NCASES-1, y + dy))

    deplacer_abeille(plateau, abeille, (x_new, y_new))
    
    # Après déplacement, tenter de butiner
    tour_butinage(abeille, plateau)
    
    # Déposer le nectar si dans la zone de la ruche
    deposer_nectar(abeille, ruche, plateau)

def tour_ruche(plateau, ruche):
    """
    Joue le tour complet d'une ruche
    """
    for abeille in ruche["abeilles"]:
        tour_abeille(plateau, abeille, ruche)
    
    # Phase d'escarmouche
    phase_escarmouche(plateau, ruche)


def tour_jeu(plateau, ruches, tour):
    print(f"--- TOUR {tour} ---")
    for ruche in ruches:
        tour_ruche(plateau, ruche)


def lancer_partie():
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)

    # Créer 2 abeilles ennemies proches pour tester l'escarmouche
    abeille1 = pondre(ruches[0], "ouvriere", (5, 5))
    if abeille1:
        placer_abeille(plateau, abeille1)
    
    abeille2 = pondre(ruches[1], "bourdon", (5, 6))  # Adjacent à abeille1
    if abeille2:
        placer_abeille(plateau, abeille2)
    
    # Jouer quelques tours pour voir les escarmouches
    for tour in range(1, 10):  # Juste 10 tours pour tester
        print(f"\n--- TOUR {tour} ---")
        for ruche in ruches:
            tour_ruche(plateau, ruche)
        
        # Afficher l'état des abeilles
        print(f"Abeille1: etat={abeille1['etat']}, nectar={abeille1['nectar']}, pos={abeille1['position']}")
        print(f"Abeille2: etat={abeille2['etat']}, nectar={abeille2['nectar']}, pos={abeille2['position']}")
    
lancer_partie()




