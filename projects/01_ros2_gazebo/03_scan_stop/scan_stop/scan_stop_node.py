#!/usr/bin/env python3
"""Drive forward until the front LIDAR sector detects an obstacle."""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ScanStop(Node):
    def __init__(self):
        super().__init__('scan_stop')
        self.declare_parameter('stop_distance', 0.5)
        self.declare_parameter('speed', 0.15)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            LaserScan, '/scan', self.cb, qos_profile_sensor_data)

    def front_min(self, scan):
        n = len(scan.ranges)
        # +-15 deg around the front (index 0)
        window = int((15.0 / 360.0) * n)
        idx = list(range(-window, window))
        vals = [scan.ranges[i] for i in idx
                if not math.isinf(scan.ranges[i]) and scan.ranges[i] > 0.05]
        return min(vals) if vals else float('inf')

    def cb(self, scan):
        d = self.front_min(scan)
        t = Twist()
        stop = self.get_parameter('stop_distance').value
        if d > stop:
            t.linear.x = self.get_parameter('speed').value
        else:
            self.get_logger().warn(f'Obstacle at {d:.2f} m -> STOP')
        self.pub.publish(t)


def main():
    rclpy.init()
    node = ScanStop()
    try:
        rclpy.spin(node)
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
