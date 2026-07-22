#!/usr/bin/env python3
"""Detect contours and classify each shape by its polygon vertex count."""
import argparse
import cv2
import numpy as np


def demo():
    img = np.full((400, 600, 3), 255, np.uint8)
    cv2.rectangle(img, (40, 60), (160, 180), (0, 0, 0), -1)
    cv2.circle(img, (320, 120), 70, (0, 0, 0), -1)
    pts = np.array([[480, 60], [560, 200], [400, 200]], np.int32)
    cv2.fillPoly(img, [pts], (0, 0, 0))
    return img


def classify(approx):
    v = len(approx)
    return {3: 'Triangle', 4: 'Rect/Square', 5: 'Pentagon'}.get(v, 'Circle')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default=None)
    args = ap.parse_args()
    img = cv2.imread(args.image) if args.image else demo()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c) < 200:
            continue
        approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
        name = classify(approx)
        M = cv2.moments(c)
        cx = int(M['m10'] / (M['m00'] + 1e-6))
        cy = int(M['m01'] / (M['m00'] + 1e-6))
        cv2.drawContours(img, [approx], -1, (0, 180, 0), 2)
        cv2.putText(img, name, (cx - 40, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow('shapes', img)
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
