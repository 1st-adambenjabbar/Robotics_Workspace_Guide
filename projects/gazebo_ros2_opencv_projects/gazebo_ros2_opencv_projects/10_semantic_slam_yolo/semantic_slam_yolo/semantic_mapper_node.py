#!/usr/bin/env python3
"""Project 10 (node 2/2) - Semantic Mapper.

Fuse YOLO detections with depth + TF to place labeled objects into the map
frame, building a persistent semantic map on top of the geometric SLAM map
(slam_toolbox / Nav2). For each detection we sample the depth at the box
center, back-project to a 3D point in the camera optical frame, transform it
into the map frame via TF, cluster nearby detections of the same class, and
publish a visualization_msgs/MarkerArray for RViz.

Concepts introduced
-------------------
* Back-projection: pixel + depth + intrinsics -> 3D point
* TF2 lookups to move a point from camera_optical_frame into map
* Online clustering / dedup so one real object = one persistent landmark
* Layering semantics on a metric SLAM map (the basis of semantic navigation)
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image, CameraInfo
from vision_msgs.msg import Detection2DArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge

import tf2_ros
from tf2_geometry_msgs import do_transform_point
import numpy as np


class SemanticMapper(Node):
    def __init__(self):
        super().__init__('semantic_mapper')
        self.declare_parameter('depth_topic', '/camera/depth/image_raw')
        self.declare_parameter('info_topic', '/camera/depth/camera_info')
        self.declare_parameter('camera_frame', 'camera_depth_optical_frame')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('merge_radius', 0.5)   # metres for dedup

        self.camera_frame = self.get_parameter('camera_frame').value
        self.map_frame = self.get_parameter('map_frame').value
        self.merge_radius = float(self.get_parameter('merge_radius').value)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.K = None
        self.depth = None

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.create_subscription(CameraInfo, self.get_parameter('info_topic').value,
                                 self.on_info, qos)
        self.create_subscription(Image, self.get_parameter('depth_topic').value,
                                 self.on_depth, qos)
        self.create_subscription(Detection2DArray, '/yolo/detections',
                                 self.on_detections, 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/semantic_map', 10)

        # landmarks: list of dicts {label, x, y, z, n}
        self.landmarks = []

    def on_info(self, msg: CameraInfo):
        self.K = np.array(msg.k, dtype=np.float64).reshape(3, 3)

    def on_depth(self, msg: Image):
        d = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        d = np.asarray(d, dtype=np.float32)
        if msg.encoding in ('16UC1', 'mono16'):
            d = d / 1000.0
        self.depth = d

    def backproject(self, u, v, z):
        fx, fy = self.K[0, 0], self.K[1, 1]
        cx, cy = self.K[0, 2], self.K[1, 2]
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy
        return x, y, z

    def on_detections(self, msg: Detection2DArray):
        if self.K is None or self.depth is None:
            return
        try:
            tf = self.tf_buffer.lookup_transform(
                self.map_frame, self.camera_frame, rclpy.time.Time())
        except (tf2_ros.LookupException, tf2_ros.ExtrapolationException,
                tf2_ros.ConnectivityException):
            return

        h, w = self.depth.shape
        for det in msg.detections:
            if not det.results:
                continue
            label = det.results[0].hypothesis.class_id
            u = int(det.bbox.center.position.x)
            v = int(det.bbox.center.position.y)
            if not (0 <= u < w and 0 <= v < h):
                continue
            patch = self.depth[max(0, v - 3):v + 4, max(0, u - 3):u + 4]
            valid = patch[np.isfinite(patch) & (patch > 0.05)]
            if valid.size == 0:
                continue
            z = float(np.median(valid))
            x, y, z = self.backproject(u, v, z)

            p = PointStamped()
            p.header.frame_id = self.camera_frame
            p.point.x, p.point.y, p.point.z = x, y, z
            pm = do_transform_point(p, tf)
            self.add_landmark(label, pm.point.x, pm.point.y, pm.point.z)

        self.publish_markers()

    def add_landmark(self, label, x, y, z):
        for lm in self.landmarks:
            if lm['label'] == label and math.dist((lm['x'], lm['y'], lm['z']),
                                                   (x, y, z)) < self.merge_radius:
                n = lm['n']
                lm['x'] = (lm['x'] * n + x) / (n + 1)
                lm['y'] = (lm['y'] * n + y) / (n + 1)
                lm['z'] = (lm['z'] * n + z) / (n + 1)
                lm['n'] = n + 1
                return
        self.landmarks.append({'label': label, 'x': x, 'y': y, 'z': z, 'n': 1})
        self.get_logger().info(f'New landmark: {label} at ({x:.2f},{y:.2f})')

    def publish_markers(self):
        arr = MarkerArray()
        for i, lm in enumerate(self.landmarks):
            sph = Marker()
            sph.header.frame_id = self.map_frame
            sph.ns = 'objects'
            sph.id = i
            sph.type = Marker.SPHERE
            sph.action = Marker.ADD
            sph.pose.position.x = lm['x']
            sph.pose.position.y = lm['y']
            sph.pose.position.z = lm['z']
            sph.pose.orientation.w = 1.0
            sph.scale.x = sph.scale.y = sph.scale.z = 0.2
            sph.color.r, sph.color.g, sph.color.b, sph.color.a = 1.0, 0.3, 0.0, 0.9
            arr.markers.append(sph)

            txt = Marker()
            txt.header.frame_id = self.map_frame
            txt.ns = 'labels'
            txt.id = 1000 + i
            txt.type = Marker.TEXT_VIEW_FACING
            txt.action = Marker.ADD
            txt.pose.position.x = lm['x']
            txt.pose.position.y = lm['y']
            txt.pose.position.z = lm['z'] + 0.3
            txt.pose.orientation.w = 1.0
            txt.scale.z = 0.25
            txt.color.r = txt.color.g = txt.color.b = txt.color.a = 1.0
            txt.text = f"{lm['label']} ({lm['n']})"
            arr.markers.append(txt)
        self.marker_pub.publish(arr)


def main(args=None):
    rclpy.init(args=args)
    node = SemanticMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
