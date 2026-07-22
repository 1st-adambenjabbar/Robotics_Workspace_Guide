# 06 - LIDAR / Range Sensor ★★★

## Goal
Create a rotating LIDAR inside a box room and read the per-beam depths.

## What you learn
- Creating a sensor via `omni.kit.commands` (`RangeSensorCreateLidar`).
- The range-sensor interface (`get_linear_depth_data`).
- FOV / resolution / rotation-rate parameters.

## Run
```bash
~/env_isaacsim/bin/python lidar_sensor.py
```

## Notes
- On RTX-LIDAR-only builds use the RTX LIDAR + the point-cloud annotator
  instead; the README in the asset library shows the exact command.

## Extend it
- Convert beams to an (x, y) point cloud and plot it.
- Mount the LIDAR on a moving robot and log scans.
