# ROS 2 Environment Check

## Description
Ce sous-projet contient un script Python simple pour vérifier si l'environnement ROS 2 est correctement sourcé. Il est crucial de s'assurer que ROS 2 est actif avant de tenter d'exécuter des nœuds ou des commandes ROS 2.

## Prérequis
*   Une installation fonctionnelle de ROS 2 (Humble ou Galactic recommandé) dans votre environnement Linux (WSL ou natif).
*   Python 3 installé.

## Instructions d'exécution
1.  Ouvrez votre terminal Linux.
2.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/02_ros2_basics
    ```
3.  Exécutez le script Python :
    ```bash
    python3 ros2_env_check.py
    ```

## Résultat attendu
Le script indiquera si la variable d'environnement `ROS_DISTRO` est définie, ce qui signifie que ROS 2 est correctement sourcé. Si ce n'est pas le cas, il vous invitera à sourcer votre installation ROS 2.

**Exemple de sortie (ROS 2 sourcé) :**
```
Checking ROS 2 Environment...
ROS 2 Distro: humble
```

**Exemple de sortie (ROS 2 non sourcé) :**
```
Checking ROS 2 Environment...
ROS 2 is not sourced. Please source your ROS 2 installation.
```

## Comment sourcer ROS 2
Si ROS 2 n'est pas sourcé, vous pouvez le faire en exécutant la commande suivante (adaptez le chemin et la distribution à votre installation) :
```bash
source /opt/ros/humble/setup.bash
```
Ou si vous utilisez un espace de travail personnalisé :
```bash
source ~/ros2_ws/install/setup.bash
```
