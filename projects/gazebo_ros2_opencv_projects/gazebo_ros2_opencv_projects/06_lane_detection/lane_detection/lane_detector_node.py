#!/usr/bin/env python3
"""Project 06 - Lane Detection.

A self-driving-car style lane detector: grayscale -> Gaussian blur -> Canny
edges -> trapezoidal region mask -> probabilistic Hough lines. Lines are split
into left/right by slope, averaged into two lane boundaries, and the lane
center offset is turned into a steering command.

Concepts introduced
-------------------
* Canny edge detection and parameter intuition
* Region-of-interest masking with a polygon (fillPoly)
* cv2.HoughLinesP and slope/intercept averaging
* Mapping lane-center offset to a steering rate
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np


class LaneDetector(Node):
    def __init__(self):
        super().__init__('lane_detector')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('kp', 0.004)
        self.declare_parameter('drive', True)
        topic = self.get_parameter('image_topic').value
        self.v = float(self.get_parameter('linear_speed').value)
        self.kp = float(self.get_parameter('kp').value)
        self.drive = bool(self.get_parameter('drive').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.on_image, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)

    def region(self, img):
        h, w = img.shape[:2]
        poly = np.array([[(int(0.05 * w), h), (int(0.45 * w), int(0.6 * h)),
                          (int(0.55 * w), int(0.6 * h)), (int(0.95 * w), h)]],
                        dtype=np.int32)
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, poly, 255)
        return cv2.bitwise_and(img, mask)

    def average_lane(self, lines, side, h):
        pts = []
        for x1, y1, x2, y2 in lines:
            if x2 == x1:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if side == 'left' and slope < -0.3:
                pts.append((slope, y1 - slope * x1))
            elif side == 'right' and slope > 0.3:
                pts.append((slope, y1 - slope * x1))
        if not pts:
            return None
        slope, intercept = np.mean(pts, axis=0)
        y1, y2 = h, int(0.62 * h)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return (x1, y1, x2, y2)

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        cropped = self.region(edges)

        lines = cv2.HoughLinesP(cropped, 2, np.pi / 180, 50,
                                minLineLength=40, maxLineGap=80)
        twist = Twist()
        if lines is not None:
            seg = lines[:, 0, :]
            left = self.average_lane(seg, 'left', h)
            right = self.average_lane(seg, 'right', h)
            centers = []
            for lane, color in ((left, (0, 255, 0)), (right, (0, 200, 255))):
                if lane:
                    cv2.line(frame, lane[:2], lane[2:], color, 6)
                    centers.append((lane[0] + lane[2]) / 2.0)
            if centers:
                lane_center = float(np.mean(centers))
                error = lane_center - w / 2.0
                twist.linear.x = self.v
                twist.angular.z = -self.kp * error
                cv2.circle(frame, (int(lane_center), h - 10), 6, (255, 0, 255), -1)

        if self.drive:
            self.cmd.publish(twist)
        cv2.imshow('lanes', frame)
        cv2.imshow('edges', cropped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = LaneDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd.publish(Twist())
        node.destroy_node()
        cv2.destroyAllWindows()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
