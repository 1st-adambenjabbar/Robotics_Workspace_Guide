# Guide Complet MATLAB

## Introduction

MATLAB (MATrix LABoratory) est un langage de programmation et un environnement de calcul numérique développé par :contentReference[oaicite:0]{index=0}.

Il est principalement utilisé pour :

- Le calcul scientifique
- L’analyse de données
- Le traitement du signal
- L’intelligence artificielle
- Les simulations
- Les mathématiques avancées
- La robotique
- Le contrôle automatique

---

# Sommaire

1. Installation
2. Syntaxe de base
3. Variables
4. Types de données
5. Opérations mathématiques
6. Vecteurs et matrices
7. Conditions
8. Boucles
9. Fonctions
10. Scripts
11. Graphiques
12. Fichiers
13. Structures et cellules
14. Programmation orientée objet
15. Debugging
16. Bonnes pratiques
17. Toolbox populaires
18. Exemples de projets
19. Ressources

---

# 1. Installation

Télécharger MATLAB :

- :contentReference[oaicite:1]{index=1}

Installer puis lancer MATLAB depuis :

- Windows
- Linux
- macOS

---

# 2. Syntaxe de base

## Commentaires

```matlab
% Commentaire sur une ligne

{
Commentaire
multi-lignes
}
```

## Affichage

```matlab
disp("Bonjour MATLAB")

a = 5;
fprintf("Valeur : %d\n", a);
```

## Point-virgule

```matlab
a = 5; % Pas d'affichage
b = 10  % Affichage automatique
```

---

# 3. Variables

## Déclaration

```matlab
x = 10;
nom = "MATLAB";
```

## Types dynamiques

```matlab
a = 10;
b = 3.14;
c = "texte";
d = true;
```

## Vérification du type

```matlab
class(a)
```

## Suppression

```matlab
clear x
```

---

# 4. Types de données

| Type | Exemple |
|---|---|
| Double | `3.14` |
| Integer | `int32(5)` |
| String | `"Bonjour"` |
| Char | `'A'` |
| Logical | `true` |
| Cell | `{1, "abc"}` |
| Struct | `person.nom = "Jean"` |

---

# 5. Opérations mathématiques

## Opérations basiques

```matlab
a = 5 + 3;
b = 10 - 2;
c = 4 * 2;
d = 8 / 2;
e = 2^3;
```

## Fonctions mathématiques

```matlab
sqrt(16)
sin(pi/2)
cos(0)
tan(pi/4)
log(10)
exp(1)
abs(-5)
```

## Constantes

```matlab
pi
inf
NaN
```

---

# 6. Vecteurs et matrices

## Création de vecteurs

```matlab
v = [1 2 3 4];
```

## Création de matrices

```matlab
A = [1 2; 3 4];
```

## Matrices spéciales

```matlab
zeros(3)
ones(3)
eye(3)
rand(3)
```

## Accès aux éléments

```matlab
A(1,2)
```

## Taille

```matlab
size(A)
length(v)
```

## Transposition

```matlab
A'
```

## Multiplication matricielle

```matlab
A * B
```

## Multiplication élément par élément

```matlab
A .* B
```

## Division élément par élément

```matlab
A ./ B
```

---

# 7. Conditions

## if / elseif / else

```matlab
x = 10;

if x > 0
    disp("Positif")
elseif x < 0
    disp("Négatif")
else
    disp("Zéro")
end
```

## switch

```matlab
jour = 1;

switch jour
    case 1
        disp("Lundi")
    case 2
        disp("Mardi")
    otherwise
        disp("Autre")
end
```

---

# 8. Boucles

## for

```matlab
for i = 1:5
    disp(i)
end
```

## while

```matlab
x = 1;

while x < 10
    x = x + 1;
end
```

## break

```matlab
for i = 1:10
    if i == 5
        break
    end
end
```

## continue

```matlab
for i = 1:10
    if mod(i,2) == 0
        continue
    end
    disp(i)
end
```

---

# 9. Fonctions

## Fonction simple

```matlab
function y = carre(x)
    y = x^2;
end
```

## Fonction avec plusieurs sorties

```matlab
function [somme, produit] = calcul(a, b)
    somme = a + b;
    produit = a * b;
end
```

## Appel

