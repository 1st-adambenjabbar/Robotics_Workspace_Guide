# 06 · Lane Detection  ★★★☆☆

**Package:** `lane_detection`

## Goal
A self-driving-style lane detector: Canny edges, a trapezoidal ROI, Hough lines split into left/right lanes, and a steering command from the lane-center offset.

## What you learn
- Canny edge detection and parameter intuition
- polygon ROI masking with fillPoly
- cv2.HoughLinesP + slope/intercept averaging
- lane-center offset → steering rate

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch lane_detection lane_detection.launch.py
# detect-only (no driving) to first tune the pipeline:
ros2 run lane_detection lane_detector_node --ros-args -p drive:=false
```

## Extend it
- Add a perspective (bird's-eye) warp before fitting for stability.
- Fit 2nd-order polynomials for curved lanes instead of straight lines.
- Reject outlier Hough segments with RANSAC.

## Troubleshooting
- No lanes → tune Canny thresholds and the ROI polygon to your camera height.
- Steers off the road → check the dashed line is inside the ROI band.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
