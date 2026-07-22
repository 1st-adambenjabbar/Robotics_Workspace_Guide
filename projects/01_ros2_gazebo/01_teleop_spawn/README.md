# 01 - Teleop & Spawn ★

First contact with ROS 2 + Gazebo: spawn a robot and drive it.

## Goal
Launch the TurtleBot3 world in Gazebo and publish `geometry_msgs/Twist`
on `/cmd_vel` from the keyboard.

## What you learn
- The publisher pattern (`create_publisher`, `publish`).
- The `/cmd_vel` velocity command interface used by every diff-drive robot.
- How a launch file includes another package's launch file.
- Reading raw keyboard input without blocking the ROS spin.

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch teleop_spawn teleop.launch.py
# or, if you already have a world running:
ros2 run teleop_spawn teleop
```
Keys: `w/x` forward/back, `a/d` turn, `s` stop, `q/z` speed +/-.

## Extend it
- Add a dead-man key (hold to move).
- Publish to a namespaced topic `/robot1/cmd_vel` for multi-robot.

## Troubleshooting
- No movement? Check `ros2 topic echo /cmd_vel` while pressing keys.
- `turtlebot3_gazebo` not found → `sudo apt install ros-humble-turtlebot3*`.
