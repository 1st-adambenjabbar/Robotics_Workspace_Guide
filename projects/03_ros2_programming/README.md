# Simple ROS 2 Node

## Description
Ce sous-projet présente un exemple minimaliste de nœud ROS 2 écrit en Python. Il illustre la structure de base d'un nœud, son initialisation et la manière dont il s'enregistre auprès du système ROS 2. C'est un point de départ idéal pour comprendre les fondations de la programmation avec ROS 2.

## Prérequis
*   Une installation fonctionnelle de ROS 2 (Humble ou Galactic recommandé) dans votre environnement Linux.
*   Python 3 installé.
*   ROS 2 doit être sourcé (voir `02_ros2_basics` pour plus de détails).

## Instructions d'exécution
1.  Ouvrez votre terminal Linux.
2.  Sourcez votre environnement ROS 2 si ce n'est pas déjà fait :
    ```bash
    source /opt/ros/humble/setup.bash  # Adaptez à votre distribution
    ```
3.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/03_ros2_programming
    ```
4.  Exécutez le script Python :
    ```bash
    python3 simple_node.py
    ```

## Résultat attendu
Le script lancera un nœud ROS 2 simple qui affichera un message dans le terminal, indiquant que le nœud a été démarré. Le nœud s'arrêtera après un court instant.

```
[INFO] [simple_publisher]: Simple ROS 2 Node has been started.
```

## Concepts clés
*   **`rclpy.init()` et `rclpy.shutdown()` :** Fonctions essentielles pour initialiser et arrêter la bibliothèque client ROS 2 pour Python.
*   **`Node` :** La classe de base pour tous les nœuds ROS 2. Un nœud est un processus exécutable qui effectue des calculs.
*   **`super().__init__('node_name')` :** Appelle le constructeur de la classe parente `Node` et donne un nom unique au nœud.
*   **`self.get_logger().info()` :** Utilisé pour afficher des messages d'information dans la console, utile pour le débogage et le suivi de l'état du nœud.
*   **`rclpy.spin_once()` :** Traite une seule fois toutes les callbacks en attente du nœud. Utilisé ici pour s'assurer que le message de démarrage est publié avant l'arrêt.
