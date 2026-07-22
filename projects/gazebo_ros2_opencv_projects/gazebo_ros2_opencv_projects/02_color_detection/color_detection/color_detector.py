#!/usr/bin/env python3
"""Project 02 - Color Detection.

Threshold an HSV color range, find contours, keep the largest blob and draw a
bounding box + centroid. The detection (centroid in normalized image
coordinates and blob area) is published so later projects can act on it.

Concepts introduced
-------------------
* BGR -> HSV conversion and why HSV is better for color segmentation
* cv2.inRange masks, morphological opening/closing to clean noise
* cv2.findContours / contourArea / boundingRect / moments (centroid)
* Publishing a structured result (geometry_msgs/PointStamped: x,y = centroid,
  z = area fraction) for downstream nodes
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
import cv2
import numpy as np


class ColorDetector(Node):
    def __init__(self):
        super().__init__('color_detector')
        self.declare_parameter('image_topic', '/camera/image_raw')
        # Default range targets a red object. HSV in OpenCV: H 0-179, S/V 0-255.
        self.declare_parameter('hsv_low', [0, 120, 70])
        self.declare_parameter('hsv_high', [10, 255, 255])
        self.declare_parameter('min_area', 300)

        topic = self.get_parameter('image_topic').value
        self.lo = np.array(self.get_parameter('hsv_low').value, dtype=np.uint8)
        self.hi = np.array(self.get_parameter('hsv_high').value, dtype=np.uint8)
        self.min_area = int(self.get_parameter('min_area').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.on_image, qos)
        self.pub = self.create_publisher(PointStamped, 'detection', 10)
        self.get_logger().info('Color detector running. Press q to quit.')

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lo, self.hi)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area >= self.min_area:
                x, y, bw, bh = cv2.boundingRect(c)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

                out = PointStamped()
                out.header = msg.header
                # Normalize to [-1, 1] with 0 at image center; z = area fraction.
                out.point.x = (cx - w / 2.0) / (w / 2.0)
                out.point.y = (cy - h / 2.0) / (h / 2.0)
                out.point.z = area / float(w * h)
                self.pub.publish(out)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = ColorDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
