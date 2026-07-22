#!/usr/bin/env python3
"""Detect faces (and eyes) with Haar cascades from a webcam/video stream."""
import argparse
import cv2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='0')
    args = ap.parse_args()
    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)

    base = cv2.data.haarcascades
    face_cc = cv2.CascadeClassifier(base + 'haarcascade_frontalface_default.xml')
    eye_cc = cv2.CascadeClassifier(base + 'haarcascade_eye.xml')

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cc.detectMultiScale(gray, 1.3, 5, minSize=(60, 60))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_g = gray[y:y + h, x:x + w]
            roi_c = frame[y:y + h, x:x + w]
            for (ex, ey, ew, eh) in eye_cc.detectMultiScale(roi_g, 1.1, 6):
                cv2.rectangle(roi_c, (ex, ey), (ex + ew, ey + eh),
                              (0, 255, 0), 1)
        cv2.putText(frame, f'faces: {len(faces)}', (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('faces', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
