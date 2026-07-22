# 03 - LIDAR Emergency Stop ★★

## Goal
Move forward and stop automatically when the front laser sector reads a
distance below a threshold.

## What you learn
- `sensor_msgs/LaserScan` structure (`ranges`, `angle_min`, `angle_increment`).
- Sensor QoS (`qos_profile_sensor_data` = BEST_EFFORT).
- Extracting an angular window from a 360° scan.
- ROS 2 parameters (`declare_parameter`, override with `--ros-args -p`).

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 run scan_stop scan_stop --ros-args -p stop_distance:=0.6 -p speed:=0.2
```

## Extend it
- Instead of stopping, slow down proportionally to distance.
- Add left/right sectors and turn away from the obstacle (-> project 04/05).
