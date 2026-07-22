# 09 - Camera Calibration & Undistortion ★★★★

## Goal
Recover a camera's intrinsic matrix and distortion coefficients from
chessboard photos, then undistort an image. Foundation for any metric vision.

## What you learn
- The pinhole model: intrinsics `K`, distortion, reprojection error.
- `findChessboardCorners` + `cornerSubPix` + `calibrateCamera`.
- `getOptimalNewCameraMatrix` and `undistort`.
- Saving/loading calibration with `np.savez`.

## Prepare
Print a 9x6 chessboard, take ~15 photos from varied angles/distances,
drop them in `calib/`.

## Run
```bash
python3 camera_calibration.py --images "calib/*.jpg" --cols 9 --rows 6 --square 0.025
```

## Extend it
- Load `calibration.npz` and run `cv2.aruco.estimatePoseSingleMarkers`.
- Compute per-image reprojection error to spot bad shots.
