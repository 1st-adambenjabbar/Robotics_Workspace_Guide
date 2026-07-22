# 05 - Color Object Tracking ★★★

## Goal
Track a colored object live from a webcam (or video), tuning the HSV bounds
with trackbars, and draw a bounding box + centroid on the largest blob.

## What you learn
- Live capture with `cv2.VideoCapture`.
- HSV thresholding (`inRange`) and why HSV beats RGB for color.
- Morphological opening to kill speckle noise.
- Picking the largest contour as the tracked object.

## Run
```bash
python3 color_tracking.py --source 0          # webcam
python3 color_tracking.py --source clip.mp4   # video file
```
Defaults are tuned for green. Move the trackbars for your object's color.

## Extend it
- Add a Kalman filter to smooth the centroid.
- Trigger an action when the object enters a region of interest.
