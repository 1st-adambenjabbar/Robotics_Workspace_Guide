#!/usr/bin/env python3
"""Load an image (or a generated gradient), show it in several color spaces,
and save the result. The 'hello world' of OpenCV."""
import argparse
import cv2
import numpy as np


def demo_image():
    """Generate a synthetic gradient so the script runs with zero assets."""
    img = np.zeros((300, 400, 3), np.uint8)
    for x in range(400):
        img[:, x] = (x % 256, (2 * x) % 256, (3 * x) % 256)
    cv2.putText(img, 'OpenCV', (120, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default=None, help='path to an image file')
    ap.add_argument('--out', default='output.png')
    args = ap.parse_args()

    img = cv2.imread(args.image) if args.image else demo_image()
    if img is None:
        raise SystemExit(f'Could not read {args.image}')

    print(f'shape={img.shape} dtype={img.dtype}')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow('BGR (original)', img)
    cv2.imshow('Grayscale', gray)
    cv2.imshow('HSV', hsv)
    cv2.imwrite(args.out, img)
    print(f'Saved {args.out}. Press q to quit.')
    while True:
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
