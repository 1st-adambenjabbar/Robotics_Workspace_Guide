# 04 - Wall Follower (PD) ★★

## Goal
Keep a constant distance to the right-hand wall while moving forward, and
handle inner corners by turning away.

## What you learn
- Indexing a specific ray angle in a LaserScan.
- PD control on a lateral error signal.
- The classic "right-hand rule" maze-solving behaviour.

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 run wall_follower wall_follower --ros-args -p target:=0.5 -p kp:=3.0
```

## Extend it
- Add the integral term -> full PID.
- Switch to left-wall following with a parameter.
