#!/usr/bin/env python3
"""Project 05 helper - generate ArUco marker PNGs.

Run this once to create marker images you can drop onto Gazebo objects as
textures (see worlds/markers.world and the README for how to apply them).

    ros2 run aruco_navigation generate_markers --ros-args -p ids:="[0,1,2]"
"""
import os
import rclpy
from rclpy.node import Node
import cv2
import cv2.aruco as aruco


class MarkerGen(Node):
    def __init__(self):
        super().__init__('generate_markers')
        self.declare_parameter('ids', [0, 1, 2])
        self.declare_parameter('size_px', 400)
        self.declare_parameter('out_dir', os.path.expanduser('~/aruco_markers'))

        ids = list(self.get_parameter('ids').value)
        size = int(self.get_parameter('size_px').value)
        out = self.get_parameter('out_dir').value
        os.makedirs(out, exist_ok=True)

        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        for i in ids:
            img = aruco.generateImageMarker(dictionary, int(i), size)
            path = os.path.join(out, f'marker_{i}.png')
            cv2.imwrite(path, img)
            self.get_logger().info(f'wrote {path}')
        self.get_logger().info('Done. Use these as box textures in Gazebo.')


def main(args=None):
    rclpy.init(args=args)
    node = MarkerGen()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
