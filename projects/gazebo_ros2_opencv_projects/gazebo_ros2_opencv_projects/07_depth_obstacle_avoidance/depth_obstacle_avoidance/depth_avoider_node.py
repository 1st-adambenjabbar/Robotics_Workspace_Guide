#!/usr/bin/env python3
"""Project 07 - Depth-Camera Obstacle Avoidance.

Read a depth image, split the lower-middle band into left / center / right
sectors, take a robust near-distance per sector, and reactively steer toward
the most open direction (a vision-based Braitenberg / VFH-lite behaviour).

Concepts introduced
-------------------
* Depth image encodings: 32FC1 (metres) vs 16UC1 (millimetres)
* Robust statistics on noisy depth (ignoring NaN/0, using a low percentile)
* Sector-based reactive obstacle avoidance without a global map
* Why OpenCV is still useful on depth: ROI crops, masking, visualization
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np


class DepthAvoider(Node):
    def __init__(self):
        super().__init__('depth_avoider')
        self.declare_parameter('depth_topic', '/depth_camera/depth/image_raw')
        self.declare_parameter('stop_distance', 0.6)   # metres
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('turn_speed', 0.6)
        self.depth_topic = self.get_parameter('depth_topic').value
        self.stop = float(self.get_parameter('stop_distance').value)
        self.v = float(self.get_parameter('linear_speed').value)
        self.w = float(self.get_parameter('turn_speed').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.create_subscription(Image, self.depth_topic, self.on_depth, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)

    def sector_distance(self, depth_m):
        """Return (left, center, right) near-distances in metres."""
        h, w = depth_m.shape
        band = depth_m[int(0.35 * h):int(0.75 * h), :]   # ignore floor & sky
        thirds = np.array_split(band, 3, axis=1)
        out = []
        for s in thirds:
            valid = s[np.isfinite(s) & (s > 0.05)]
            out.append(np.percentile(valid, 5) if valid.size else np.inf)
        return out  # left, center, right

    def on_depth(self, msg: Image):
        depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        depth = np.asarray(depth, dtype=np.float32)
        if msg.encoding in ('16UC1', 'mono16'):
            depth = depth / 1000.0   # mm -> m

        left, center, right = self.sector_distance(depth)
        twist = Twist()
        if center > self.stop:
            twist.linear.x = self.v               # path ahead is clear
        else:
            twist.linear.x = 0.0                  # turn toward more open side
            twist.angular.z = self.w if left > right else -self.w

        self.cmd.publish(twist)
        self._visualize(depth, (left, center, right))

    def _visualize(self, depth, sectors):
        vis = np.nan_to_num(depth, nan=0.0, posinf=0.0)
        vis = cv2.normalize(vis, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        vis = cv2.applyColorMap(vis, cv2.COLORMAP_JET)
        labels = ['L', 'C', 'R']
        for i, (lab, d) in enumerate(zip(labels, sectors)):
            txt = f'{lab}:{d:4.2f}' if np.isfinite(d) else f'{lab}: inf'
            cv2.putText(vis, txt, (10 + i * 110, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow('depth', vis)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = DepthAvoider()
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
