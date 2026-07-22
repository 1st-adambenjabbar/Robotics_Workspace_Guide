#!/usr/bin/env python3
"""Compare global, Otsu and adaptive thresholding side by side."""
import argparse
import cv2
import numpy as np


def demo():
    img = np.tile(np.linspace(0, 255, 400, dtype=np.uint8), (300, 1))
    cv2.circle(img, (200, 150), 60, 230, -1)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default=None)
    args = ap.parse_args()
    gray = (cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
            if args.image else demo())

    _, glob = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    _, otsu = cv2.threshold(gray, 0, 255,
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adap = cv2.adaptiveThreshold(gray, 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 5)

    top = np.hstack([gray, glob])
    bot = np.hstack([otsu, adap])
    grid = np.vstack([top, bot])
    cv2.imshow('gray | global || otsu | adaptive', grid)
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
