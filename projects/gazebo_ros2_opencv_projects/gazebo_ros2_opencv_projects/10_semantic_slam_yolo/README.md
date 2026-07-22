# 10 · Semantic SLAM with YOLO  ★★★★★

**Package:** `semantic_slam_yolo`

## Goal
Fuse YOLOv8 detections with depth + TF to place labeled objects into the map frame, building a persistent semantic map on top of geometric SLAM.

## What you learn
- wrapping a deep model (YOLOv8) in a ROS2 node
- back-projection: pixel + depth + intrinsics → 3D point
- TF2 lookups to move a point into the map frame
- online clustering/dedup so one real object = one landmark

## Run
```bash
pip install ultralytics    # first time only
export TURTLEBOT3_MODEL=waffle
# bring up a DEPTH-capable robot + world first (e.g. reuse project 07's depth_bot,
# or a waffle configured with a depth camera), then:
ros2 launch semantic_slam_yolo semantic_slam.launch.py \
  image_topic:=/depth_camera/image_raw \
  depth_topic:=/depth_camera/depth/image_raw \
  info_topic:=/depth_camera/depth/camera_info \
  camera_frame:=depth_camera_optical_frame
# visualize /semantic_map (MarkerArray) and the map in RViz2
```

## Extend it
- Add semantic navigation: 'go to the nearest chair' using the landmark map.
- Persist the semantic map to disk (YAML/JSON) and reload it.
- Replace the centroid-depth sample with full instance-mask back-projection.
- This is a natural extension of your ros2_drone_slam / semantic_slam work.

## Troubleshooting
- TF LookupException → SLAM/odom must publish a map frame; check `ros2 run tf2_tools view_frames`.
- All objects at origin → depth topic/encoding wrong, or camera_frame mismatched.
- Slow → use yolov8n.pt, downscale the image, or throttle inference.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
