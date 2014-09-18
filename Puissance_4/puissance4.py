#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import random
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageColor

EMPTY = "0"
J1 = "1"
J2 = "2"

JETON_SIZE = 20
JETON_OFFSET = 2

JAUNE = ImageColor.getrgb("#ffff00")
ROUGE = ImageColor.getrgb("#ff0000")
BLEU = ImageColor.getrgb("#0000ff")
NOIR = ImageColor.getrgb("#000000")

LARGEUR = 7
HAUTEUR = 6
FILENAME = "grille.txt"


class Grille:

    def __init__(self, hauteur, largeur, fichier=None):
        self.hauteur = hauteur
        self.largeur = largeur
        self.fichier = fichier
        self.etape = 1
        self.grille = [[EMPTY for x in xrange(largeur)] for y in xrange(hauteur)]
        self.taille = largeur*hauteur

    def test_victoire(self):
        """
        retourne 0 si égalité
        1 si J1 gagne
        2 si J2 gagne
        42 si égalité parfaite (toute case prise sans possibilité de jouer)
        """
        # re.search(r'1{4}', chaine)
        # re.search(r'2{4}', chaine)

        # test si egalite parfaite
        if self.etape == self.taille:
            return 42

        # cherche horizontalement
        for y in range(0, self.hauteur):
            chaine = ""
            for x in range(0, self.largeur):
                chaine += self.grille[y][x]
            res = re.search(r'1{4}', chaine)
            if res is not None:
                return 1
            res = re.search(r'2{4}', chaine)
            if res is not None:
                return 2

        # cherche verticalement
        for x in range(0, self.largeur):
            chaine = ""
            for y in range(0, self.hauteur):
                chaine += self.grille[y][x]
            res = re.search(r'1{4}', chaine)
            if res is not None:
                return 1
            res = re.search(r'2{4}', chaine)
            if res is not None:
                return 2

        # cherche en diagonal
        if self.largeur > self.hauteur:
            grandcote = self.largeur
        else:
            grandcote = self.hauteur
        # diagonal /
        for i in range(0, grandcote*2-1):
            top = i
            chaine = ""
            for x in range(0, i+1):
                try:
                    chaine += self.grille[top-x][x]
                except:
                    continue
            res = re.search(r'1{4}', chaine)
            if res is not None:
                return 1
            res = re.search(r'2{4}', chaine)
            if res is not None:
                return 2

        # diagonal \
        for i in range(0, grandcote):
            top = i
            chaine = ""
            for x in range(0, grandcote):
                try:
                    chaine += self.grille[x+top][x]
                except:
                    continue
            res = re.search(r'1{4}', chaine)
            if res is not None:
                return 1
            res = re.search(r'2{4}', chaine)
            if res is not None:
                return 2
            chaine = ""
            for x in range(0, grandcote):
                try:
                    chaine += self.grille[x][x+top]
                except:
                    continue
            res = re.search(r'1{4}', chaine)
            if res is not None:
                return 1
            res = re.search(r'2{4}', chaine)
            if res is not None:
                return 2

        return 0 # Personne ne gagne pour le moment

    def hash(self):
        """ Retourne le hash du contenu en parametre """
        hacheur = hashlib.md5()
        hacheur.update(self.grille)
        return hacheur.digest()

    def exporter(self, fichier=None):
        """ Exporte la grille dans un fichier """
        if fichier is not None:
            f = fichier
        elif self.fichier is not None:
            f = self.fichier
        else:
            return 1

        try:
            contenu = ""
            for y in range(self.hauteur-1, -1, -1):
                for x in range(0, self.largeur):
                    contenu += self.grille[y][x]
                contenu += "\n"
            with open(f, "w") as fichier:
                fichier.write(contenu)
            return 0
        except:
            print "Problème d'ouverture du fichier"
            return 1

    def exportPNG(self, fichier):
        """ Exporte la grille dans un png """
        if fichier is None:
            return 1
        taille = JETON_SIZE+JETON_OFFSET*2
        rayon = JETON_SIZE/2
        largeur = taille*self.largeur + taille/2
        hauteur = taille*self.hauteur + taille/2
        image = Image.new("RGB", (largeur, hauteur), BLEU)
        dessinateur = ImageDraw.Draw(image)

        for y in range(0, self.hauteur):
            for x in range(0, self.largeur):
                if self.grille[y][x] == J1:
                    couleur = JAUNE
                elif self.grille[y][x] == J2:
                    couleur = ROUGE
                else:
                    couleur = None

                if couleur is not None:
                    centre_x = JETON_OFFSET+taille/2+taille*x
                    centre_y = hauteur-taille/2-JETON_OFFSET-taille*y
                    dessinateur.ellipse(
                            [(centre_x-rayon, centre_y-rayon),
                             (centre_x+rayon, centre_y+rayon)],
                            couleur, NOIR
                    )
        image.save(fichier)

    def importer(self, fichier=None):
        """ Importe la grille depuis un fichier """
        if fichier is not None:
            f = fichier
        elif self.fichier is not None:
            f = self.fichier
        else:
            return 0

        try:
            with open(f, "r") as fichier:
                contenu = fichier.read()

            y = 0; # self.hauteur
            x = 0; # largeur
            for car in contenu:
                try:
                    if(car == '\n'):
                        y += 1
                        x = 0
                    else:
                        self.grille[self.hauteur-y-1][x] = car
                        x += 1
                except:
                    print "Souci dans la recuperation"
                    return 0
            return 1
        except:
            print "Problème d'ouverture du fichier"
            return 0

    def afficher(self, filename=None):
        """ Affiche la grille dans la console """
        contenu = ""
        for y in range(self.hauteur-1, -1, -1):
            for x in range(0, self.largeur):
                contenu += self.grille[y][x]
            contenu += "\n"
        print contenu

    def jouer(self, joueur, colonne):
        """ Joue un pion dans une colonne """
        colonne -= 1 # offset
        if colonne > self.largeur-1:
            colonne = self.largeur-1
        elif colonne < 0:
            colonne = 0

        for y in range(0, self.hauteur):
            if self.grille[y][colonne] == EMPTY:
                self.grille[y][colonne] = joueur
                return 0 # on a reussi a jouer dans la colonne

        return 1 # on a pas pu jouer dans cette colonne (pleine)

    def debug_set(self, x, y, value):
        self.grille[x][y] = value



