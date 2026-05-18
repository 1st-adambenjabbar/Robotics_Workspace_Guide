# CUDA & PyTorch Verification

## Description
Ce sous-projet contient un script Python qui vérifie la disponibilité de CUDA et son intégration avec PyTorch. L'accélération GPU est essentielle pour les charges de travail d'intelligence artificielle et les simulations robotiques complexes, et ce script confirme que votre configuration est prête à en tirer parti.

## Prérequis
*   Une carte graphique NVIDIA compatible CUDA.
*   Les pilotes NVIDIA correctement installés.
*   CUDA Toolkit installé.
*   PyTorch installé avec le support CUDA.
*   Python 3 installé.

## Instructions d'exécution
1.  Ouvrez votre terminal Linux.
2.  Naviguez jusqu'au répertoire de ce projet :
    ```bash
    cd /home/ubuntu/Robotics_Workspace_Guide/projects/05_cuda_test
    ```
3.  Exécutez le script Python :
    ```bash
    python3 cuda_check.py
    ```

## Résultat attendu
Le script affichera la version de PyTorch, indiquera si CUDA est disponible et, si c'est le cas, affichera des informations sur le périphérique CUDA détecté (par exemple, le nom de la carte graphique).

**Exemple de sortie (CUDA disponible) :**
```
PyTorch version: 2.0.1+cu117
CUDA available: True
Current device: 0
Device name: NVIDIA GeForce RTX 3080
```

**Exemple de sortie (CUDA non disponible) :**
```
PyTorch version: 2.0.1+cpu
CUDA available: False
```

## Concepts clés
*   **CUDA :** Une plateforme de calcul parallèle et un modèle de programmation développés par NVIDIA pour les GPU. Il permet aux développeurs d'utiliser les GPU pour l'informatique à usage général.
*   **PyTorch :** Une bibliothèque open-source d'apprentissage automatique utilisée pour des applications telles que la vision par ordinateur et le traitement du langage naturel. Elle est largement utilisée pour son support flexible de l'accélération GPU.
*   **`torch.cuda.is_available()` :** Fonction PyTorch qui renvoie `True` si un GPU compatible CUDA est détecté et que PyTorch a été compilé avec le support CUDA.
*   **`torch.cuda.get_device_name(0)` :** Renvoie le nom du périphérique CUDA à l'index spécifié (ici, le premier GPU).
