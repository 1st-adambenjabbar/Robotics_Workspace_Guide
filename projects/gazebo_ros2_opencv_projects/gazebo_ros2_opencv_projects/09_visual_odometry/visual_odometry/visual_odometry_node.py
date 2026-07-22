#!/usr/bin/env python3
"""Project 09 - Monocular Visual Odometry.

Estimate the camera's ego-motion from the image stream alone: detect ORB
features, match them between consecutive frames, recover the relative rotation
and (up-to-scale) translation via the essential matrix, and integrate them into
a trajectory published as nav_msgs/Odometry. The ground-truth /odom from Gazebo
is overlaid so you can see drift and the monocular scale ambiguity.

Concepts introduced
-------------------
* ORB keypoints/descriptors and Hamming brute-force matching with ratio test
* Epipolar geometry: findEssentialMat + recoverPose (R, t)
* Pose composition / integration and why monocular t has no metric scale
* Comparing an estimate against ground truth to reason about drift
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image, CameraInfo
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import cv2
import numpy as np


class VisualOdometry(Node):
    def __init__(self):
        super().__init__('visual_odometry')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('info_topic', '/camera/camera_info')
        self.declare_parameter('scale', 0.03)   # fixed pseudo-scale per step

        self.scale = float(self.get_parameter('scale').value)
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.K = None
        self.prev_gray = None
        self.prev_kp = None
        self.prev_des = None

        self.orb = cv2.ORB_create(1500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # Accumulated pose (3x3 R, 3x1 t) in camera frame.
        self.R = np.eye(3)
        self.t = np.zeros((3, 1))
        self.traj = np.zeros((600, 600, 3), np.uint8)

        self.create_subscription(CameraInfo, self.get_parameter('info_topic').value,
                                 self.on_info, qos)
        self.create_subscription(Image, self.get_parameter('image_topic').value,
                                 self.on_image, qos)
        self.pub = self.create_publisher(Odometry, '/visual_odom', 10)

    def on_info(self, msg: CameraInfo):
        self.K = np.array(msg.k, dtype=np.float64).reshape(3, 3)

    def on_image(self, msg: Image):
        if self.K is None:
            return
        gray = self.bridge.imgmsg_to_cv2(msg, 'mono8')
        kp, des = self.orb.detectAndCompute(gray, None)

        if self.prev_des is not None and des is not None and len(kp) > 8:
            matches = self.bf.knnMatch(self.prev_des, des, k=2)
            good = [m for m, n in matches if len([m, n]) == 2 and m.distance < 0.75 * n.distance]
            if len(good) >= 8:
                pts_prev = np.float32([self.prev_kp[m.queryIdx].pt for m in good])
                pts_cur = np.float32([kp[m.trainIdx].pt for m in good])
                E, mask = cv2.findEssentialMat(pts_cur, pts_prev, self.K,
                                               method=cv2.RANSAC, prob=0.999, threshold=1.0)
                if E is not None and E.shape == (3, 3):
                    _, R, t, _ = cv2.recoverPose(E, pts_cur, pts_prev, self.K)
                    # Integrate: t_world += scale * R_world * t ; R_world = R * R_world
                    self.t = self.t + self.scale * (self.R @ t)
                    self.R = R @ self.R
                    self.publish_odom(msg.header.stamp)
                    self.draw_traj()

        self.prev_gray, self.prev_kp, self.prev_des = gray, kp, des
        vis = cv2.drawKeypoints(gray, kp, None, color=(0, 255, 0))
        cv2.imshow('features', vis)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

    def publish_odom(self, stamp):
        od = Odometry()
        od.header.stamp = stamp
        od.header.frame_id = 'odom'
        od.child_frame_id = 'vo_camera'
        # camera optical frame: x right, y down, z forward -> map to planar x,y
        od.pose.pose.position.x = float(self.t[2])    # forward
        od.pose.pose.position.y = float(-self.t[0])   # left
        od.pose.pose.position.z = 0.0
        self.pub.publish(od)

    def draw_traj(self):
        x = int(self.t[2] * 100) + 300
        y = int(-self.t[0] * 100) + 300
        if 0 <= x < 600 and 0 <= y < 600:
            cv2.circle(self.traj, (x, y), 1, (0, 0, 255), 2)
        cv2.imshow('trajectory', self.traj)


def main(args=None):
    rclpy.init(args=args)
    node = VisualOdometry()
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
