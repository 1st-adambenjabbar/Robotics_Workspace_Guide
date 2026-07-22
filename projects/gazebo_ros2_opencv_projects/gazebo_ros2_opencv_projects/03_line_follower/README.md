# 03 · Line Follower  ★★☆☆☆

**Package:** `line_follower`

## Goal
Follow a ground line by thresholding a band near the image bottom, taking its centroid, and steering with a P controller — your first closed loop.

## What you learn
- region-of-interest cropping
- binary threshold for a high-contrast line
- centroid (moments) as a control error
- image error → geometry_msgs/Twist on /cmd_vel

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch line_follower line_follower.launch.py
# tune the proportional gain / speed:
ros2 run line_follower line_follower_node --ros-args -p kp:=0.008 -p linear_speed:=0.12
```

## Extend it
- Add a derivative term (PD) to kill oscillation on tight curves.
- Detect line loss and reverse the search direction intelligently.
- Use multiple ROI bands to anticipate curvature (look-ahead).

## Troubleshooting
- Robot weaves → lower kp. Robot cuts corners → raise look-ahead / lower speed.
- Sees the whole floor as line → adjust threshold; the track is black on light floor.

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
