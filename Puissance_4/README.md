ZestArena - Puissance 4
=======================

Challenge Puissance 4 de la ZestArena.

Le but de ce challenge est de réaliser une IA de résolution de Puissance 4
contre un adversaire.

Les fichiers suivants sont présents :
+ `puissance4.py` : Maitre du jeu
+ `random_player.py` : Joueur de test qui joue aléatoirement

Afin de jouer, le maitre du jeu doit etre appelé via la commande suivante :
```bash
./puissance4.py joueur1 joueur2
```

Pour faire s'affronter deux joueurs aléatoires on ferait :
```bash
./puissance4.py random_player.py random_player.py
```

## Details techniques

## Python

Le maître du jeu est codé en python avec python 2.7. Il utilise aussi la
librairie Pillow (PIL) pour générer les images et imagemagick pour générer le
gif de replay de match. Une option sera bientot disponible pour désactiver ces
derniers.

## Contenu

Afin que les IA puissent jouer correctement, le jeu est mis à disposition sous
la forme suivante :
+ Un fichier nommé `grille.txt` est fourni dans le dossier principal.
Ce fichier contient l'état de la grille avant que le joueur joue (et est mis
à jour après son mouvement)
+ Un dossier nommé `histo` contient l'ensemble des grilles des manches. Chaque
grille st nommé sous le format suivant : `grille_xx.txt` avec `xx` le tour joué.

### Représentation d'une grille

Une grille est représenté de la manière suivante :
+ Un 0 est une case vide
+ Un 1 est une case occupé par un jeton de joueur 1
+ Un 2 est une case occupé par un jeton de joueur 2

Le format standard d'une grille est de 7 colonnes et 6 lignes.

La grille est representé de manière symbolique et analogue à celle d'une grille
de jeu normale. Autrement dit, le premier caractère lu dans le fichier
représente la case en haut à gauche du jeu,et la dernière ligne du fichier sera
la ligne du bas d'une grille de jeu classique.

Voici un extrait de représentation textuel où le joueur 2 gagne par diagonal :

```text
0000000
0000000
0002100
0201210
0201122
0112112
```

### GIF !

Un gif est généré à la fin du match pour rejouer le match sous forme visuel.