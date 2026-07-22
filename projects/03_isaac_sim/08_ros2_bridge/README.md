# 08 - ROS 2 Bridge ★★★★

## Goal
Enable the Isaac `ros2_bridge` extension and publish a simulated camera onto
a ROS 2 topic via an OmniGraph action graph — connecting Isaac Sim to your
ROS 2 Humble stack.

## What you learn
- Enabling extensions from script (`enable_extension`).
- OmniGraph: `OnPlaybackTick` -> `ROS2Context` -> `ROS2CameraHelper`.
- `get_render_product_path()` wiring for camera publishing.
- How Isaac Sim becomes a sensor source for your existing ROS 2 nodes.

## Prerequisites
- ROS 2 Humble sourced in the shell that launches Isaac Sim
  (`source /opt/ros/humble/setup.bash`), matching RMW.

## Run
```bash
source /opt/ros/humble/setup.bash
~/env_isaacsim/bin/python ros2_bridge.py
# elsewhere:
ros2 topic hz /isaac/camera/rgb
```

## Extend it
- Add a `ROS2PublishTransformTree` node to stream TF.
- Feed `/isaac/camera/rgb` into the OpenCV category's detector.
