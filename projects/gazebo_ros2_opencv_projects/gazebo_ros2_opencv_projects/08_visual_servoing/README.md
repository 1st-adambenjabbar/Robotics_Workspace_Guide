# 08 · Image-Based Visual Servoing  ★★★★☆

**Package:** `visual_servoing`

## Goal
Regulate the four corners of an ArUco marker toward a desired (centered, fixed-size) configuration — a simplified IBVS adapted to a differential-drive base.

## What you learn
- feature vector s and error e = s − s*
- the interaction (image Jacobian) matrix idea and what a mobile base can/can't span
- exponential error decay ė = −λe as the control objective
- monitoring residual feature error for convergence

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch visual_servoing visual_servo.launch.py
ros2 run visual_servoing visual_servo_node --ros-args -p desired_side_px:=160
```

## Extend it
- Implement the full 8×k interaction matrix and a pseudo-inverse control law.
- Compare IBVS vs PBVS (position-based) convergence and image trajectories.
- Add a holonomic robot to actually use all DOF.

## Troubleshooting
- Same as project 05: needs opencv-contrib and visible markers.
- Oscillates → reduce lambda_gain.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
