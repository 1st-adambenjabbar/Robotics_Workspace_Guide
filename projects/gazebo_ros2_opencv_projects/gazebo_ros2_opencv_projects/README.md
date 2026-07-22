# Gazebo · ROS 2 · OpenCV — 10 Projects, Beginner → Hardest

A hands-on ladder of robot-vision projects. Every project runs a robot in
**Gazebo**, processes its camera with **OpenCV**, and wires perception to action
through **ROS 2** nodes/topics. Each step adds exactly one new idea on top of the
previous, so by project 10 you've built a small visual-SLAM stack from scratch.

Target stack: **ROS 2 Humble · Gazebo Classic (gazebo11) · Python (rclpy) · OpenCV via cv_bridge**.
(The concepts port directly to Jazzy/Gazebo Sim; only topic names and launch
includes change.)

## The ladder

| #  | Project | New idea | Difficulty |
|----|---------|----------|------------|
| 01 | `camera_viewer` | Subscribe to a camera, `cv_bridge`, display | ★☆☆☆☆ |
| 02 | `color_detection` | HSV thresholding, contours, publish a detection | ★☆☆☆☆ |
| 03 | `line_follower` | ROI + centroid → first closed loop on `/cmd_vel` | ★★☆☆☆ |
| 04 | `object_follower` | Two coupled P-loops (center + approach) | ★★☆☆☆ |
| 05 | `aruco_navigation` | Camera intrinsics + ArUco pose, drive to marker | ★★★☆☆ |
| 06 | `lane_detection` | Canny + Hough lanes, steering | ★★★☆☆ |
| 07 | `depth_obstacle_avoidance` | Depth images, sector-based avoidance | ★★★★☆ |
| 08 | `visual_servoing` | Image-based visual servoing (feature error) | ★★★★☆ |
| 09 | `visual_odometry` | ORB + essential matrix, estimate ego-motion | ★★★★★ |
| 10 | `semantic_slam_yolo` | YOLO + depth + TF → a semantic map | ★★★★★ |

Each folder is a standalone ROS 2 (`ament_python`) package with its own
`README.md`, node(s), `launch/`, and `worlds/` where needed.

## Prerequisites

```bash
# ROS 2 Humble + Gazebo Classic integration + vision bits
sudo apt install \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-cv-bridge \
  ros-humble-turtlebot3* \
  ros-humble-vision-msgs \
  ros-humble-slam-toolbox \
  ros-humble-tf2-geometry-msgs

# Python libs
pip install opencv-contrib-python numpy
pip install ultralytics      # only for project 10 (YOLOv8)

# TurtleBot3 model (waffle has a camera) — projects 1-6, 9
echo 'export TURTLEBOT3_MODEL=waffle' >> ~/.bashrc
```

> `opencv-contrib-python` (not plain `opencv-python`) is required for `cv2.aruco`
> in projects 05 and 08.

## Build & run (typical workflow)

```bash
# 1. put this folder inside a colcon workspace
mkdir -p ~/ros2_ws/src
cp -r gazebo_ros2_opencv_projects ~/ros2_ws/src/
cd ~/ros2_ws

# 2. build everything (or one package with --packages-select)
colcon build --symlink-install
source install/setup.bash

# 3. launch a project (example: line follower)
export TURTLEBOT3_MODEL=waffle
ros2 launch line_follower line_follower.launch.py
```

Build just one package while iterating:

```bash
colcon build --packages-select color_detection && source install/setup.bash
```

## How the pieces fit together

```
Gazebo  --/camera/image_raw-->  [OpenCV node]  --/cmd_vel-->  Gazebo
 (sim)        (sensor_msgs/Image)   (rclpy)      (geometry_msgs/Twist)
```

Projects 1–2 stop at perception. Projects 3–8 close the loop to motion.
Projects 9–10 estimate state (odometry / a semantic map) from vision.

## Conventions used throughout

- Sensor topics use **BEST_EFFORT** QoS (matches Gazebo camera publishers).
- The processed-image error is normalized to `[-1, 1]` (0 = image center) so
  control gains are resolution-independent.
- Every controller node publishes a zero `Twist` on shutdown so the robot stops.
- Press **`q`** in any OpenCV window to quit a node cleanly.

## Suggested order & pacing

Do them in order — each README's "Extend it" section seeds the next project.
A comfortable pace is 1–2 projects per sitting; 07–10 each deserve their own.

## Troubleshooting quick hits

- **No image / black window** → check `ros2 topic list`; confirm the camera topic
  and pass it with `-p image_topic:=/your/topic`.
- **`cv2.aruco` missing** → you have plain `opencv-python`; install
  `opencv-contrib-python`.
- **Robot doesn't move** → is something else publishing `/cmd_vel`? Is the
  Gazebo sim un-paused (press play)?
- **TF errors in project 10** → SLAM/odom must be running so a `map` frame exists.

Licensed MIT. Built as a learning series — read the code, break it, extend it.
