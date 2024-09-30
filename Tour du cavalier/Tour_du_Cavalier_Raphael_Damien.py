#------------------------------------------------------Importations-------------------------------------------------------
import random
import time
from tkinter import * 
from collections import deque 

#-----------------------------------------------------Fonctions-----------------------------------------------------------

def creer_graphe(n):
    """
    Crée et retourne un graphe représentant les déplacements possibles d'un cavalier
    sur un plateau d'échecs de taille x taille.
    """
    #numlig * dimension + numcol
    g = dict() #creation du dictionnaire

    for i in range(n*n): #pour chaque case
        g[i] = []        #on initialise avec une liste vide les cases sur lesquelles le cavalier peut aller
        x = i//n         #x est l'abscisse
        y = i%n          #y est l'ordonnée
        
        #pour chaque case étant accessible en faisant un L, on regarde si le cavalier peut se deplacer
        #sur cette case(si la case existe), on ajoute cette case comme valeur de la case
        if  (0 <= x-2 and  0 <= y-1):      #Par rapport à la case actuelle, si la case avec -2 en abscisse et -1 en ordonné à une ordonnée inférieur ou égale à 0 et que son abscisse est <= à 0 alors
            g[i].append((x-2) * (n) + (y-1)) #On ajoute cette case aux valeurs de la case actuelle
        if  (0 <= x-2 and  (n) > y+1): 
            g[i].append((x-2) * (n) + (y+1))
        if  (0 <= x-1 and  0 <= y-2): 
            g[i].append((x-1) * (n) + (y-2))
        if  ((n) > x+1 and  0 <= y-2): 
            g[i].append((x+1) * (n) + (y-2))
        
        if  ((n) > x+2 and  0 <= y-1): 
            g[i].append((x+2) * (n) + (y-1))
        if  ((n) > x+2 and  (n) > y+1): 
            g[i].append((x+2) * (n) + (y+1))
        if  ((n) > x+1 and  (n) > y+2): 
            g[i].append((x+1) * (n) + (y+2))
        if  (0 <= x-1 and  (n) > y+2): 
            g[i].append((x-1) * (n) + (y+2))

    return g

def choisir_case_aleatoire(taille):
    """
    Choisit aléatoirement la case de départ pour le cavalier.
    """
    return random.randint(0, taille * taille - 1) #retourne une case aléatoire avec la bibliothèque random (entre 0 et taille*taille-1)



def trouver_chemin(taille, graphe, case_actuelle, plateau):
    """
    Fonction récursive qui trouve un chemin pour un cavalier d'échecs qui passe par toutes les cases
    d'un plateau d'échecs de taille x taille sans jamais passer deux fois sur la même case.
    """
    # Marquer la case actuelle comme visitée sur le plateau
    plateau[case_actuelle] = True
    if all(plateau):
        # Si toutes les cases ont été visitées, on a trouvé une solution, on renvoie la case actuelle
        return [case_actuelle]
    # Récupérer les voisins de la case actuelle dans le graphe
    voisins = graphe[case_actuelle]
    # Trier les voisins par ordre croissant du nombre de voisins qu'ils ont
    voisins = sorted(voisins, key=lambda v: len(graphe[v]))
    # Explorer chaque voisin non visité récursivement pour trouver un chemin
    for voisin in voisins:
        #Si le voisin n'est pas visité
        if not plateau[voisin]: 
            chemin = trouver_chemin(taille, graphe, voisin, plateau.copy())
            # Si un chemin a été trouvé, on le retourne en ajoutant la case actuelle
            if chemin is not None:
                return [case_actuelle] + chemin
    # Si aucun chemin n'a été trouvé, on retourne None
    return None

def trouver_chemin_boucle(taille, graphe, case_actuelle, depart, plateau):
    """
    Fonction récursive qui trouve un chemin pour un cavalier d'échecs qui passe par toutes les cases
    d'un plateau d'échecs de taille x taille sans jamais passer deux fois sur la même case, en bouclant sur la dernière case.
    """
    # Marquer la case actuelle comme visitée sur le plateau
    plateau[case_actuelle] = True

    if all(plateau):
        # Si toutes les cases ont été visitées, on a trouvé une solution
        if depart in graphe[case_actuelle]:
            # Si la case de départ est un voisin de la case actuelle, on a trouvé un chemin en boucle, on renvoie la case actuelle et la case de départ
            return [case_actuelle, depart]

    # Récupérer les voisins de la case actuelle dans le graphe
    voisins = graphe[case_actuelle]
    # Trier les voisins par ordre croissant du nombre de voisins qu'ils ont
    voisins = sorted(voisins, key=lambda v: len(graphe[v]))
    # Explorer chaque voisin non visité récursivement pour trouver un chemin
    for voisin in voisins:
        if not plateau[voisin]:
            chemin = trouver_chemin_boucle(taille, graphe, voisin, depart, plateau.copy())
            # Si un chemin a été trouvé, on le retourne en ajoutant la case actuelle
            if chemin is not None:
                return [case_actuelle] + chemin
    # Si aucun chemin n'a été trouvé, on retourne None
    return None

