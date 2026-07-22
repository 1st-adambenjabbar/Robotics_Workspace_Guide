#!/usr/bin/env python3
"""Calibrate a camera from chessboard images, then undistort and (optionally)
estimate ArUco marker pose with the recovered intrinsics."""
import argparse
import glob
import cv2
import numpy as np


def calibrate(images, cols, rows, square):
    objp = np.zeros((rows * cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2) * square
    objpoints, imgpoints, shape = [], [], None
    for path in images:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        shape = gray.shape[::-1]
        found, corners = cv2.findChessboardCorners(gray, (cols, rows))
        if found:
            corners = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            objpoints.append(objp); imgpoints.append(corners)
    if not objpoints:
        raise SystemExit('No chessboard corners found.')
    rms, K, dist, _, _ = cv2.calibrateCamera(
        objpoints, imgpoints, shape, None, None)
    return rms, K, dist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--images', default='calib/*.jpg')
    ap.add_argument('--cols', type=int, default=9)
    ap.add_argument('--rows', type=int, default=6)
    ap.add_argument('--square', type=float, default=0.025)
    args = ap.parse_args()
    files = sorted(glob.glob(args.images))
    if not files:
        print('No calibration images found at', args.images)
        print('Capture ~15 photos of a printed chessboard from many angles.')
        return
    rms, K, dist = calibrate(files, args.cols, args.rows, args.square)
    print(f'RMS reprojection error: {rms:.4f} px')
    print('Camera matrix K:\n', K)
    print('Distortion coeffs:\n', dist.ravel())
    np.savez('calibration.npz', K=K, dist=dist)
    print('Saved calibration.npz')

    sample = cv2.imread(files[0])
    h, w = sample.shape[:2]
    newK, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1)
    undist = cv2.undistort(sample, K, dist, None, newK)
    cv2.imshow('original | undistorted', np.hstack([sample, undist]))
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
