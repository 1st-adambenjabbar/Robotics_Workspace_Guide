# 01 · Camera Viewer  ★☆☆☆☆

**Package:** `camera_viewer`

## Goal
Subscribe to the robot's camera in Gazebo and display the live feed with OpenCV — the smallest possible perception node.

## What you learn
- rclpy node lifecycle (init / spin / destroy)
- sensor_msgs/Image ↔ OpenCV via cv_bridge
- BEST_EFFORT QoS for camera streams
- the imshow/waitKey render loop inside a callback

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch camera_viewer viewer.launch.py
# or run the node alone against any image topic:
ros2 run camera_viewer viewer_node --ros-args -p image_topic:=/camera/image_raw
```

## Extend it
- Add a grayscale/Canny toggle bound to a keypress.
- Overlay the topic's frame_id and timestamp.
- Record to a video file with cv2.VideoWriter.

## Troubleshooting
- Black window → wrong topic. Check `ros2 topic list` and pass image_topic.
- Window never appears → run with a display (not headless ssh).

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
