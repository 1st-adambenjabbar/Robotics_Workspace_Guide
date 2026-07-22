# 04 - Contours & Shape Recognition ★★

## Goal
Find external contours, filter by area, approximate each to a polygon, and
label it (triangle / rectangle / circle) at its centroid.

## What you learn
- `cv2.findContours` retrieval modes and approximation methods.
- `approxPolyDP` (Douglas-Peucker) and vertex counting for shape ID.
- Image moments to get a centroid.

## Run
```bash
python3 contours_shapes.py
```

## Extend it
- Add solidity / aspect-ratio features to separate squares from rectangles.
- Sort contours left-to-right and number them.
