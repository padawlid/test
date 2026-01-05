from tkinter import *
from model import *



def dessiner_zones_protegees(canvas, taille_case, width, height):
    zone_size = 4 * taille_case
    
    # Coin haut-gauche
    canvas.create_rectangle(0, 0, zone_size, zone_size, fill="lightblue", outline="")
    
    # Coin haut-droite
    canvas.create_rectangle(width - zone_size, 0, width, zone_size, fill="#FF5967", outline="")
    
    # Coin bas-gauche
    canvas.create_rectangle(0, height - zone_size, zone_size, height, fill="lightgreen", outline="")
    
    # Coin bas-droite
    canvas.create_rectangle(width - zone_size, height - zone_size, width, height, fill="yellow", outline="")



def dessiner_quadrillage(canvas, width, height, taille_case):
    """Dessiner le quadrillage"""
    for i in range(NCASES + 1): #+1 car on a besoin de (NCASES + 1) ligne pour NCASES de case

        canvas.create_line(0, i*taille_case, width, i*taille_case, fill="black")
        canvas.create_line(i*taille_case, 0, i*taille_case, height,fill="black")



def dessiner_ruche(canvas, x, y, taille_case, image):
    #Calculer le centre de la case (x, y)
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    
    #Placer l'image au centre
    canvas.create_image(centre_x, centre_y, image=image)



def dessiner_fleur(canvas, x, y, taille_case, image):
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)


def dessiner_abeille(canvas,x,y,taille_case,image):
    centre_x = y * taille_case + taille_case // 2
    centre_y = x * taille_case + taille_case // 2
    canvas.create_image(centre_x,centre_y, image=image)


def dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille):
    """
    Parcourt le plateau et dessine chaque élément
    """
    
    for x in range(NCASES):
        for y in range(NCASES):
            case = plateau[x][y]  # Liste d'éléments
            
            # Parcourir tous les éléments de la case
            for element in case:
                if type(element) is dict: #Vérifier si c'est une liste ou un dict direct
                    if element["type"] == "ruche":
                        dessiner_ruche(canvas, x, y, taille_case, image_ruche)
                    elif element["type"] == "fleur":
                        dessiner_fleur(canvas, x, y, taille_case, image_fleur)
                    elif element["type"] == "abeille":
                        dessiner_abeille(canvas, x, y, taille_case, image_abeille)


