#!/usr/bin/env python3
"""Sparse Lucas-Kanade and dense Farneback optical flow on a video stream."""
import argparse
import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='0')
    ap.add_argument('--mode', choices=['lk', 'dense'], default='lk')
    args = ap.parse_args()
    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)

    ok, prev = cap.read()
    if not ok:
        raise SystemExit('No frames.')
    prev_g = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(prev_g, 100, 0.3, 7)
    mask = np.zeros_like(prev)
    hsv = np.zeros_like(prev); hsv[..., 1] = 255

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if args.mode == 'lk' and p0 is not None:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(prev_g, g, p0, None)
            if p1 is not None:
                good_new = p1[st == 1]
                good_old = p0[st == 1]
                for new, old in zip(good_new, good_old):
                    a, b = new.ravel(); c, d = old.ravel()
                    mask = cv2.line(mask, (int(a), int(b)),
                                    (int(c), int(d)), (0, 255, 0), 2)
                    frame = cv2.circle(frame, (int(a), int(b)), 3,
                                       (0, 0, 255), -1)
                p0 = good_new.reshape(-1, 1, 2)
            out = cv2.add(frame, mask)
        else:
            flow = cv2.calcOpticalFlowFarneback(
                prev_g, g, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            hsv[..., 0] = ang * 180 / np.pi / 2
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
            out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('optical flow', out)
        prev_g = g
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if p0 is None or (args.mode == 'lk' and len(p0) < 10):
            p0 = cv2.goodFeaturesToTrack(g, 100, 0.3, 7)
            mask = np.zeros_like(frame)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
