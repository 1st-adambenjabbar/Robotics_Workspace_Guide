#!/usr/bin/env python3
"""Broadcast a dynamic frame that orbits around base_link, driven by a timer."""
import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class DynamicFrame(Node):
    def __init__(self):
        super().__init__('dynamic_frame')
        self.br = TransformBroadcaster(self)
        self.t0 = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.tick)

    def tick(self):
        dt = (self.get_clock().now() - self.t0).nanoseconds * 1e-9
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'orbiting_marker'
        t.transform.translation.x = 0.5 * math.cos(dt)
        t.transform.translation.y = 0.5 * math.sin(dt)
        t.transform.rotation.w = 1.0
        self.br.sendTransform(t)


def main():
    rclpy.init()
    node = DynamicFrame()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
