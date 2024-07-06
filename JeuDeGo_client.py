# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:07:43 2021

@author: alexa
"""

#import des librairies nécessaires
import socket, sys
import tkinter as tk

#déclaration des variables
goban = [[0 for i in range(13)]for i in range(13)]
CASE = 45
L = 13
C = 13
WIDTH = C*CASE
HEIGHT = L*CASE
j_actuel = 1
window = tk.Tk()
canva = tk.Canvas(window, bg="#D17C16", width=CASE*C+40, height=CASE*L+40)
canva.pack(side="bottom")

def apparaitre_goban(goban):
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
    window.mainloop()

def affiche(goban):
    for ligne in goban:
        for case in ligne:
            print("{:>2}".format(case), end="")
        print("")
                
#partie client

HOST = "localhost"
PORT = 15555

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    connexion.connect((HOST,PORT))
except socket.error :
    print("La liaison a échoué")
    sys.exit()
print("La liaison au serveur {}, port : {} est établie".format(HOST,PORT))

msg_serveur = connexion.recv(1024).decode()

while True :
    msg_client = input("Client ---> ")
    #print("Client ---> {}".format(msg_client))
    connexion.send(msg_client.encode())
    msg_serveur = connexion.recv(1024).decode()
    if msg_serveur == "FIN" :
        break
    goban_provisoire = list(msg_serveur)
    goban = []
    for i in range(L):
        ligne = []
        for j in range(C):
            ligne.append(int(goban_provisoire[13*i+j]))
        goban.append(ligne)
    affiche(goban)
            


print("Connexion interrompue ...")
connexion.close()