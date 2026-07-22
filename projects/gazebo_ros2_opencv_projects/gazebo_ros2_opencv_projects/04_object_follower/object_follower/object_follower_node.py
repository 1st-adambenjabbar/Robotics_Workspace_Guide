#!/usr/bin/env python3
"""Project 04 - Object Follower.

Detect a colored object (HSV) and drive the robot to keep it centered while
approaching it to a target size. Two coupled proportional loops:
  * angular.z  <- horizontal centroid error  (keep object centered)
  * linear.x   <- area error                  (approach to a target area)

Concepts introduced
-------------------
* Combining perception (color blob) with a 2-DOF control law
* Using apparent size (area) as a crude range proxy
* Deadbands and saturation to keep motion smooth and safe
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class ObjectFollower(Node):
    def __init__(self):
        super().__init__('object_follower')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('hsv_low', [40, 80, 40])     # default: green
        self.declare_parameter('hsv_high', [80, 255, 255])
        self.declare_parameter('target_area_frac', 0.10)    # desired blob size
        self.declare_parameter('kp_ang', 1.2)
        self.declare_parameter('kp_lin', 1.5)

        topic = self.get_parameter('image_topic').value
        self.lo = np.array(self.get_parameter('hsv_low').value, np.uint8)
        self.hi = np.array(self.get_parameter('hsv_high').value, np.uint8)
        self.target = float(self.get_parameter('target_area_frac').value)
        self.kp_ang = float(self.get_parameter('kp_ang').value)
        self.kp_lin = float(self.get_parameter('kp_lin').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.on_image, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lo, self.hi)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        twist = Twist()
        if contours:
            c = max(contours, key=cv2.contourArea)
            area_frac = cv2.contourArea(c) / float(w * h)
            if area_frac > 0.002:
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                ex = (cx - w / 2.0) / (w / 2.0)          # [-1, 1]
                e_area = self.target - area_frac          # >0 -> too far -> go

                if abs(ex) > 0.05:
                    twist.angular.z = clamp(-self.kp_ang * ex, -1.5, 1.5)
                if abs(e_area) > 0.01:
                    twist.linear.x = clamp(self.kp_lin * e_area, -0.2, 0.22)

                x, y, bw, bh = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
        else:
            twist.angular.z = 0.4   # search

        self.cmd.publish(twist)
        cv2.imshow('object_follower', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = ObjectFollower()
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