def parcours_cavalier(taille):
    """
    Trouve un chemin pour un cavalier d'échecs qui passe par toutes les cases
    d'un plateau d'échecs de taille x taille sans jamais passer deux fois sur la même case.
    """
    #on crée le graphe
    graphe = creer_graphe(taille)
    choix1 = 0
    # Boucle pour demander à l'utilisateur de choisir la position de départ ou de la générer aléatoirement
    while(choix1 != 1 and choix1 != 2):
        choix1 = int(input("1 - choisir vous même la position de départ \n2 - Position de départ aléatoire \nVotre Choix : "))
        if (choix1 == 1):
            depart = int(input("Entrez le numéro de la case de départ : "))
        elif(choix1 == 2):
            depart = choisir_case_aleatoire(taille)
            print(depart)
        else:
            print("Erreur")
        
    # Initialisation du plateau à False pour chaque case
    plateau = [False] * taille * taille
    
    choix = 0
    
    # Initialisation du choix de l'utilisateur pour le type de chemin à trouver
    while(choix != 1 and choix != 2):
        choix = int(input("1 - chemin Hamiltonien \n2 - cycle Hamiltonien \nVotre choix : "))
        if (choix == 1):
            tps1 = time.time()
            chemin = trouver_chemin(taille, graphe, depart, plateau)
            tps2 = time.time()
            print("temps d'exécution : ", tps2 - tps1)
        elif(choix == 2):
            tps1 = time.time()
            chemin = trouver_chemin_boucle(taille, graphe, depart, depart, plateau)
            tps2 = time.time()
            print("temps d'exécution : ", tps2 - tps1)
        else:
            print("Erreur")
    # Retourne le chemin trouvé
    return chemin



def créerInterface(taille, chemin):
    # Création de la fenêtre principale
    fenetre = Tk()
    fenetre['bg']='white'
    # Création du canvas pour afficher les cases et les pions
    canvas = Canvas(fenetre, width=taille*75, height=taille*75, background='white')
    # Parcours de toutes les cases du plateau
    for j in range(taille):
        for i in range(taille):
            # Si la case doit être noire, on la colorie en noir
            if (i%2 != 0 and j%2 ==0) or (i%2 == 0 and j%2 !=0):
                rect = canvas.create_rectangle(i*75, j*75, i*75+75, j*75+75, fill='black')
            # Sinon, on la colorie en blanc
            else:
                rect = canvas.create_rectangle(i*75, j*75, i*75+75, j*75+75, fill='white')
    
    # Initialisation du premier pion
    i=0
    pion = chemin[i]
    x1 = pion%taille*75
    y1 = (taille-1)*75 - pion//taille*75
    # Affichage du premier pion sous forme de cercle rouge
    cercle = canvas.create_oval(x1+12,y1+12,x1+63,y1+63, fill='red')

    # Placement du cercle rouge au centre de la case correspondante
    x1+=37.5
    y1+=37.5

    # Parcours de toutes les cases du chemin
    while (i < len(chemin)-1):
        i+=1
        # Récupération de la case suivante
        pion2 = chemin[i]
        x2 = pion2%taille*75 +37.5
        y2 = (taille-1)*75 - pion2//taille*75 +37.5
        # Affichage d'une ligne rouge entre les deux cases
        line = canvas.create_line(x1,y1,x2,y2, fill='red')
        
        # Mise à jour des coordonnées du cercle rouge
        x1 = x2
        y1 = y2

    # Affichage final du canevas
    canvas.pack()
    # Boucle principale de la fenêtre
    fenetre.mainloop()

def main():
    # taille du plateau demandée à l'utilisateur
    taille = int(input("Saisir la taille du plateau : "))
    #on crée une variable chemin qui stockera ou non le chemin si il est trouvé
    chemin = parcours_cavalier(taille)
    #si un chemin a été trouvé
    if chemin is not None:
        #on affiche ce chemin
        print(chemin)
        #on lance la fonction suivante qui modélise le chemin trouvé
        créerInterface(taille, chemin)
    else:
        #sinon on dit qu'il n'y a pas de solution
        print("Pas de solution trouvée")


#------------------------------------------------------Executions---------------------------------------------------------

main() #on lance la fonction principale