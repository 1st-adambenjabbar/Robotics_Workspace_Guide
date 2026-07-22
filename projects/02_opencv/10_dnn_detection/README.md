# 10 - Real-Time DNN Object Detection ★★★★★

## Goal
Run a modern object detector live. If `ultralytics` (YOLOv8) is installed it
detects 80 COCO classes; otherwise it gracefully falls back to OpenCV's
bundled detector so the script always runs.

## What you learn
- Plugging a deep model into a real-time OpenCV capture loop.
- The detection output format (boxes, classes, confidences).
- Graceful degradation / dependency fallback design.
- The bridge from classical CV to deep learning (and to project 10 of the
  ROS+Gazebo category: semantic SLAM).

## Prerequisites (optional but recommended)
```bash
pip install ultralytics      # downloads yolov8n.pt on first run
```

## Run
```bash
python3 dnn_detection.py --source 0
python3 dnn_detection.py --source street.mp4
```

## Extend it
- Export detections to JSON / CSV per frame.
- Track detections across frames (ByteTrack / SORT).
- Publish them over a socket to feed a robotics stack.
