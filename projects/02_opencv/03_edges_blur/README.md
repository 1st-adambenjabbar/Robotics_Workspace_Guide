# 03 - Blur & Edges ★★

## Goal
Smooth an image and detect edges with Sobel and Canny, tuning the Canny
hysteresis thresholds live with trackbars.

## What you learn
- Why you blur *before* edge detection (noise suppression).
- Sobel gradients vs Canny's full pipeline (gradient + NMS + hysteresis).
- GUI trackbars with `cv2.createTrackbar` / `getTrackbarPos`.

## Run
```bash
python3 edges_blur.py
```

## Extend it
- Try `cv2.medianBlur` / `cv2.bilateralFilter` and compare edge quality.
- Feed the edges into `cv2.HoughLinesP` to detect straight lines.
