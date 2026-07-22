#!/usr/bin/env python3
"""Project 03 - Line Follower.

Classic differential-drive line following. Crop a band near the bottom of the
image, threshold the dark line, compute its centroid, and steer with a simple
proportional controller so the centroid stays in the image center.

Concepts introduced
-------------------
* Region of interest (ROI) cropping to look only where the line is
* Grayscale threshold / binary mask for a high-contrast line
* Centroid via image moments as the control error
* First closed loop: image error -> geometry_msgs/Twist on /cmd_vel
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np


class LineFollower(Node):
    def __init__(self):
        super().__init__('line_follower')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('linear_speed', 0.15)
        self.declare_parameter('kp', 0.005)          # gain on pixel error
        self.declare_parameter('roi_height', 60)     # band height in pixels
        self.declare_parameter('threshold', 100)     # below = line (dark)

        topic = self.get_parameter('image_topic').value
        self.v = float(self.get_parameter('linear_speed').value)
        self.kp = float(self.get_parameter('kp').value)
        self.roi_h = int(self.get_parameter('roi_height').value)
        self.thr = int(self.get_parameter('threshold').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.on_image, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Line follower running.')

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]

        roi = frame[h - self.roi_h:h, 0:w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, self.thr, 255, cv2.THRESH_BINARY_INV)

        M = cv2.moments(mask)
        twist = Twist()
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            error = cx - w // 2
            twist.linear.x = self.v
            twist.angular.z = -self.kp * error
            cv2.circle(roi, (cx, self.roi_h // 2), 6, (0, 0, 255), -1)
        else:
            # Line lost: stop and rotate to search.
            twist.linear.x = 0.0
            twist.angular.z = 0.3
        self.cmd.publish(twist)

        cv2.imshow('roi', roi)
        cv2.imshow('mask', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = LineFollower()
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
