#!/usr/bin/env python3
"""Project 05 - ArUco Detection + Navigation.

Detect ArUco markers in the camera stream, estimate each marker's 6-DOF pose
relative to the camera using the camera intrinsics, and drive the robot toward
the nearest marker, stopping at a target standoff distance.

Concepts introduced
-------------------
* Camera intrinsics from sensor_msgs/CameraInfo (fx, fy, cx, cy, distortion)
* cv2.aruco detection and estimatePoseSingleMarkers (tvec = 3D translation)
* Turning a 3D target into linear/angular velocity commands
* Subscribing to two synchronized streams (image + camera_info)
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import cv2.aruco as aruco
import numpy as np


class ArucoNav(Node):
    def __init__(self):
        super().__init__('aruco_nav')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('info_topic', '/camera/camera_info')
        self.declare_parameter('marker_length', 0.2)     # metres (real size)
        self.declare_parameter('standoff', 0.5)          # stop distance (m)

        self.marker_len = float(self.get_parameter('marker_length').value)
        self.standoff = float(self.get_parameter('standoff').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.K = None
        self.D = None

        self.create_subscription(CameraInfo, self.get_parameter('info_topic').value,
                                 self.on_info, qos)
        self.create_subscription(Image, self.get_parameter('image_topic').value,
                                 self.on_image, qos)
        self.cmd = self.create_publisher(Twist, '/cmd_vel', 10)

        self.dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.params = aruco.DetectorParameters()

    def on_info(self, msg: CameraInfo):
        self.K = np.array(msg.k, dtype=np.float64).reshape(3, 3)
        self.D = np.array(msg.d, dtype=np.float64)

    def on_image(self, msg: Image):
        if self.K is None:
            return
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(gray, self.dict, parameters=self.params)

        twist = Twist()
        if ids is not None and len(ids) > 0:
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                corners, self.marker_len, self.K, self.D)
            # Pick the closest marker (smallest forward distance z).
            zs = [t[0][2] for t in tvecs]
            idx = int(np.argmin(zs))
            tvec = tvecs[idx][0]            # [x_right, y_down, z_forward]
            x_off, _, dist = tvec

            aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, self.K, self.D, rvecs[idx], tvecs[idx],
                              self.marker_len * 0.5)

            bearing = math.atan2(x_off, dist)   # rad, +ve = marker to the right
            twist.angular.z = float(np.clip(-1.5 * bearing, -1.0, 1.0))
            range_err = dist - self.standoff
            if abs(bearing) < 0.25:
                twist.linear.x = float(np.clip(0.4 * range_err, 0.0, 0.22))

            cv2.putText(frame, f'id={int(ids[idx])} d={dist:.2f}m',
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            twist.angular.z = 0.3   # search

        self.cmd.publish(twist)
        cv2.imshow('aruco_nav', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cmd.publish(Twist())
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = ArucoNav()
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
