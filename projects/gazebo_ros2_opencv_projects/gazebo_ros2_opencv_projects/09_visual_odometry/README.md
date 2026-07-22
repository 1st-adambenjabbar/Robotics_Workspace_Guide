# 09 · Monocular Visual Odometry  ★★★★★

**Package:** `visual_odometry`

## Goal
Estimate the camera's motion from the image stream alone: ORB features, matching, essential matrix, recoverPose, integrated into a trajectory and compared to ground-truth /odom.

## What you learn
- ORB keypoints/descriptors + Hamming matching with ratio test
- epipolar geometry: findEssentialMat + recoverPose (R, t)
- pose composition and the monocular scale ambiguity
- reasoning about drift against ground truth

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch visual_odometry visual_odometry.launch.py
# in another terminal, drive the robot:
ros2 run turtlebot3_teleop teleop_keyboard
ros2 topic echo /visual_odom --field pose.pose.position
```

## Extend it
- Recover metric scale using the known camera height or the depth camera.
- Add local bundle adjustment / a keyframe scheme to cut drift.
- Swap ORB for optical-flow (KLT) tracking and compare.

## Troubleshooting
- Trajectory explodes → too few/poor matches; add texture to the world or lower speed.
- No motion estimated → needs parallax; pure rotation is degenerate for the essential matrix.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
