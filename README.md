# jeu_de_go
Implémentation d'un jeu de go sur un ordinateur ou en réseau avec un serveur et un client

Fonctionnalités :
 1) Jeu de go  sur un seul ordinateur : JeuDeGo.py
	- création d'un goban interactif de nombre de case et de taille de case réglable facilement, s'ouvrant dans une nouvelle fenêtre
	- jeu classique à deux personnes sur un même appareil vérifiant la non répétition d'un coup, capturant les chaînes adverses sans 
	  liberté, avec vérification de non mort immédiate
	- affichage du joueur dont c'est le tour
	- trois boutons : Stop qui après confirmation arrête la partie en fermant la fenêtre (pour relancer la partie, il faudra à nouveau
	  lancer le programme), Passer qui permet de passer son tour après confirmation, retour qui permet de revenir en arrière
	- calcul des points et affichage du vainqueur dans la console d'exécution
 
2) Jeu de go en réseau : JeuDeGoClient.py et JeuDeGoServeur.py
	- (ces programmes sont les débuts de la réflexion à propos de la réalisation d'un projet de jeu de go en réseau)
	- si les deux sont lancés dans deux consoles d'exécution différentes, on peut placer des pions dans un tableau selon les mêmes règles qu'au jeu de go
	- pas d'interface graphique, donner les coordonnées sur le goban séparées par ","
	- Pour finir la partie, un des joueurs écrit "FIN", pour passer "PASSE" et fin du jeu quand les deux joueurs passent à la suite
	- à la fin, proposition de recommencer (potentiellement avec un autre client qui se reconnecte) ou de terminer