```matlab
r = carre(4);
```

---

# 10. Scripts

## Script MATLAB

Fichier :

```text
mon_script.m
```

Contenu :

```matlab
a = 5;
b = 10;
c = a + b;
disp(c)
```

Exécution :

```matlab
mon_script
```

---

# 11. Graphiques

## Graphe simple

```matlab
x = 0:0.1:10;
y = sin(x);

plot(x, y)
title("Sinus")
xlabel("x")
ylabel("y")
grid on
```

## Plusieurs courbes

```matlab
plot(x, sin(x))
hold on
plot(x, cos(x))
legend("sin", "cos")
```

## Histogramme

```matlab
data = randn(1000,1);
histogram(data)
```

## Scatter plot

```matlab
x = rand(100,1);
y = rand(100,1);

scatter(x,y)
```

---

# 12. Lecture et écriture de fichiers

## Sauvegarde

```matlab
save("data.mat")
```

## Chargement

```matlab
load("data.mat")
```

## Lecture texte

```matlab
fichier = fopen("test.txt", "r");
contenu = fread(fichier);
fclose(fichier);
```

## Écriture texte

```matlab
fichier = fopen("test.txt", "w");
fprintf(fichier, "Bonjour");
fclose(fichier);
```

---

# 13. Structures et cellules

## Structures

```matlab
personne.nom = "Jean";
personne.age = 25;
```

## Accès

```matlab
personne.nom
```

## Cellules

```matlab
C = {1, "texte", [1 2 3]};
```

## Accès cellule

```matlab
C{2}
```

---

# 14. Programmation orientée objet

## Classe simple

```matlab
classdef Voiture
    properties
        marque
        vitesse
    end

    methods
        function obj = Voiture(marque, vitesse)
            obj.marque = marque;
            obj.vitesse = vitesse;
        end

        function afficher(obj)
            disp(obj.marque)
        end
    end
end
```

## Utilisation

```matlab
v = Voiture("BMW", 200);
v.afficher();
```

---

# 15. Debugging

## Point d’arrêt

Cliquer dans la marge gauche de l’éditeur MATLAB.

## Commandes utiles

```matlab
dbstop if error
dbclear all
```

## Inspection

```matlab
whos
workspace
```

---

# 16. Bonnes pratiques

- Utiliser des noms explicites
- Commenter le code
- Éviter les boucles inutiles
- Préférer les opérations vectorisées
- Organiser les fonctions dans des fichiers séparés
- Utiliser Git pour le versioning
- Tester régulièrement le code

---

# 17. Toolbox populaires

| Toolbox | Utilité |
|---|---|
| Signal Processing Toolbox | Traitement du signal |
| Image Processing Toolbox | Vision et images |
| Statistics Toolbox | Statistiques |
| Deep Learning Toolbox | IA |
| Control System Toolbox | Automatique |
| Simulink | Simulation |

Documentation officielle :

- :contentReference[oaicite:2]{index=2}

---

# 18. Exemples de projets

## Analyse de données

```matlab
data = randn(1000,1);

mean(data)
std(data)

histogram(data)
```

## Résolution d’équation

```matlab
syms x
solve(x^2 - 4 == 0)
```

## Simulation simple

```matlab
t = 0:0.01:10;
x = sin(t);

plot(t, x)
```

## Génération d’un signal

```matlab
fs = 1000;
t = 0:1/fs:1;

signal = sin(2*pi*50*t);

plot(t, signal)
```

---

# 19. Ressources utiles

## Officielles

- :contentReference[oaicite:3]{index=3}
- :contentReference[oaicite:4]{index=4}
- :contentReference[oaicite:5]{index=5}

## GitHub

- :contentReference[oaicite:6]{index=6}

---

# Raccourcis utiles

| Action | Raccourci |
|---|---|
| Exécuter | F5 |
| Commenter | Ctrl + R |
| Décommenter | Ctrl + T |
| Aide | F1 |

---

# Conclusion

MATLAB est un environnement puissant pour :

- les mathématiques,
- la simulation,
- l’analyse scientifique,
- l’ingénierie,
- l’intelligence artificielle,
- le traitement des données.

La maîtrise des matrices et de la vectorisation est essentielle pour écrire du code MATLAB performant.
