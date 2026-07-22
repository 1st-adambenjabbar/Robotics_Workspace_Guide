# 07 - Feature Detection & Matching ★★★

## Goal
Detect ORB keypoints in two images, match them with a ratio test, and
estimate the homography that maps one onto the other.

## What you learn
- ORB (FAST + BRIEF) keypoints and binary descriptors.
- Brute-force matching with Hamming distance + Lowe's ratio test.
- RANSAC homography estimation (`cv2.findHomography`).
- This is the backbone of panorama stitching, AR, and visual odometry.

## Run
```bash
python3 feature_matching.py                       # synthetic rotated pair
python3 feature_matching.py --img1 a.jpg --img2 b.jpg
```

## Extend it
- Warp img1 onto img2 with `cv2.warpPerspective` to overlay them.
- Swap ORB for SIFT (in opencv-contrib) and compare.
