# 07 · Depth-Camera Obstacle Avoidance  ★★★★☆

**Package:** `depth_obstacle_avoidance`

## Goal
Use a simulated depth camera: split the view into left/center/right sectors, take a robust near-distance per sector, and steer toward the most open direction.

## What you learn
- depth encodings: 32FC1 (m) vs 16UC1 (mm)
- robust stats on noisy depth (ignore NaN/0, low percentile)
- sector-based reactive avoidance with no global map
- a self-contained robot SDF with a depth-camera plugin

## Run
```bash
# self-contained: ships its own depth_bot.sdf, no TurtleBot3 needed
ros2 launch depth_obstacle_avoidance depth_avoidance.launch.py
# tune the stop distance:
ros2 run depth_obstacle_avoidance depth_avoider_node --ros-args -p stop_distance:=0.8
```

## Extend it
- Fuse with the LiDAR (LaserScan) for a wider field of view.
- Add hysteresis so it doesn't oscillate between left/right.
- Turn the sectors into a mini vector-field-histogram (VFH).

## Troubleshooting
- No depth topic → confirm `ros2 topic list` shows /depth_camera/depth/image_raw.
- Robot ignores obstacles → check encoding; if values are huge, it's mm not m.
- Robot won't spawn → give Gazebo a few seconds (launch staggers spawn by a timer).

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
