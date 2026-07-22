#!/usr/bin/env python3
"""Interactive Canny edge detector with trackbars for the two thresholds."""
import argparse
import cv2
import numpy as np


def demo():
    img = np.full((360, 480, 3), 40, np.uint8)
    cv2.rectangle(img, (60, 60), (220, 300), (200, 200, 200), -1)
    cv2.circle(img, (340, 180), 90, (120, 180, 250), -1)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default=None)
    args = ap.parse_args()
    img = cv2.imread(args.image) if args.image else demo()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.namedWindow('canny')
    cv2.createTrackbar('low', 'canny', 50, 500, lambda v: None)
    cv2.createTrackbar('high', 'canny', 150, 500, lambda v: None)
    print('Adjust trackbars; q to quit.')
    while True:
        lo = cv2.getTrackbarPos('low', 'canny')
        hi = cv2.getTrackbarPos('high', 'canny')
        edges = cv2.Canny(blur, lo, hi)
        sobel = cv2.magnitude(
            cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3),
            cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3))
        sobel = cv2.convertScaleAbs(sobel)
        view = np.hstack([gray, sobel, edges])
        cv2.imshow('canny', view)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
