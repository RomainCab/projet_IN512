########################################################################################################################

#                                       Visualisation de la grille

########################################################################################################################
import numpy as np
from tkinter import *
import tkinter
import time

print(tkinter.TkVersion)

L = 20
H = 20
rows, cols = 20, 20
cases = []
Lcan = cols*L
Hcan = rows*H
Pcan = 3
"""GridProba, GridBelieves: 3-D matrix containing :
    1- first dimension = information about obstacles
    2- second dimension = information about human presence
    3- Third dimension = indicates if the robot already explored the cell or not"""
GridProba = np.zeros((3, rows, cols))
GridBelieves = np.zeros((3, rows, cols))

class Robot:
    def __init__(self, pos_x, pos_y):
        self.pos_x_robot, self.pos_y_robot = pos_x, pos_y #Position par défaut du robot : (2,2)
        self.itemRobot = dessin.itemconfigure(cases[20-self.pos_y_robot][self.pos_x_robot], outline='black', fill='green')

    def moveRobot(self, n_iter):

        #--- move forward ---#
        for i in range(n_iter):
            if GridProba[0, self.pos_x_robot, (20-self.pos_y_robot)+1]==0:
                #Check if there is an obstacle in front
                self.pos_y_robot+=1
                dessin.itemconfigure(cases[20-self.pos_y_robot][self.pos_x_robot], outline='black', fill='green')
                dessin.itemconfigure(cases[(20 - self.pos_y_robot)+1][self.pos_x_robot], outline='black', fill='grey')


            elif GridProba[0, self.pos_x_robot+1, (20-self.pos_y_robot)+1]==0:
                #Check if there is an obstacle to the right
                self.pos_x_robot += 1
                dessin.itemconfigure(cases[20 - self.pos_y_robot][self.pos_x_robot], outline='black', fill='green')
                dessin.itemconfigure(cases[20 - self.pos_y_robot][self.pos_x_robot-1], outline='black', fill='grey')


            elif GridProba[0, self.pos_x_robot-1, (20-self.pos_y_robot)+1]==0:
                #Check if there is an obstacle to the left
                self.pos_x_robot -= 1
                dessin.itemconfigure(cases[20 - self.pos_y_robot][self.pos_x_robot], outline='black', fill='green')
                dessin.itemconfigure(cases[20 - self.pos_y_robot][self.pos_x_robot + 1], outline='black', fill='grey')

def afficher_position(event):
    #clic=event.x, event.y
    pos_x, pos_y = dessin.canvasx(event.x), dessin.canvasy(event.y)
    strvar_position.set(f"Position du clic : abscisse = {pos_x} ; ordonnées = {pos_y}")

    colonne, ligne = pos_x // L, pos_y // H  # ligne 'magique'
    strvar_case.set(f"Case désignée : colonne = {colonne} ; ligne = {ligne}")

def draw_obstacle_by_click(event):
    pos_x, pos_y = dessin.canvasx(event.x), dessin.canvasy(event.y)
    colonne, ligne = int(pos_x // L), int(pos_y // H)  # ligne 'magique'

    if dessin.itemconfigure(cases[ligne][colonne])['fill'] !='black':
        GridProba[0, ligne-1:ligne+2, colonne-1:colonne+2] = 0.5
        GridProba[0, ligne, colonne] = 1
        dessin.itemconfigure(cases[ligne][colonne], outline='black', fill='black')
        #dessin.itemconfigure(cases[ligne][colonne-1], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne][colonne+1], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne-1][colonne], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne-1][colonne-1], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne-1][colonne+1], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne+1][colonne], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne+1][colonne - 1], outline='black', fill='grey')
        #dessin.itemconfigure(cases[ligne+1][colonne + 1], outline='black', fill='grey')
        #print(GridProba[ligne-1:ligne+2, colonne-1:colonne+2])


def delete_obstacle(event):
    pos_x, pos_y = dessin.canvasx(event.x), dessin.canvasy(event.y)
    colonne, ligne = int(pos_x // L), int(pos_y // H)  # ligne 'magique'
    GridProba[0, ligne - 1:ligne + 2, colonne - 1:colonne + 2] = 0
    dessin.itemconfigure(cases[ligne][colonne], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne-1][colonne-1], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne - 1][colonne], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne - 1][colonne + 1], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne][colonne - 1], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne][colonne + 1], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne + 1][colonne - 1], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne + 1][colonne], outline='black', fill='Ivory')
    #dessin.itemconfigure(cases[ligne + 1][colonne + 1], outline='black', fill='Ivory')

