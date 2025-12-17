import tkinter as tk
from model import *  # Importer toutes les fonctions du modèle

def afficher_plateau(plateau):
    """
    Affiche le plateau 16x16 avec fleurs, abeilles, ruches
    """
    fenetre = tk.Tk()
    fenetre.title("Jeu des Abeilles")
    
    canvas = tk.Canvas(fenetre, width=640, height=640, bg="black")
    canvas.pack()
    
    taille_case = 40
    
    # Dessiner le quadrillage
    for i in range(NCASES + 1):
        canvas.create_line(0, i*taille_case, 640, i*taille_case, fill="gray")
        canvas.create_line(i*taille_case, 0, i*taille_case, 640, fill="gray")
    
    # Dessiner les éléments du plateau
    # for x in range(NCASES):
    #     for y in range(NCASES):
    #         case = plateau[x][y]
            
    #         if isinstance(case, dict):
    #             dessiner_ruche(canvas, x, y, taille_case, case)
    #         elif isinstance(case, list):
    #             for element in case:
    #                 if isinstance(element, dict):
    #                     if element.get("type") == "ruche":
    #                         dessiner_ruche(canvas, x, y, taille_case, element)
    #                     elif element.get("type") == "abeille":
    #                         dessiner_abeille(canvas, x, y, taille_case, element)
    #                     elif "id" in element and element["id"].startswith("fleur"):
    #                         dessiner_fleur(canvas, x, y, taille_case, element)
    
    fenetre.mainloop()



# Lancer le jeu
if __name__ == "__main__":
    # Initialiser le jeu
    plateau = creer_plateau()

    
    # Afficher
    afficher_plateau(plateau)
