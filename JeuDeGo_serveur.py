# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:01:34 2021

@author: alexa
"""

import socket, sys
import tkinter as tk
import copy

#partie programme 

goban = [[0 for i in range(13)]for i in range(13)]
CASE = 45
L = 13
C = 13
WIDTH = C*CASE
HEIGHT = L*CASE
j_actuel = 1
autre_j = 2
window = tk.Tk()
canva = tk.Canvas(window, bg="#D17C16", width=CASE*C+40, height=CASE*L+40)
canva.pack(side="bottom")
passe = False

def apparaitre_goban():
    canva.create_rectangle(0,0,700,700,fill="#D17C16",outline="#D17C16")
    for i in range(L):
        canva.create_line(CASE, (i+1)*CASE, WIDTH, (i+1)*CASE, width=1, fill="black")
    for i in range(C):
        canva.create_line((i+1)*CASE, CASE, (i+1)*CASE, HEIGHT, width=1, fill="black")
    for l in range(len(goban)):
        for c in range(len(goban[1])):
            if goban[l][c] == 1:
                x1, y1 = (c+1)*CASE-((CASE-8)//2), (l+1)*CASE-((CASE-8)//2)
                x2, y2 = (c+1)*CASE+((CASE-8)//2), (l+1)*CASE+((CASE-8)//2)
                canva.create_oval(x1, y1, x2, y2, width= 3, fill="black", outline="black")
            elif goban[l][c] == 2:
                x1, y1 = (c+1)*CASE-((CASE-8)//2), (l+1)*CASE-((CASE-8)//2)
                x2, y2 = (c+1)*CASE+((CASE-8)//2), (l+1)*CASE+((CASE-8)//2)
                canva.create_oval(x1, y1, x2, y2, width= 3, fill="white", outline="white")

def repetition():
    return True

def capture(i,j,j_actuel):
    global suppression
    if j+1<13:
        g_chaine = [[0 for i in range(13)] for i in range(13)]
        if goban[i][j+1]==autre_j:
            suppression = True
            recherche_chaine(i,j+1,autre_j,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if i+1<13:
        g_chaine = [[0 for i in range(13)] for i in range(13)]
        if goban[i+1][j]==autre_j:
            suppression = True
            recherche_chaine(i+1,j,autre_j,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if j-1>-1:
        g_chaine = [[0 for i in range(13)] for i in range(13)]
        if goban[i][j-1]==autre_j:
            suppression = True
            recherche_chaine(i,j-1,autre_j,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    if i-1>-1:
        g_chaine = [[0 for i in range(13)] for i in range(13)]
        if goban[i-1][j]==autre_j:
            suppression = True
            recherche_chaine(i-1,j,autre_j,g_chaine)
            if suppression:
                suppression_chaine(g_chaine)
    return goban

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

def recherche_chaine(i,j,joueur,g_chaine):
    global suppression
    g_chaine[i][j] = 1
    if j+1<13:
        if goban[i][j+1]==joueur:
            if not g_chaine[i][j+1]==1:
                recherche_chaine(i,j+1,joueur,g_chaine)
        if goban[i][j+1]==0:
            suppression = False
    if i+1<13:
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
            
def suppression_chaine(g_chaine):
    for i in range(len(g_chaine)):
        for j in range(len(g_chaine[1])):
            if g_chaine[i][j] == 1:
                goban[i][j]=0
                
def mort(l,c):
    global suppression
    g_chaine = [[0 for i in range(13)] for i in range(13)]
    suppression = True
    recherche_chaine(l,c,j_actuel,g_chaine)
    return suppression

def changer_valeur(goban,l,c,j_actuel):
    global label
    jeu = False
    assert repetition()
    if goban[l-1][c-1]==0:
        goban[l-1][c-1] = j_actuel
        jeu = True
    else :
        return jeu
    capture(l-1,c-1,j_actuel)
    if mort(l-1,c-1):
        goban[l-1][c-1] = 0
        jeu = False
    return jeu

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

def affiche(goban):
    for ligne in goban:
        for case in ligne:
            print("{:>2}".format(case), end="")
        print("")

#partie serveur 

HOST = ""
PORT = 15555

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    connexion.bind((HOST,PORT))
except socket.error :
    print("La liaison a échoué")
    sys.exit()
print("La liaison au serveur {}, port : {} est établie".format(HOST,PORT))

while True :
    print("Serveur lancé ... en attente de requêtes d'un client")
    connexion.listen(1)
    connexion_client, adresse = connexion.accept()
    print("Client connecté, adresse IP : {}, port : {}".format(adresse[0], adresse[1]))
    msg_serveur = "Vous êtes connecté au serveur {}. Envoyez vos messages.".format(HOST)
    connexion_client.send(msg_serveur.encode())
    msg_client = connexion_client.recv(1024).decode()
    
    while True :
        if msg_client == "FIN" :
            msg_serveur = "FIN"
            connexion_client.send(msg_serveur.encode())
            break
        elif msg_client == "PASSE" and not passe:
            print("Passe")
            passe = True
        elif msg_client == "PASSE" :
            comptage_points()
            break
        else :
            passe = False
            msg_client = msg_client.split(",")
            for i in range(len(msg_client)):
                msg_client[i] = int(msg_client[i])
            changer_valeur(goban,msg_client[0],msg_client[1], j_actuel)
            affiche(goban)
        if j_actuel == 1:
            j_actuel = 2
            autre_j = 1
        else:
            j_actuel = 1
            autre_j = 2
        jeu_serveur = input("Serveur ---> ")
        if jeu_serveur == "FIN" :
            msg_serveur = "FIN"
            connexion_client.send(msg_serveur.encode())
            break
        elif jeu_serveur == "PASSE" and not passe:
            print("Passe")
            passe = True
        elif jeu_serveur == "PASSE" :
            comptage_points()
            break
        else :
            passe = False
            jeu_serveur = jeu_serveur.split(",")
            for i in range(len(jeu_serveur)):
                jeu_serveur[i] = int(jeu_serveur[i])
            changer_valeur(goban,jeu_serveur[0],jeu_serveur[1], j_actuel)
        if j_actuel == 1:
            j_actuel = 2
            autre_j = 1
        else:
            j_actuel = 1
            autre_j = 2
        msg_serveur = ""
        for i in range(len(goban)):
            for j in range(len(goban[1])):
                msg_serveur += str(goban[i][j])
        connexion_client.send(msg_serveur.encode())
        msg_client = connexion_client.recv(1024).decode()
                
    
    connexion_client.send("FIN".encode())
    print("Connexion interrompue ...")
    ch = input("<R>ecommencer ou <T>erminer ? ")
    if ch == "T" :
        print("Serveur déconnecté ... ")
        break
    if ch == "R" :
        goban = [[0 for i in range(13)]for i in range(13)]
connexion.close()
