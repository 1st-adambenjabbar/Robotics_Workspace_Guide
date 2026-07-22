# 06 - TF2 Frames ★★★

## Goal
Publish a static transform (a fixed sensor mount) and a dynamic transform
(a marker orbiting the robot), then inspect the tree in RViz / `tf2_tools`.

## What you learn
- `StaticTransformBroadcaster` vs `TransformBroadcaster`.
- `geometry_msgs/TransformStamped` and the parent/child convention.
- Timer-driven publishing.
- Visualising the TF tree.

## Run
```bash
ros2 run tf2_frames static_frame
ros2 run tf2_frames dynamic_frame
ros2 run tf2_tools view_frames        # generates frames.pdf
ros2 run tf2_ros tf2_echo base_link orbiting_marker
```

## Extend it
- Listen to the transform with a `TransformListener` and react to it.
- Add the frames to a robot in Gazebo and view them in RViz.