def draw_human(event):
    pos_x, pos_y = dessin.canvasx(event.x), dessin.canvasy(event.y)
    colonne, ligne = int(pos_x // L), int(pos_y // H)  #ligne 'magique'
    dessin.itemconfigure(cases[ligne][colonne], outline='black', fill='red')
    GridProba[0,ligne-3: ligne+4, colonne-3:colonne+4]=0.1
    GridProba[0,ligne - 2: ligne + 3, colonne - 2:colonne + 3] = 0.3
    GridProba[0,ligne - 1: ligne + 2, colonne - 1:colonne + 2] = 0.6
    GridProba[0,ligne, colonne] = 1

def reset_grid():
    for ligne in range(rows):  # Les cases de chaque ligne seront stockées dans "transit"
        for colonne in range(cols):
            dessin.itemconfigure(cases[ligne][colonne], outline='black', fill='Ivory')
            #dessin.itemconfigure(cases[20 - 2][1], outline='black', fill='green')
    GridProba = np.zeros(rows, cols)


##----- Création de la fenêtre -----##
fen = Tk()
fen.title('2D GridProba')
fen.geometry("600x500")

##----- Création des boutons -----##
#bouton_quitter = Button(fen, text='Quitter', command=fen.destroy)
#bouton_quitter.grid(row = 1, column = 1, sticky=W+E, padx=3, pady=3)

##----- Création des canevas -----##
dessin = Canvas(fen, width = rows*cols+2, height = rows*cols+2, bg = 'ivory', scrollregion=(0, 0, Lcan, Hcan))
dessin.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

##----- Création des figures -----##
for ligne in range(rows):          # Les cases de chaque ligne seront stockées dans "transit"
    transit=[]
    for colonne in range(rows):    # Conception des cases d'une ligne
        transit.append(dessin.create_rectangle(colonne*cols+2, ligne*cols+2, (colonne+1)*cols+2, (ligne+1)*cols+2))
    cases.append(transit)       # Ajout de la ligne à la liste principale

##----- placement du robot -----##
robot = Robot(2, 2)
itemRobot = dessin.itemconfigure(cases[20 - robot.pos_y_robot][robot.pos_x_robot], outline='black', fill='green')
robot.moveRobot(5)

strvar_position = StringVar()
strvar_position.set('Position de la souris dans la scrollregion: ')
Label(fen, textvariable=strvar_position).grid(row=0, column = 0)

strvar_case = StringVar()
strvar_case.set('Case désignée')
Label(fen, textvariable=strvar_case).grid(row=0, column=1)

##----- Affichage de la position de la souris -----##
dessin.bind("<Motion>", afficher_position)

##----- Ajout d'obstacle avec un clic droit -----##
fen.bind("<Button-1>", draw_obstacle_by_click)

##----- Suppression d'obstacle avec un clic gauche -----##
fen.bind("<Button-3>", delete_obstacle)

##----- Ajout d'humain avec un clic sur la molette de la souris -----##
fen.bind("<Button-2>", draw_human)

##----- Bouton reset -----##
resetButton = Button(fen, text='Reset grid', command=reset_grid).grid(row=2, column=0)

##----- Bouton quitter ----- ##
quitButton = Button(fen, text='Quit', command=quit).grid(row=2, column=1)

##----- Champ d'entrée des coordonnées du robot -----##
#selectCoordRobot_x = Entry(fen, text='X_robot : ', width = 5).place(x)
#selectCoordRobot_y = Entry(fen, text='Y_robot : ', width = 5).grid(row=1, column=2)

##----- Draw obstacles (static representation)
GridProba[0, 3, 2:-2] = 1
GridProba[0, 2, 1:-1] = 0.5
GridProba[0, 4, 1:-1] = 0.5
GridProba[0, 3, -2] = 0.5
GridProba[0, 3, 1] = 0.5

GridProba[0, 4:9, 5:8] = 0.5
GridProba[0, 5:8, 6] = 1

GridProba[0, 4:9, 8:11] = 0.5
GridProba[0, 5:8, 9] = 1

GridProba[0, 4:9, 11:14] = 0.5
GridProba[0, 5:8, 12] = 1

GridProba[0, 6:9, 0:5]=0.5
GridProba[0, 7, 0:4]=1

GridProba[0, 8:15, 14:17]=0.5
GridProba[0, 9:14, -5]=1

GridProba[0, 8:15, 9:12]=0.5
GridProba[0, 9:14, 10]=1

GridProba[0, 9:15, 6:9]=0.5
GridProba[0, 10:14, 7]=1

GridProba[0, 11:14, 0:7]=0.5
GridProba[0, 12, 1:6]=1

GridProba[0, 15:18, 0:6]=0.5
GridProba[0, 16, 0:5]=1

GridProba[0, 14:17, 12:20]=0.5
GridProba[0, 15, 14:19]=1

GridProba[0, 18:20, 12:19]=0.5
GridProba[0, -1, 13:18]=1

GridProba[0, 17:20, 3:10]=0.5
GridProba[0, -2, 4:9]=1

#--- Draw humans
GridProba[1, -1, -1] = 1

GridProba[1, -1, 0] = 1

GridProba[1, -3, 11] = 1

GridProba[1, 14, 0] = 1

GridProba[1, 14, 0] = 1

GridProba[1, 8, 0] = 1

GridProba[1, 9, 7] = 1

GridProba[1, 11, 11] = 1

GridProba[1, 8, -1] = 1

GridProba[1, 4, -3] = 1

for x in range(GridProba.shape[1]):
    for y in range(GridProba.shape[2]):
        if GridProba[1, x, y] == 1:
            #GridProba[1, x - 3:x + 4, y - 3:y + 4] = np.where(GridProba[0, x - 3:x + 4, y - 3:y + 4] < 0.1, 0.1, 0)
            GridProba[1, x - 2:x + 3, y - 2:y + 3] = np.where(GridProba[0, x - 2:x + 3, y - 2:y + 3] < 0.3, 0.3, 0)
            GridProba[1, x-1:x+2, y-1:y+2]=np.where(GridProba[0, x-1:x+2, y-1:y+2]<1, 0.6, 0)
            GridProba[1, x, y] = 1

for x in range(GridProba.shape[1]):
    for y in range(GridProba.shape[2]):
        if GridProba[0, x, y] == 1:
            dessin.itemconfigure(cases[-y-1][x], outline='black', fill='black')
        elif GridProba[0, x, y] == 0.5:
            dessin.itemconfigure(cases[-y-1][x], outline='black', fill='grey')
        if GridProba[1, x, y] == 1:
            dessin.itemconfigure(cases[-y-1][x], outline='brown', fill='brown')
        elif GridProba[1, x, y] == 0.6:
            dessin.itemconfigure(cases[-y-1][x], outline='red', fill='red')
        elif GridProba[1, x, y] == 0.3:
            dessin.itemconfigure(cases[-y-1][x], outline='salmon', fill='salmon')
        elif GridProba[1, x, y] == 0.1:
            dessin.itemconfigure(cases[-y-1][x], outline='pink', fill='pink')

#--- Place robot
dessin.itemconfigure(cases[14][1], outline='green', fill='green')

#--- Exploration strategy







##----- Programme principal -----##
fen.mainloop()                  # Boucle d'attente des événements

print(cases)



