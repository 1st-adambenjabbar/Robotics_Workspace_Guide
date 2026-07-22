#!/usr/bin/env python3
"""Publish a static transform base_link -> custom_sensor."""
import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticFrame(Node):
    def __init__(self):
        super().__init__('static_frame')
        self.br = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'custom_sensor'
        t.transform.translation.x = 0.2
        t.transform.translation.z = 0.15
        t.transform.rotation.w = 1.0
        self.br.sendTransform(t)
        self.get_logger().info('Static TF base_link -> custom_sensor sent.')


def main():
    rclpy.init()
    node = StaticFrame()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
