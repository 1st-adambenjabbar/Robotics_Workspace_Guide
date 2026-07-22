# 05 - Go To Goal ★★★

## Goal
Drive the robot to a parametric (x, y) goal in the odometry frame using a
two-stage proportional controller (rotate-then-translate).

## What you learn
- Combining a subscriber (odom) and a publisher (cmd_vel) in one node.
- Heading error normalisation to (-pi, pi].
- The "turn first, then drive" gating to avoid spiralling.

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 run go_to_goal go_to_goal --ros-args -p goal_x:=2.0 -p goal_y:=-1.0
```

## Extend it
- Accept a list of waypoints and visit them in sequence.
- Replace the gating with a unicycle (rho, alpha, beta) controller.
