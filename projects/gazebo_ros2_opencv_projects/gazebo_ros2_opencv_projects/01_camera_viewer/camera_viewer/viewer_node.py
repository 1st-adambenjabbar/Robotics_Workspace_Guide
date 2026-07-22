#!/usr/bin/env python3
"""Project 01 - Camera Viewer.

The "hello world" of robot vision: subscribe to a camera topic published by
Gazebo, convert the ROS Image message into an OpenCV image with cv_bridge,
and display it in a window with a small HUD overlay (resolution + FPS).

Concepts introduced
-------------------
* rclpy Node lifecycle (init, spin, destroy)
* sensor_msgs/Image and the cv_bridge conversion
* QoS for sensor streams (BEST_EFFORT)
* The OpenCV imshow / waitKey render loop inside a ROS callback
"""
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraViewer(Node):
    def __init__(self):
        super().__init__('camera_viewer')

        # The camera topic differs per robot. TurtleBot3 waffle publishes on
        # /camera/image_raw. Make it a parameter so the node is reusable.
        self.declare_parameter('image_topic', '/camera/image_raw')
        topic = self.get_parameter('image_topic').get_parameter_value().string_value

        # Camera/LiDAR data should use a sensor-friendly QoS (best effort).
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )

        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.on_image, sensor_qos)

        self._last_t = time.time()
        self._fps = 0.0
        self.get_logger().info(f'Camera viewer listening on "{topic}". Press q in the window to quit.')

    def on_image(self, msg: Image):
        # Convert ROS Image -> OpenCV BGR image.
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Compute a smoothed FPS estimate.
        now = time.time()
        dt = now - self._last_t
        self._last_t = now
        if dt > 0:
            self._fps = 0.9 * self._fps + 0.1 * (1.0 / dt)

        h, w = frame.shape[:2]
        hud = f'{w}x{h}  |  {self._fps:4.1f} FPS'
        cv2.putText(frame, hud, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Camera Viewer', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CameraViewer()
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
