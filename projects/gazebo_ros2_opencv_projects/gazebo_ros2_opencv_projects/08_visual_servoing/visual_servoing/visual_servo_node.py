#!/usr/bin/env python3
"""Project 08 - Image-Based Visual Servoing (IBVS).

Use the four corners of an ArUco marker as image point-features and regulate
them toward a desired (centered, fixed-size) configuration. This is a
simplified IBVS adapted to a non-holonomic differential-drive base: the
horizontal feature error maps to angular velocity and the scale error (current
vs desired marker side length in pixels) maps to linear velocity.

Concepts introduced
-------------------
* Feature vector s = stacked image-point coordinates, error e = s - s*
* The idea of the interaction (image Jacobian) matrix L mapping camera twist
  to feature velocity, and why a mobile base only spans part of that space
* Exponential error decay e_dot = -lambda * e as the control objective
* Tracking convergence by monitoring the residual feature error norm
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco
import numpy as np


class VisualServo(Node):
    def __init__(self):
        super().__init__('visual_servo')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('desired_side_px', 140.0)  # target apparent size
        self.declare_parameter('lambda_gain', 0.004)
        self.desired_side = float(self.get_parameter('desired_side_px').value)
        self.lam = float(self.get_parameter('lambda_gain').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.create_subscription(Image, self.get_parameter('image_topic').value,
                                 self.on_image, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.params = aruco.DetectorParameters()

    @staticmethod
    def side_length(corners):
        c = corners.reshape(4, 2)
        d = [np.linalg.norm(c[i] - c[(i + 1) % 4]) for i in range(4)]
        return float(np.mean(d))

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(gray, self.dict, parameters=self.params)

        twist = Twist()
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            c = corners[0].reshape(4, 2)
            centroid = c.mean(axis=0)

            # Feature errors.
            ex = centroid[0] - w / 2.0                       # horizontal pixels
            side = self.side_length(corners[0])
            e_scale = self.desired_side - side               # +ve -> too far

            # Exponential-decay control law (simplified IBVS).
            twist.angular.z = float(np.clip(-self.lam * ex, -1.0, 1.0))
            if abs(ex) < 60:
                twist.linear.x = float(np.clip(0.0015 * e_scale, -0.18, 0.2))

            err_norm = float(np.hypot(ex, e_scale))
            cv2.putText(frame, f'|e|={err_norm:6.1f}px', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.circle(frame, tuple(centroid.astype(int)), 6, (255, 0, 255), -1)
        else:
            twist.angular.z = 0.3

        self.cmd.publish(twist)
        cv2.imshow('visual_servo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = VisualServo()
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
