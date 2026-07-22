#!/usr/bin/env python3
"""Real-time object detection. Uses Ultralytics YOLO if installed; otherwise
falls back to OpenCV's bundled DNN face detector so it always runs."""
import argparse
import cv2
import numpy as np


def run_yolo(source):
    from ultralytics import YOLO          # pip install ultralytics
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(source)
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        res = model(frame, verbose=False)[0]
        annotated = res.plot()
        cv2.imshow('YOLOv8', annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release(); cv2.destroyAllWindows()


def run_haar(source):
    print('Ultralytics not found -> fallback to Haar face detector.')
    cap = cv2.VideoCapture(source)
    cc = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in cc.detectMultiScale(gray, 1.3, 5):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('fallback detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release(); cv2.destroyAllWindows()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='0')
    args = ap.parse_args()
    src = int(args.source) if args.source.isdigit() else args.source
    try:
        run_yolo(src)
    except Exception as e:
        print('YOLO path failed:', e)
        run_haar(src)


if __name__ == '__main__':
    main()