# initialise l'ensemble
shutil.rmtree("./histo/")
os.mkdir("./histo/")

# verifie que l'on a bien deux joueurs
if len(sys.argv) != 3:
    print "Le programme n'a pas ete lance correctement"
    print "exemple : ./puissance_4.py joueur1.py joueur2.py"
else:
    print "Pret pour la bataille !"
    print "Tirage au sort du premier joueur..."
    random.seed()
    choix = random.randint(0, 1)
    if choix:
        joueur1 = sys.argv[1]
        joueur2 = sys.argv[2]
    else:
        joueur1 = sys.argv[2]
        joueur2 = sys.argv[1]
    print "le joueur 1 sera : {}".format(joueur1)
    print "le joueur 2 sera : {}".format(joueur2)

grille = Grille(hauteur=HAUTEUR, largeur=LARGEUR, fichier=FILENAME)
fin = 0
while not fin:
    grille.exporter()
    grille.exporter("./histo/grille_{}.txt".format(grille.etape))
    grille.exportPNG("./histo/grille_{0:0=2d}.png".format(grille.etape))
    grille.afficher()
    if grille.etape % 2:
         # le joueur 1 joue
        try:
            colonne = int(subprocess.check_output(["./{}".format(joueur1)]))
            resu = grille.jouer(J1, colonne)
        except:
            print "Input incorrect !"
            resu = 1
    else:
        # le joueur 2 joue
        try:
            colonne = int(subprocess.check_output(["./{}".format(joueur2)]))
            resu = grille.jouer(J2, colonne)
        except:
            print "Input incorrect !"
            resu = 1

    if resu:
        # Le joueur a mal joué = défaite
        print "Le joueur {} a joué un coup impossible (colonne {})".format(2-grille.etape % 2, colonne)
        fin = grille.etape % 2 + 1
    else:
        fin = grille.test_victoire()
    # passe a l'etape suivante
    grille.etape += 1

# Fin de la partie
if fin == 42:
    print "---- Egalite parfaite ! ----\n"
elif fin == 1:
    print "Le Joueur 1 ({}) a gagne !".format(joueur1)
elif fin == 2:
    print "Le Joueur 2 ({}) a gagne !".format(joueur2)
else:
    print "Oupsie !"

print "Grille finale : \n"
grille.afficher()
grille.exporter("./test/grille_{}.txt".format(grille.etape))
grille.exportPNG("./test/grille_{0:0=2d}.png".format(grille.etape))

# fais un gif de tout ca 1
subprocess.call(["convert", "-delay", "100", "-loop", "0", "./test/*.png", "animated.gif"])