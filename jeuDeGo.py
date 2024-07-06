# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:56:50 2021

@author: alexa
"""

#import des librairies nécessaires
import tkinter as tk
import copy

#LANCEMENT DE LA PARTIE : ouvre la fenêtre avec laquelle le joueur peut
# intéragir et ainsi jouer
def commencer():
    window.mainloop()

#DECLARATION des varaibles nécessaires à la suite du programme et 
#PREPARATION du goban et de la fenêtre tkinter
goban_j1 = []
goban_j2 = []
CASE = 45 #taille modifiable des cases
L = 13 #nombre de ligne du goban, modifiable
C = 13 #nombre de colonne du goban, modifiable
goban = [[0 for i in range(C)]for i in range(L)]
WIDTH = C*CASE
HEIGHT = L*CASE
j_actuel = 1
window = tk.Tk()
canva = tk.Canvas(window, bg="#D17C16", width=CASE*C+40, height=CASE*L+40)
canva.pack(side="bottom")
coups = [] #liste des coups qui seront joués
passe = False


#JEU PRINCIPAL, PLACEMENT DES PIONS ET CALCUL DU GOBAN
    #réaction à un événement dans la fenêtre tkinter, calcul des coordonnées
def jouer(event):
    global j_actuel
    global label
    global goban
    global passe
    x = event.x
    y = event.y
    for i in range(1, C+1):
        if x > i*CASE-25 and x < (i+1)*CASE-25:
            c = i
    for j in range(1, L+1):
        if y > j*CASE-25 and y < (j+1)*CASE-25 :
            l = j
    if changer_valeur(goban,l,c,j_actuel,"jouer"):
        coups.append((l,c,j_actuel))
        j_actuel = -j_actuel
        if j_actuel == 1:
            texte_joueur = "Tour : joueur 1 (Noir)"
        else:
            texte_joueur = "Tour : joueur 2 (Blanc)"
        label.pack_forget()
        label = tk.Label(window, text=texte_joueur)
        label.pack()
        apparaitre_goban()
        passe = False

    #regarde si le coup est possible, s'il respecte les régles et dans le cas échéant, le joue
def changer_valeur(goban,l,c,j_actuel,origine):
    global label
    jeu = False
    if goban[l-1][c-1]==0:
        goban[l-1][c-1] = j_actuel
        jeu = True
    else :
        return jeu
    if repetition() and origine != "calcul": #vérifie que le goban n'est pas le même
    #qu'à la fin du tour précédent du même joueur, si on n'est pas dans le calcul du goban
        goban[l-1][c-1] = 0
        return False
    capture(l-1,c-1,j_actuel) #test la capture d'une chaîne adverse
    if mort(l-1,c-1): #test la mort immédiate du pion joué, dans le cas échéant, la suite le supprime
        goban[l-1][c-1] = 0
        jeu = False
    return jeu

    #calcul du goban à partir de la liste de coups
def calcul_goban(coups):
    global goban
    goban = [[0 for i in range(C)]for i in range(L)]
    for coup in coups:
        changer_valeur(goban,coup[0], coup[1],coup[2],"calcul")
    return goban

#REGLES DE VERIFICATION ET CAPTURE DES PIONS ADVERSES
    #vérifie la règle de non-répétition du goban
def repetition():
    global goban_j1
    global goban_j2
    if j_actuel == 1:
        if goban_j1 == goban: 
            return True
        else :
            goban_j1 = copy.deepcopy(goban)
            return False
    else:
        if goban_j2 == goban: 
            return True
        else :
            goban_j2 = copy.deepcopy(goban)
            return False

    #vérifie la mort immédiate du pion placé
def mort(l,c):
    global suppression
    g_chaine = [[0 for i in range(C)] for i in range(L)]
    suppression = True
    recherche_chaine(l,c,j_actuel,g_chaine)
    return suppression

    #fonctions de test de capture de chaîne, selon les règles énoncées
        #regarde autour du pion posé s'il y a un pion adverse, appelle la
        #fonction de recherche de chaîne, et la supprime si elle n'a plus de liberté
def capture(i,j,j_actuel):
    global suppression
    if j+1<C:
        g_chaine = [[0 for i in range(C)] for i in range(L)]
        if goban[i][j+1]==-j_actuel:
            suppression = True
            recherche_chaine(i,j+1,-j_actuel,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if i+1<L:
        g_chaine = [[0 for i in range(C)] for i in range(L)]
        if goban[i+1][j]==-j_actuel:
            suppression = True
            recherche_chaine(i+1,j,-j_actuel,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if j-1>-1:
        g_chaine = [[0 for i in range(C)] for i in range(L)]
        if goban[i][j-1]==-j_actuel:
            suppression = True
            recherche_chaine(i,j-1,-j_actuel,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if i-1>-1:
        g_chaine = [[0 for i in range(C)] for i in range(L)]
        if goban[i-1][j]==-j_actuel:
            suppression = True
            recherche_chaine(i-1,j,-j_actuel,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    return goban

        #fonction récursive qui parcoure tous les pions d'une même couleur formant une chaîne
        #et regarde s'il leur reste au moins une liberté
def recherche_chaine(i,j,joueur,g_chaine):
    global suppression
    g_chaine[i][j] = 1
    if j+1<C:
        if goban[i][j+1]==joueur:
            if not g_chaine[i][j+1]==1:
                recherche_chaine(i,j+1,joueur,g_chaine)
        if goban[i][j+1]==0:
            suppression = False
    if i+1<L:
        if goban[i+1][j]==joueur:
            if not g_chaine[i+1][j]==1:
                recherche_chaine(i+1,j,joueur,g_chaine)
        if goban[i+1][j]==0:
            suppression = False
    if j-1>-1:
        if goban[i][j-1]==joueur:
            if not g_chaine[i][j-1]==1:
                recherche_chaine(i,j-1,joueur,g_chaine)
        if goban[i][j-1]==0:
            suppression = False
    if i-1>-1:
        if goban[i-1][j]==joueur:
            if not g_chaine[i-1][j]==1:
                recherche_chaine(i-1,j,joueur,g_chaine)
        if goban[i-1][j]==0:
            suppression = False
            
        #suppression de la chaîne sans liberté donnée par la fonction capture et trouver 
        #par la fonctionde recherche de chaîne
def suppression_chaine(g_chaine):
    for i in range(len(g_chaine)):
        for j in range(len(g_chaine[1])):
            if g_chaine[i][j] == 1:
                goban[i][j]=0

#BOUTONS ET FONCTIONS ASSOCIEES
    #Bouton pour passer son tour, mène à la fin de la partie, si les deux passent
        #change l'interface des boutons pour vérifier si le joueur veut vraiment passer
def PASSER():
    global label
    global bouton_PASSOUI
    global bouton_PASSNON
    label.pack_forget()
    bouton_STOP.pack_forget()
    bouton_PASSER.pack_forget()
    bouton_RETOUR.pack_forget()
    label = tk.Label(window, text="Voulez-vous vraiment passer ?")
    bouton_PASSOUI = tk.Button(window, text = "Oui", command=passer)
    bouton_PASSNON = tk.Button(window, text = "Non", command=annuler_passer) 
    label.pack()
    bouton_PASSOUI.pack()
    bouton_PASSNON.pack()
    
        #signale que le joueur a passé, si et si le joueur précédent vient
        #de passer, compte les points et arrête la partie
def passer():
    global passe
    global j_actuel
    global label
    if passe:
        comptage_points()
        window.destroy()
    else:
        passe = True
        j_actuel = -j_actuel
        if j_actuel == 1:
            texte_joueur = "Tour : joueur 1 (Noir) (Passé)"
        else:
            texte_joueur = "Tour : joueur 2 (Blanc) (Passé)"
        label.pack_forget()
        label = tk.Label(window, text=texte_joueur)
        
        bouton_PASSNON.pack_forget()
        bouton_PASSOUI.pack_forget()
        bouton_STOP.pack()
        bouton_PASSER.pack()
        bouton_RETOUR.pack()
        label.pack()
        apparaitre_goban()

        #remet les boutons de l'interface classique sans avoir passé et laisse 
        #ainsi le joueur jouer normalement
def annuler_passer():
    global label
    global bouton_PASSNON
    global bouton_PASSOUI
    if j_actuel == 1:
        texte_joueur = "Tour : joueur 1 (Noir)"
    else:
        texte_joueur = "Tour : joueur 2 (Blanc)"
    if passe:
        texte_joueur+= " (Passé)"
    label.pack_forget()
    bouton_PASSNON.pack_forget()
    bouton_PASSOUI.pack_forget()
    label = tk.Label(window, text=texte_joueur)
    bouton_STOP.pack()
    bouton_PASSER.pack()
    bouton_RETOUR.pack()
    label.pack()

    #Bouton d'arrêt immédiat de la partie
        #change l'interface des boutons pour vérifier si le joueur veut vraiment arrêter
def STOP():
    global label
    global bouton_OUI
    global bouton_NON
    label.pack_forget()
    bouton_STOP.pack_forget()
    bouton_PASSER.pack_forget()
    bouton_RETOUR.pack_forget()
    label = tk.Label(window, text="Voulez-vous vraiment arrêter la partie ?")
    bouton_OUI = tk.Button(window, text = "Oui", command=fermeture_partie)
    bouton_NON = tk.Button(window, text = "Non", command=annuler_fermeture)
    label.pack()
    bouton_OUI.pack()
    bouton_NON.pack()
    
        #arrêt immédiat de la partie en fermant la fenêtre de jeu
def fermeture_partie():
    window.destroy()
    
        #remet les boutons de l'interface classique sans avoir arrêté et laisse 
        #ainsi le joueur jouer normalement
def annuler_fermeture():
    global label
    global bouton_NON
    global bouton_OUI
    if j_actuel == 1:
        texte_joueur = "Tour : joueur 1 (Noir)"
    else:
        texte_joueur = "Tour : joueur 2 (Blanc)"
    label.pack_forget()
    bouton_NON.pack_forget()
    bouton_OUI.pack_forget()
    label = tk.Label(window, text=texte_joueur)
    bouton_STOP.pack()
    bouton_PASSER.pack()
    bouton_RETOUR.pack()
    label.pack()

    #Bouton de retour d'un cran en arrière 
def RETOUR():
    global coups
    global j_actuel
    global label
    global passe
    if passe:
        passe = False #annule un passage s'il y a eu
    else:
        coups.pop() #supprime le dernier coup joué de la liste des coups
    calcul_goban(coups) #calcul le goban en jouant tous les coups enregistré
    #dans la liste des coups l'un après l'autre
    j_actuel = -j_actuel #retour au joueur précédent
    if j_actuel == 1:
        texte_joueur = "Tour : joueur 1 (Noir)"
    else:
        texte_joueur = "Tour : joueur 2 (Blanc)"
    label.pack_forget()
    label = tk.Label(window, text=texte_joueur)
    label.pack()
    apparaitre_goban()


#COMPTAGE DES POINTS SELON LES REGLES ENONCEES, APPELEES EN FIN DE PARTIE
    #fonction globale qui calcul les points
def comptage_points():
    global goban_territoires
    global dictionnaire_territoire
    territoire = 2
    points_j1 = 0
    points_j2 = 7.5 #komi pour le deuxième joueur
    goban_territoires = copy.deepcopy(goban) #crée une copie du goban qui 
    #servira à déterminer les différents territoires
    dictionnaire_territoire = {} #dictionnaire qui à chaque définie son appartenance
    for l in range(L):
        for c in range(C):
            if goban_territoires[l][c]==0:
                trouver_territoires(l,c,territoire) #recherche le territoire de chaque case
                #si la case est vide et qu'elle n'a pas déjà été attribuée à un territoire
                territoire+=1 #crée une nouvelle valeur qui sera donnée aux éléments d'un nouveau territoire
    for ligne in goban_territoires:
        for case in ligne:
            if case >= 2:
                if dictionnaire_territoire[case] == 1:
                    points_j1+=1
                elif dictionnaire_territoire[case]==-1:
                    points_j2+=1 #+1 point par case qui appartient au territoire d'un joueur
            elif case == 1:
                points_j1 += 1
            elif case == -1:
                points_j2 += 1 # +1 point par case sur laquelle il y a le pion du joueur
    print("Le joueur 1 (Noir) a {} points et le joueur 2 (Blanc) a {} points".format(points_j1,points_j2))
    if points_j1 > points_j2 :
        print("Le joueur 1 (Noir) a gagné ! Bravo")
    else :
        print("Le joueur 2 (Blanc) a gagné ! Bravo")
   
    #fonction récursive qui répand le numéro d'un territoire dans tout le territoire
def trouver_territoires(l,c,territoire):
    global goban_territoires
    global dictionnaire_territoire
    goban_territoires[l][c] = territoire #donne le numéro du territoire associé à
    # la case observée
    if c+1<C: # case de droite
        if goban_territoires[l][c+1] == 0:
            trouver_territoires(l,c+1,territoire) # si la case est vide, recherche
            # sur cette nouvelle case
        elif goban_territoires[l][c+1]==1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = 1 #enregistre le joueur rencontré par le territoire
            elif dictionnaire_territoire[territoire] == -1:
                dictionnaire_territoire[territoire] = 0 # si le territoire touche 
                #deux joueurs, ne donne le territoire à personne
        elif goban_territoires[l][c+1]==-1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = -1
            elif dictionnaire_territoire[territoire] == 1:
                dictionnaire_territoire[territoire] = 0
    if l+1<L: # case du bas
        if goban_territoires[l+1][c] == 0:
            trouver_territoires(l+1,c,territoire)
        elif goban_territoires[l+1][c] == 1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = 1
            elif dictionnaire_territoire[territoire] == -1:
                dictionnaire_territoire[territoire] = 0
        elif goban_territoires[l+1][c]==-1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = -1
            elif dictionnaire_territoire[territoire] == 1:
                dictionnaire_territoire[territoire] = 0
    if c-1>-1: # case de gauche
        if goban_territoires[l][c-1]==0:
            trouver_territoires(l,c-1,territoire)
        elif goban_territoires[l][c-1]==1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = 1
            elif dictionnaire_territoire[territoire] == -1:
                dictionnaire_territoire[territoire] = 0
        elif goban_territoires[l][c-1]==-1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = -1
            elif dictionnaire_territoire[territoire] == 1:
                dictionnaire_territoire[territoire] = 0
    if l-1>-1: # case du haut
        if goban_territoires[l-1][c]==0:
            trouver_territoires(l-1,c,territoire)
        elif goban[l-1][c]==1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = 1
            elif dictionnaire_territoire[territoire] == -1:
                dictionnaire_territoire[territoire] = 0
        elif goban_territoires[l-1][c]==-1:
            if territoire not in dictionnaire_territoire:
                dictionnaire_territoire[territoire] = -1
            elif dictionnaire_territoire[territoire] == 1:
                dictionnaire_territoire[territoire] = 0

#CREATON DE L'INTERFACE GRAPHIQUE
def apparaitre_goban():
    canva.create_rectangle(0,0,700,700,fill="#D17C16",outline="#D17C16") #rectangle de fond
    for i in range(L):
        canva.create_line(CASE, (i+1)*CASE, WIDTH, (i+1)*CASE, width=1, fill="black")
        #lignes horizontales
    for i in range(C):
        canva.create_line((i+1)*CASE, CASE, (i+1)*CASE, HEIGHT, width=1, fill="black")
        #lignes verticales
    for l in range(len(goban)):
        for c in range(len(goban[1])):
            if goban[l][c] == 1:
                x1, y1 = (c+1)*CASE-((CASE-8)//2), (l+1)*CASE-((CASE-8)//2)
                x2, y2 = (c+1)*CASE+((CASE-8)//2), (l+1)*CASE+((CASE-8)//2)
                canva.create_oval(x1, y1, x2, y2, width= 3, fill="black", outline="black")
            elif goban[l][c] == -1:
                x1, y1 = (c+1)*CASE-((CASE-8)//2), (l+1)*CASE-((CASE-8)//2)
                x2, y2 = (c+1)*CASE+((CASE-8)//2), (l+1)*CASE+((CASE-8)//2)
                canva.create_oval(x1, y1, x2, y2, width= 3, fill="white", outline="white")
            #apparition des cercles blancs et noirs pour chaque case sur laquelle on a joué

#CREATION DE TOUS LES AUTRES ELEMENTS DE LA FENÊTRE
apparaitre_goban() #création du canvas
texte_joueur = "Tour : joueur 1 (Noir)"
label = tk.Label(window, text=texte_joueur) #label expliquant le joueur
bouton_STOP = tk.Button(window,text="STOP", command=STOP) # voir ligne 253
bouton_STOP.pack()
bouton_PASSER = tk.Button(window,text="PASSER", command=PASSER) # voir ligne 188
bouton_PASSER.pack()
bouton_RETOUR = tk.Button(window,text="RETOUR", command=RETOUR) # voir ligne 292
bouton_RETOUR.pack()
label.pack()
canva.bind("<Button-1>", jouer) # liaison d'un évènement sur la fenêtre à la fonction jouer