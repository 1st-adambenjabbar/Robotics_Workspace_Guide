#!/usr/bin/env python3
"""Drive to a 2D goal using a heading + distance proportional controller."""
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


def yaw_from_quat(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                      1.0 - 2.0 * (q.y * q.y + q.z * q.z))


def norm(a):
    return math.atan2(math.sin(a), math.cos(a))


class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        self.declare_parameter('goal_x', 1.5)
        self.declare_parameter('goal_y', 1.0)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, '/odom', self.cb, 10)

    def cb(self, msg):
        p = msg.pose.pose.position
        yaw = yaw_from_quat(msg.pose.pose.orientation)
        gx = self.get_parameter('goal_x').value
        gy = self.get_parameter('goal_y').value
        dx, dy = gx - p.x, gy - p.y
        rho = math.hypot(dx, dy)
        t = Twist()
        if rho < 0.1:
            self.get_logger().info('Goal reached.')
            self.pub.publish(Twist())
            return
        head_err = norm(math.atan2(dy, dx) - yaw)
        t.angular.z = max(-1.5, min(1.5, 1.5 * head_err))
        t.linear.x = 0.0 if abs(head_err) > 0.5 else min(0.22, 0.5 * rho)
        self.pub.publish(t)


def main():
    rclpy.init()
    node = GoToGoal()
    try:
        rclpy.spin(node)
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
