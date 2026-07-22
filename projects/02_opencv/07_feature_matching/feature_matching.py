#!/usr/bin/env python3
"""ORB keypoints + BFMatcher ratio test, then estimate a homography between
two views of the same scene/object."""
import argparse
import cv2
import numpy as np


def synth_pair():
    a = np.full((300, 300, 3), 30, np.uint8)
    cv2.putText(a, 'AR', (60, 180), cv2.FONT_HERSHEY_SIMPLEX, 4,
                (255, 255, 255), 8)
    M = cv2.getRotationMatrix2D((150, 150), 20, 0.8)
    b = cv2.warpAffine(a, M, (300, 300))
    return a, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--img1', default=None)
    ap.add_argument('--img2', default=None)
    args = ap.parse_args()
    if args.img1 and args.img2:
        a, b = cv2.imread(args.img1), cv2.imread(args.img2)
    else:
        a, b = synth_pair()

    orb = cv2.ORB_create(1000)
    k1, d1 = orb.detectAndCompute(a, None)
    k2, d2 = orb.detectAndCompute(b, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(d1, d2, k=2)
    good = [m for m, n in matches if m.distance < 0.75 * n.distance]
    print(f'{len(k1)} / {len(k2)} keypoints, {len(good)} good matches')

    if len(good) >= 4:
        src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        print('Homography:\n', H)

    vis = cv2.drawMatches(a, k1, b, k2, good[:40], None,
                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imshow('matches', vis)
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