def afficher_plateau_anime(plateau, ruches, tour_actuel):
    fenetre = Tk()
    fenetre.title("BZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ 🐝")
    fenetre.geometry("1270x890")
    fenetre.minsize(1270, 890)
    fenetre.maxsize(1270, 890)
    
    
    #charger images
    image_ruche = PhotoImage(file="image/ruche.png").subsample(10, 10)
    image_fleur = PhotoImage(file="image/fleur.png").subsample(10, 10)
    image_abeille = PhotoImage(file="image/abeille.png").subsample(10, 10)
    
    width = 700
    height = width
    taille_case = width / NCASES
    
    #variables
    joueur_actuel = 0
    phase = "ponte"
    abeille_cliquee = None
    POSITIONS_RUCHES = {0: (0,0), 
                        1: (0,15), 
                        2: (15,0), 
                        3: (15,15)}

    #interface
    label_tour = Label(fenetre, text="", font=("Arial", 16))
    label_tour.grid(row=0, column=0, columnspan=3, sticky="ew")
    
    label_phase = Label(fenetre, text="", font=("Arial", 12, "bold"), bg="#FF54D0", fg="white", pady=5)
    label_phase.grid(row=1, column=0, columnspan=3, sticky="ew")
    
    # Plateau au centre
    canvas = Canvas(fenetre, width=width, height=height, bg="green")
    canvas.grid(row=2, column=1, padx=10, pady=10)
    
    # Infos ruches gauche (ruches du côté gauche du plateau)
    frame_gauche = Frame(fenetre, width=250)
    frame_gauche.grid(row=2, column=0, sticky="ns", padx=10)

    # Ruche 0 (haut-gauche) en haut
    label_ruche0 = Label(frame_gauche, text="", bg="lightblue", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche0.pack(pady=15, padx=5, fill="both", expand=True)

    # Ruche 2 (bas-gauche) en bas
    label_ruche2 = Label(frame_gauche, text="", bg="lightgreen", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche2.pack(pady=15, padx=5, fill="both", expand=True)

    # Infos ruches droite (ruches du côté droit du plateau)
    frame_droite = Frame(fenetre, width=250)
    frame_droite.grid(row=2, column=2, sticky="ns", padx=10)

    # Ruche 1 (haut-droite) en haut
    label_ruche1 = Label(frame_droite, text="", bg="#FF5967", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche1.pack(pady=15, padx=5, fill="both", expand=True)

    # Ruche 3 (bas-droite) en bas
    label_ruche3 = Label(frame_droite, text="", bg="yellow", font=("Arial", 14, "bold"), 
                        width=25, height=12, relief="solid", borderwidth=2)
    label_ruche3.pack(pady=15, padx=5, fill="both", expand=True)

    labels_ruches = [label_ruche0, label_ruche1, label_ruche2, label_ruche3]
    
    # Frame pour boutons et messages
    frame_bas = Frame(fenetre)
    frame_bas.grid(row=3, column=0, columnspan=3, pady=10)
    
    label_message = Label(frame_bas, text="", font=("Arial", 10), fg="red")
    label_gagnant = Label(fenetre, text="", font=("Arial", 16), fg="green")
    label_gagnant.grid(row=4, column=0, columnspan=3)
    
    # ===== FONCTIONS LOCALES =====
    
    def message(texte, couleur="red"):
        label_message.config(text=texte, fg=couleur)
        fenetre.after(2000, lambda: label_message.config(text=""))
    
    def pondre(type_abeille):
        ruche = ruches[joueur_actuel]
        pos = POSITIONS_RUCHES[joueur_actuel]
        
        abeille, erreur = tenter_ponte(plateau, ruche, type_abeille, pos) #abeille est inutile ici
        if erreur:
            message(erreur)
            return
        
        message(f"{type_abeille} pondue !", "green")
        redessiner()
    
    def executer_escarmouche():
        nonlocal joueur_actuel, phase, tour_actuel
        
        phase_escarmouche(plateau, ruches[joueur_actuel])
        
        joueur_actuel = (joueur_actuel + 1) % 4
        
        if joueur_actuel == 0:
            tour_actuel += 1
            nouveau_tour(ruches)
        
        phase = "ponte"
        
        if tour_actuel >= TIME_OUT:
            gagnant = determiner_gagnant(ruches)
            label_gagnant.config(text=f"🏆 {gagnant['id']} GAGNE avec {gagnant['nectar']} nectar ! 🏆")
            return
        
        redessiner()
    
    def passer_phase():
        nonlocal joueur_actuel, phase, tour_actuel, abeille_cliquee
        
        abeille_cliquee = None
        
        if phase == "ponte":
            phase = "mouvement"
            if not any(a["etat"] == "OK" for a in ruches[joueur_actuel]["abeilles"]):
                passer_phase()
                return
        
        elif phase == "mouvement":
            phase = "butinage"
            if not any(not a["a_bouge"] and a["etat"] == "OK" for a in ruches[joueur_actuel]["abeilles"]):
                passer_phase()
                return
        
        elif phase == "butinage":
            phase = "escarmouche"
            redessiner()
            fenetre.after(500, executer_escarmouche)
            return
        
        redessiner()
    
    def redessiner():
        canvas.delete("all")
        dessiner_zones_protegees(canvas, taille_case, width, height)
        dessiner_quadrillage(canvas, width, height, taille_case)
        dessiner_plateau(canvas, plateau, taille_case, image_ruche, image_fleur, image_abeille)
        
        if abeille_cliquee:
            x, y = abeille_cliquee["position"]
            cx = y * taille_case + taille_case / 2
            cy = x * taille_case + taille_case / 2
            canvas.create_oval(cx-20, cy-20, cx+20, cy+20, outline="red", width=3)
        
        label_tour.config(text=f"Tour {tour_actuel}/{TIME_OUT}")
        
        ruche = ruches[joueur_actuel]
        if phase == "ponte":
            label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - PONTE : Pondre ou passer", font=("Arial", 15, "bold"))
            btn_ouvriere.pack(side=LEFT, padx=5)
            btn_eclaireuse.pack(side=LEFT, padx=5)
            btn_bourdon.pack(side=LEFT, padx=5)
        else:
            btn_ouvriere.pack_forget()
            btn_eclaireuse.pack_forget()
            btn_bourdon.pack_forget()
            
            if phase == "mouvement":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - MOUVEMENT : Cliquez abeille puis case")
            elif phase == "butinage":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - BUTINAGE : Cliquez abeille pour butiner")
            elif phase == "escarmouche":
                label_phase.config(text=f"Joueur {(int(ruche['id'][-1])+1)} - ESCARMOUCHE...")
        
        btn_passer.pack(side=TOP, pady=10)
        label_message.pack(side=RIGHT)
        
        for i in range(len(labels_ruches)):
            label = labels_ruches[i]
            ruche = ruches[i]

            # Compter les abeilles actives et KO
            nb_actives = 0
            nb_ko = 0
            for abeille in ruche["abeilles"]:
                if abeille["etat"] == "OK":
                    nb_actives += 1
                elif abeille["etat"] == "KO":
                    nb_ko += 1

            # Mettre à jour le texte du label
            if i == joueur_actuel:
                label.config(text="Joueur {} (à ton tour)\n\nNectar: {}\nAbeilles actives: {}\nAbeilles KO: {}".format(
                        (int(ruche["id"][-1])+1), ruche["nectar"], nb_actives, nb_ko
                    ),
                    font=("Arial", 12, "bold"), fg='#9E0000')
            else:
                label.config(text="Joueur {}\n\nNectar: {}\nAbeilles actives: {}\nAbeilles KO: {}".format(
                        (int(ruche["id"][-1])+1), ruche["nectar"], nb_actives, nb_ko
                    ),
                    font=("Arial", 11, "bold"), fg='#000000')
    
    def clic_plateau(event):
        nonlocal abeille_cliquee
        
        x = int(event.y / taille_case)
        y = int(event.x / taille_case)
        if x < 0 or x >= NCASES or y < 0 or y >= NCASES:
            return
        
        ruche = ruches[joueur_actuel]
        case = plateau[x][y]
        
        if phase == "mouvement":
            if abeille_cliquee is None:
                for elem in case:
                    if (isinstance(elem, dict) and elem.get("type") == "abeille" and 
                        elem["camp"] == ruche["id"] and elem["etat"] == "OK" and
                        not elem["a_bouge"]): 
                        abeille_cliquee = elem
                        message("Abeille sélectionnée ! Cliquez où aller", "blue")
                        redessiner()
                        return
            else:
                succes, erreur = tenter_deplacement(plateau, abeille_cliquee, (x, y))
                if erreur:
                    message(erreur)
                    return
                
                message("Déplacée !", "green")
                abeille_cliquee = None
                redessiner()
        
        elif phase == "butinage":
            for elem in case:
                if (isinstance(elem, dict) and elem.get("type") == "abeille" and 
                    elem["camp"] == ruche["id"] and elem["etat"] == "OK" and not elem["a_bouge"]):
                    
                    succes, resultat = tenter_butinage(plateau, elem, ruche)
                    if not succes:
                        message(resultat)
                        return
                    
                    message(f"Butiné ! +{resultat}", "green")
                    redessiner()
                    return
    
    # Créer les boutons
    btn_ouvriere = Button(frame_bas, text=" Pondre Ouvrière (5 nectars) ", font=("Arial", 10, "bold"), 
                         bg="#2F1559", fg="white", command=lambda: pondre("ouvriere"))
    btn_eclaireuse = Button(frame_bas, text=" Pondre Éclaireuse (5 nectars) ", font=("Arial", 10, "bold"), 
                           bg="#2F1559", fg="white", command=lambda: pondre("eclaireuse"))
    btn_bourdon = Button(frame_bas, text=" Pondre Bourdon (5 nectars) ", font=("Arial", 10, "bold"), 
                        bg="#2F1559", fg="white", command=lambda: pondre("bourdon"))
    btn_passer = Button(frame_bas, text="   PASSER   ", font=("Arial", 12, "bold"), 
                       bg="#000000", fg="white", command=passer_phase)
    btn_passer.pack(side=TOP, pady=10)
    canvas.bind("<Button-1>", clic_plateau)
    redessiner()
    fenetre.mainloop()


def lancer_partie():
    print("Lancement du jeu...")
    plateau = creer_plateau()
    ruches = creer_ruche(plateau)
    fleurs = creer_fleurs(NFLEURS)
    placer_fleurs(plateau, fleurs)
    
    afficher_plateau_anime(plateau, ruches, 1)


if __name__ == "__main__":
    lancer_partie()
