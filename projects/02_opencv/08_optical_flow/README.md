# 08 - Optical Flow ★★★★

## Goal
Estimate motion between frames two ways: sparse Lucas-Kanade tracking of
corner features, and dense Farneback flow visualised as a color field.

## What you learn
- `goodFeaturesToTrack` (Shi-Tomasi corners).
- `calcOpticalFlowPyrLK` for sparse tracking + status filtering.
- `calcOpticalFlowFarneback` for dense flow, and HSV flow visualisation.
- The motion cues that feed visual odometry and tracking.

## Run
```bash
python3 optical_flow.py --mode lk     --source 0
python3 optical_flow.py --mode dense  --source clip.mp4
```

## Extend it
- Estimate the dominant camera motion from the flow field.
- Re-seed features adaptively when tracks are lost.
