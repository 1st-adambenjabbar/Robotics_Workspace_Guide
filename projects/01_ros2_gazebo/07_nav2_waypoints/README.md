# 07 - Nav2 Waypoint Following ★★★★

## Goal
Use the production Nav2 navigation stack to follow a list of waypoints with
global + local planning and obstacle avoidance.

## What you learn
- The Nav2 lifecycle and the `BasicNavigator` / Simple Commander API.
- `followWaypoints` vs `goToPose`.
- Reading action feedback.

## Prerequisites
```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup \
                 ros-humble-nav2-simple-commander
```

## Run
```bash
export TURTLEBOT3_MODEL=waffle
# 1) bring up sim + nav2 (uses the prebuilt tb3 map)
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 launch nav2_bringup bringup_launch.py \
    map:=$HOME/turtlebot3_ws/maps/map.yaml use_sim_time:=true
# 2) set the initial pose in RViz, then:
ros2 run nav2_waypoints waypoints
```

## Extend it
- Load waypoints from a YAML file.
- Add `cancelTask()` on a keyboard interrupt.
