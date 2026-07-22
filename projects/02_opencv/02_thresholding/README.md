# 02 - Thresholding & Masks ★

## Goal
Turn a grayscale image into a binary mask four different ways and compare them.

## What you learn
- Global vs Otsu (automatic) vs adaptive thresholding.
- When local/adaptive beats a single global threshold (uneven lighting).
- Stacking images for comparison with `np.hstack` / `np.vstack`.

## Run
```bash
python3 thresholding.py
python3 thresholding.py --image scan.png
```

## Extend it
- Apply the mask back to a color image with `cv2.bitwise_and`.
- Add morphological cleanup (`cv2.morphologyEx`, OPEN/CLOSE).
