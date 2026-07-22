# 02 - Odometry Reader ★

## Goal
Subscribe to `/odom` (`nav_msgs/Odometry`), extract position and heading,
and integrate the path length.

## What you learn
- The subscriber callback pattern.
- Quaternion → yaw conversion (the formula every roboticist memorises).
- Why odometry drifts (integration of wheel velocities).

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py   # terminal 1
ros2 run odom_reader odom_reader                            # terminal 2
ros2 run teleop_spawn teleop                                # drive it around
```

## Extend it
- Publish the travelled distance on a custom topic.
- Compare `/odom` against ground truth from the Gazebo `/model_states`.
