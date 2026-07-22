# 08 - SLAM Mapping ★★★★

## Goal
Run `slam_toolbox` in online-async mode to build an occupancy grid of the
Gazebo world while a helper node drives the robot around.

## What you learn
- The SLAM front-end/back-end split (scan matching + pose graph).
- The `/map`, `/scan`, `/odom` and TF relationship.
- Saving a map with `nav2_map_server`.

## Prerequisites
```bash
sudo apt install ros-humble-slam-toolbox ros-humble-nav2-map-server
```

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 run slam_mapping explore_spin
rviz2   # add the /map display
# when happy:
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

## Extend it
- Replace the blind explorer with frontier-based exploration.
- Feed the saved map into project 07 (Nav2).
