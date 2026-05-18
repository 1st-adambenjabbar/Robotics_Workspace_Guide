# Isaac Sim ROS 2 Bridge Test

## Description
Ce sous-projet contient un script Python de vérification pour le pont ROS 2 d'NVIDIA Isaac Sim. Il s'agit d'un script simple qui confirme la préparation de l'environnement pour l'intégration d'Isaac Sim avec ROS 2, une étape cruciale pour les simulations robotiques avancées et l'IA.

## Prérequis
*   NVIDIA Isaac Sim installé et configuré.
*   ROS 2 installé et sourcé.
*   Le pont ROS 2 d'Isaac Sim doit être activé et fonctionnel.
*   Python 3 installé.

## Instructions d'exécution
1.  **Lancez NVIDIA Isaac Sim** et assurez-vous que le pont ROS 2 est activé (souvent via l'extension ROS dans Isaac Sim).
2.  Ouvrez votre terminal Linux.
3.  Sourcez votre environnement ROS 2 si ce n'est pas déjà fait :
    ```bash
    source /opt/ros/humble/setup.bash  # Adaptez à votre distribution
    ```
4.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/06_isaac_sim_test
    ```
5.  Exécutez le script Python :
    ```bash
    python3 isaac_ros_test.py
    ```

## Résultat attendu
Le script affichera un message indiquant qu'il s'agit d'un script de vérification et rappellera que Isaac Sim doit être en cours d'exécution. Dans un scénario réel, ce script serait étendu pour interagir avec les topics ROS 2 publiés par Isaac Sim pour une vérification plus approfondie.

```
NVIDIA Isaac Sim + ROS 2 Bridge Verification Script
Ensure Isaac Sim is running before executing this script.
```

## Concepts clés
*   **NVIDIA Isaac Sim :** Une plateforme de simulation robotique basée sur NVIDIA Omniverse, offrant des environnements virtuels très réalistes pour le développement, les tests et l'entraînement de robots basés sur l'IA.
*   **Pont ROS 2 (ROS 2 Bridge) :** Un composant essentiel qui permet la communication bidirectionnelle entre Isaac Sim et l'écosystème ROS 2, permettant aux nœuds ROS 2 de contrôler les robots dans la simulation et de recevoir des données de capteurs virtuels.
*   **Simulation avancée :** Isaac Sim permet de simuler des capteurs complexes (lidars, caméras, radars), des physiques réalistes et des environnements dynamiques, ce qui est crucial pour le développement de systèmes robotiques autonomes.
*   **Données synthétiques :** La capacité de générer de grandes quantités de données d'entraînement synthétiques à partir de la simulation, ce qui est précieux pour l'apprentissage automatique et la vision par ordinateur en robotique.
