# 06 - Face & Eye Detection ★★★

## Goal
Detect faces and eyes in a live stream using the classic Haar cascade
classifiers shipped with OpenCV (no downloads needed).

## What you learn
- `cv2.CascadeClassifier` and `detectMultiScale` parameters
  (`scaleFactor`, `minNeighbors`, `minSize`).
- Nested detection: search eyes only inside a detected face ROI.
- Where OpenCV stores its bundled models (`cv2.data.haarcascades`).

## Run
```bash
python3 face_detection.py --source 0
```

## Extend it
- Swap to the DNN face detector (more robust) — see project 10.
- Blur detected faces for an anonymisation demo.
