# 05 · ArUco Navigation  ★★★☆☆

**Package:** `aruco_navigation`

## Goal
Detect ArUco markers, estimate each marker's 3D pose from camera intrinsics, and drive to the nearest one, stopping at a standoff distance.

## What you learn
- camera intrinsics from sensor_msgs/CameraInfo (fx, fy, cx, cy, D)
- cv2.aruco detection + estimatePoseSingleMarkers (tvec/rvec)
- turning a 3D target into linear + angular velocity
- consuming two streams (image + camera_info)

## Run
```bash
# 1) generate marker images to texture the boxes:
ros2 run aruco_navigation generate_markers --ros-args -p ids:=[0,1,2]
#    (writes ~/aruco_markers/marker_*.png — see note below to apply them)
export TURTLEBOT3_MODEL=waffle
ros2 launch aruco_navigation aruco_nav.launch.py
```

## Extend it
- Build a multi-marker waypoint mission (visit 0, then 1, then 2).
- Fuse rvec to align the robot perpendicular to the marker (docking).
- Publish marker poses as TF frames and visualize in RViz.

## Troubleshooting
- `cv2.aruco` AttributeError → install opencv-contrib-python.
- No pose → set marker_length to the real box face size (default 0.2 m).
- Markers undetected → the placeholder boxes are blank; apply the generated PNG as a Gazebo material/texture (see the note in this folder).

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
