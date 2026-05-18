# WSL Setup Check

## Description
Ce sous-projet fournit un script simple pour vérifier la bonne configuration de votre environnement Windows Subsystem for Linux (WSL). Il s'assure que les outils essentiels comme `lsb_release`, `python3` et `git` sont installés et accessibles.

## Prérequis
*   Une installation fonctionnelle de WSL (Ubuntu recommandé).
*   Python 3 installé dans votre environnement WSL.
*   Git installé dans votre environnement WSL.

## Instructions d'exécution
1.  Ouvrez votre terminal WSL.
2.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/01_wsl_setup
    ```
3.  Rendez le script exécutable :
    ```bash
    chmod +x setup_check.sh
    ```
4.  Exécutez le script :
    ```bash
    ./setup_check.sh
    ```

## Résultat attendu
Le script affichera la version de votre distribution Linux, la version de Python 3 et la version de Git, confirmant que votre environnement WSL est prêt pour le développement robotique.

```
Checking WSL Environment...
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.4 LTS
Release:	22.04
Codename:	jammy
Checking Python version...
Python 3.10.12
Checking Git installation...
git version 2.34.1
WSL Setup verified!
```
