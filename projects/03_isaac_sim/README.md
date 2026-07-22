# Category 3 - NVIDIA Isaac Sim

Ten progressive projects for **Isaac Sim 4.x / 5.x** (the Omniverse-based robot
simulator), beginner to hardest. Each is a standalone Python script that drives
Isaac Sim through the `SimulationApp` headless/GUI launcher, plus its own README.

These match your existing setup (pip-based venv at `C:\env_isaacsim`, Isaac Sim
5.1.0, CUDA in WSL2).

| # | Project | Level | Core idea |
|---|---------|-------|-----------|
| 01 | hello_stage          | ★     | launch SimulationApp, add ground + light, step |
| 02 | spawn_primitives     | ★     | add cubes/spheres with physics, query state |
| 03 | load_robot_usd       | ★★    | load a robot USD, inspect the articulation |
| 04 | articulation_control | ★★    | command joint positions/velocities |
| 05 | camera_synthetic     | ★★★   | attach a camera, grab RGB + depth + segmentation |
| 06 | lidar_sensor         | ★★★   | RTX/range LIDAR sensor, read the point cloud |
| 07 | domain_randomization | ★★★   | randomise textures/lights/poses for sim2real |
| 08 | ros2_bridge          | ★★★★  | publish camera + TF to ROS 2 via the bridge |
| 09 | manipulator_pick     | ★★★★  | Franka pick task with motion + gripper control |
| 10 | rl_cartpole          | ★★★★★ | a Gym-style RL environment + random/PPO policy |

## How to run
Isaac Sim scripts must run with Isaac Sim's bundled Python, not your system one:
```bash
# Linux (pip install):
~/.local/share/ov/pkg/isaac-sim-*/python.sh 01_hello_stage/hello_stage.py
# or with the pip venv:
source ~/env_isaacsim/bin/activate
python 01_hello_stage/hello_stage.py

# Windows (your env):
C:\env_isaacsim\Scripts\activate
python 01_hello_stage\hello_stage.py
```
Pass `--headless` (handled per script) to run without the GUI.

> API note: Isaac Sim's Python API has been migrating namespaces
> (`omni.isaac.core` -> `isaacsim.core`). These scripts use the `omni.isaac.*`
> paths that work on 2023.1–5.x; if you are on the very latest build and an
> import fails, swap the prefix as noted in each README.
