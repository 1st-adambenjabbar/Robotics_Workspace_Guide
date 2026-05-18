# Gazebo Launch Template

## Description
Ce sous-projet contient un fichier de lancement ROS 2 (`.launch.py`) servant de modèle pour démarrer une simulation Gazebo. Bien que ce fichier soit un exemple minimaliste, il pose les bases pour l'intégration de Gazebo dans un environnement ROS 2, permettant de lancer des mondes de simulation et d'y interagir avec des robots.

## Prérequis
*   Une installation fonctionnelle de ROS 2.
*   Gazebo installé et configuré pour fonctionner avec ROS 2 (généralement via `ros-humble-gazebo-ros-pkgs`).
*   ROS 2 doit être sourcé.

## Instructions d'exécution
1.  Ouvrez votre terminal Linux.
2.  Sourcez votre environnement ROS 2 si ce n'est pas déjà fait :
    ```bash
    source /opt/ros/humble/setup.bash  # Adaptez à votre distribution
    ```
3.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/04_gazebo_sim
    ```
4.  Pour lancer un monde Gazebo vide (ce fichier est un template, il ne lancera pas un monde complet sans configuration additionnelle) :
    ```bash
    ros2 launch gazebo_ros gazebo.launch.py # Exemple de commande pour lancer Gazebo
    ```
    *Note : Le fichier `empty_world.launch.py` fourni ici est un squelette. Pour une utilisation réelle, il faudrait y ajouter la configuration spécifique pour lancer le serveur et le client Gazebo, ainsi que des modèles de robots si nécessaire.*

## Concepts clés
*   **Fichiers de lancement ROS 2 (`.launch.py`) :** Ces fichiers Python sont utilisés pour démarrer plusieurs nœuds ROS 2 et d'autres processus (comme Gazebo) simultanément, en configurant leurs paramètres et leurs interconnexions.
*   **Gazebo :** Un simulateur de robotique 3D puissant qui permet de tester des algorithmes, de concevoir des robots et de réaliser des scénarios complexes dans un environnement virtuel réaliste.
*   **`launch_ros` :** Le paquet ROS 2 qui fournit les outils nécessaires pour intégrer des nœuds ROS 2 dans les fichiers de lancement Python.
*   **Environnements de simulation :** Gazebo permet de créer et de charger divers mondes virtuels, des environnements intérieurs simples aux paysages urbains complexes, pour simuler des capteurs et des interactions physiques.
