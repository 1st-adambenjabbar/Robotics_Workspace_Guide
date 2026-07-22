# Robotics Learning Suite

Quatre catégories de **10 projets progressifs** chacune (40 au total), du plus
simple au plus dur, chacune isolée dans son propre dossier et chaque projet avec
son **README détaillé** (objectif, ce que tu apprends, commande pour lancer,
pistes d'extension, dépannage).

```
robotics_learning_suite/
├── 01_ros2_gazebo/   # ROS 2 Humble + Gazebo SEUL (contrôle, capteurs, Nav2, SLAM)
├── 02_opencv/        # OpenCV SEUL (vision pure, sans ROS)
├── 03_isaac_sim/     # NVIDIA Isaac Sim (USD, articulations, capteurs synth., RL, bridge ROS2)
└── 04_simulink/      # Simulink / MATLAB (asservissement, modèles, robotique)
```

## Vue d'ensemble

### 01 — ROS 2 + Gazebo (★→★★★★★)
teleop_spawn · odom_reader · scan_stop · wall_follower · go_to_goal · tf2_frames
· nav2_waypoints · slam_mapping · multi_robot · bt_patrol
→ paquets `ament_python`, à mettre dans un workspace colcon.

### 02 — OpenCV (★→★★★★★)
image_basics · thresholding · edges_blur · contours_shapes · color_tracking ·
face_detection · feature_matching · optical_flow · camera_calibration ·
dnn_detection
→ scripts Python autonomes, `pip install -r requirements.txt`. Chacun tourne
avec une image/scène de secours synthétique : aucun asset requis.

### 03 — NVIDIA Isaac Sim (★→★★★★★)
hello_stage · spawn_primitives · load_robot_usd · articulation_control ·
camera_synthetic · lidar_sensor · domain_randomization · ros2_bridge ·
manipulator_pick · rl_cartpole
→ scripts à lancer avec le Python d'Isaac Sim (ton venv `C:\env_isaacsim`).

### 04 — Simulink / MATLAB (★→★★★★★)
first_order_step · pid_speed_control · state_space_mass · dc_motor ·
discrete_pid · vehicle_longitudinal · stateflow_traffic · diff_drive_kinematics
· pure_pursuit · mobile_robot_sensors
→ scripts `.m` qui **construisent le modèle Simulink par code** (lisible,
versionnable) puis le simulent. `cd` dans le dossier puis lancer le `build_*.m`.

## Comment lancer chaque catégorie
- **ROS 2 + Gazebo** : `colcon build` dans un workspace, `source install/setup.bash`, puis le README de chaque paquet.
- **OpenCV** : `python3 -m venv venv && source venv/bin/activate && pip install -r 02_opencv/requirements.txt`, puis `python3 <projet>.py`.
- **Isaac Sim** : lancer avec le Python bundle d'Isaac Sim, pas le Python système (chaque README rappelle la commande, option `--headless`).
- **Simulink** : MATLAB R2021b+, `cd` dans le dossier du projet, exécuter `build_<projet>`.

Les niveaux montent de ★ (premiers pas) à ★★★★★ (capstone qui fusionne tout
le reste de la catégorie). Ça recoupe ton portfolio `ros2_drone_slam` /
`semantic_slam`, ton Automatique II (PID discret / z-transform) et tes labos
MATLAB.
