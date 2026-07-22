# 05 - Synthetic Camera Data ★★★

## Goal
Place a camera looking at a scene and capture perfectly-labelled synthetic
data: RGB, depth (distance to image plane), and semantic segmentation.

## What you learn
- The `Camera` sensor: resolution, frequency, pose from Euler angles.
- Enabling extra annotators (`add_distance_to_image_plane_to_frame`,
  `add_semantic_segmentation_to_frame`).
- Why synthetic data is gold for training perception (free ground truth).

## Run
```bash
~/env_isaacsim/bin/python camera_synthetic.py
```
Outputs `rgb.npy` / `depth.npy` you can open with numpy/OpenCV.

## Extend it
- Add bounding-box / instance segmentation annotators.
- Use the Replicator API to script a full labelled dataset.
