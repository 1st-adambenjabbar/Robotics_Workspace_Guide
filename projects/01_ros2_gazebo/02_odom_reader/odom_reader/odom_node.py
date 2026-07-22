#!/usr/bin/env python3
"""Read /odom, convert quaternion to yaw, accumulate travelled distance."""
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


def yaw_from_quat(q):
    siny = 2.0 * (q.w * q.z + q.x * q.y)
    cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny, cosy)


class OdomReader(Node):
    def __init__(self):
        super().__init__('odom_reader')
        self.sub = self.create_subscription(Odometry, '/odom', self.cb, 10)
        self.last = None
        self.dist = 0.0

    def cb(self, msg):
        p = msg.pose.pose.position
        yaw = yaw_from_quat(msg.pose.pose.orientation)
        if self.last is not None:
            self.dist += math.hypot(p.x - self.last[0], p.y - self.last[1])
        self.last = (p.x, p.y)
        self.get_logger().info(
            f'x={p.x:+.2f} y={p.y:+.2f} yaw={math.degrees(yaw):+6.1f} '
            f'deg  dist={self.dist:.2f} m')


def main():
    rclpy.init()
    node = OdomReader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
