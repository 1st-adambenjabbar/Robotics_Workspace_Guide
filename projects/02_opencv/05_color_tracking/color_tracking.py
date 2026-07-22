#!/usr/bin/env python3
"""Track a colored object from webcam/video using HSV trackbars."""
import argparse
import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='0',
                    help='webcam index or video path')
    args = ap.parse_args()
    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)

    cv2.namedWindow('ctrl')
    for name, val in [('Hl', 35), ('Sl', 80), ('Vl', 80),
                      ('Hh', 85), ('Sh', 255), ('Vh', 255)]:
        cv2.createTrackbar(name, 'ctrl', val, 255, lambda v: None)

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        g = lambda n: cv2.getTrackbarPos(n, 'ctrl')
        lo = np.array([g('Hl'), g('Sl'), g('Vl')])
        hi = np.array([g('Hh'), g('Sh'), g('Vh')])
        mask = cv2.inRange(hsv, lo, hi)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5)))
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            if cv2.contourArea(c) > 300:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (0, 255, 0), 2)
                cv2.circle(frame, (x + w // 2, y + h // 2), 4,
                           (0, 0, 255), -1)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
