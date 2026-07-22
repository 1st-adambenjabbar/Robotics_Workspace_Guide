# Category 2 - OpenCV (pure vision, no ROS)

Ten standalone computer-vision projects, beginner to hardest. Each is a single
runnable Python script with its own README. They use only `opencv-contrib-python`
and `numpy`, so you can run them on any laptop without ROS or Gazebo.

| # | Project | Level | Core idea |
|---|---------|-------|-----------|
| 01 | image_basics        | ★     | load / display / save, color spaces |
| 02 | thresholding        | ★     | binary, adaptive, Otsu, masks |
| 03 | edges_blur          | ★★    | Gaussian/median blur, Sobel, Canny |
| 04 | contours_shapes     | ★★    | contours, area, polygon approx, shape ID |
| 05 | color_tracking      | ★★★   | HSV tracking from webcam/video, trackbars |
| 06 | face_detection      | ★★★   | Haar cascades, face + eyes |
| 07 | feature_matching    | ★★★   | ORB keypoints, BFMatcher, homography |
| 08 | optical_flow        | ★★★★  | Lucas-Kanade sparse + Farneback dense |
| 09 | camera_calibration  | ★★★★  | chessboard calibration, undistort, ArUco pose |
| 10 | dnn_detection       | ★★★★★ | real-time object detection via cv2.dnn / YOLO |

## Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Most scripts accept `--source` (a video file or webcam index, default `0`).
Press `q` to quit any window.
