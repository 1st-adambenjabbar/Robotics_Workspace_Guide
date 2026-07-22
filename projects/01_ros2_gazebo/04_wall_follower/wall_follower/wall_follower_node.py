#!/usr/bin/env python3
"""Follow the right-hand wall at a target distance using a PD controller."""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class WallFollower(Node):
    def __init__(self):
        super().__init__('wall_follower')
        self.declare_parameter('target', 0.5)
        self.declare_parameter('kp', 3.0)
        self.declare_parameter('kd', 8.0)
        self.declare_parameter('speed', 0.15)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            LaserScan, '/scan', self.cb, qos_profile_sensor_data)
        self.prev_err = 0.0

    def ray(self, scan, deg):
        n = len(scan.ranges)
        i = int((deg / 360.0) * n) % n
        r = scan.ranges[i]
        return r if (not math.isinf(r) and r > 0.05) else 3.5

    def cb(self, scan):
        right = self.ray(scan, 270)       # straight to the right
        front = self.ray(scan, 0)
        err = self.get_parameter('target').value - right
        kp = self.get_parameter('kp').value
        kd = self.get_parameter('kd').value
        steer = kp * err + kd * (err - self.prev_err)
        self.prev_err = err
        t = Twist()
        t.linear.x = self.get_parameter('speed').value
        if front < 0.5:                   # inner corner -> turn left hard
            t.angular.z = 1.2
        else:
            t.angular.z = max(-1.5, min(1.5, steer))
        self.pub.publish(t)


def main():
    rclpy.init()
    node = WallFollower()
    try:
        rclpy.spin(node)
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
