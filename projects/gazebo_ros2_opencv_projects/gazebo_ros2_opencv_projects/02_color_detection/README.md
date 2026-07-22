# 02 · Color Detection  ★☆☆☆☆

**Package:** `color_detection`

## Goal
Segment a colored object in HSV, find its largest blob, draw a bounding box + centroid, and publish the detection for later projects to consume.

## What you learn
- why HSV beats BGR for color segmentation
- cv2.inRange masks + morphological open/close
- contours, contourArea, boundingRect, moments (centroid)
- publishing a structured result (PointStamped: centroid + area)

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch color_detection color_demo.launch.py
# tune the color range live (default = red):
ros2 run color_detection color_detector --ros-args -p hsv_low:=[40,80,40] -p hsv_high:=[80,255,255]
ros2 topic echo /detection
```

## Extend it
- Detect all three balls at once and publish a list.
- Add trackbars (cv2.createTrackbar) to tune HSV interactively.
- Handle the red hue wrap-around (two ranges, 0-10 and 170-179).

## Troubleshooting
- Nothing detected → your HSV range is off; visualize the `mask` window.
- Speckle detections → raise min_area or kernel size.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
