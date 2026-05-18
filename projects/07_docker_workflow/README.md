# ROS 2 Dockerfile

## Description
Ce sous-projet fournit un `Dockerfile` de base pour créer un environnement de développement ROS 2 conteneurisé. L'utilisation de Docker permet d'isoler votre environnement de développement, de garantir la reproductibilité et de faciliter le déploiement de vos applications robotiques.

## Prérequis
*   Docker installé sur votre système.
*   Accès à Internet pour télécharger les images de base.

## Instructions d'exécution
1.  Ouvrez votre terminal.
2.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/07_docker_workflow
    ```
3.  Construisez l'image Docker :
    ```bash
    docker build -t ros2_dev_env .
    ```
    Cela créera une image nommée `ros2_dev_env` basée sur le `Dockerfile`.
4.  Lancez un conteneur à partir de l'image :
    ```bash
    docker run -it ros2_dev_env
    ```
    Vous serez alors dans un terminal à l'intérieur du conteneur Docker, avec un environnement ROS 2 de base prêt à l'emploi.

## Contenu du Dockerfile
```dockerfile
FROM ros:humble-ros-base

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set workspace
WORKDIR /ros2_ws

CMD ["bash"]
```

## Concepts clés
*   **Docker :** Une plateforme qui permet de développer, de livrer et d'exécuter des applications dans des conteneurs. Les conteneurs sont des unités légères et autonomes qui incluent tout le nécessaire pour exécuter une application.
*   **`Dockerfile` :** Un fichier texte qui contient toutes les commandes qu'un utilisateur peut appeler sur la ligne de commande pour assembler une image. Il définit l'environnement du conteneur.
*   **`FROM` :** Spécifie l'image de base à partir de laquelle construire. Ici, `ros:humble-ros-base` est une image officielle de ROS 2 Humble.
*   **`RUN` :** Exécute des commandes pendant la construction de l'image. Utilisé ici pour installer `python3-pip`.
*   **`WORKDIR` :** Définit le répertoire de travail pour les instructions `RUN`, `CMD`, `ENTRYPOINT`, `COPY` et `ADD` qui suivent dans le `Dockerfile`.
*   **`CMD` :** Fournit des valeurs par défaut pour un conteneur en cours d'exécution. Ici, il lance un shell `bash`.
*   **Images et Conteneurs :** Une image est un modèle en lecture seule avec des instructions pour créer un conteneur Docker. Un conteneur est une instance exécutable d'une image.
