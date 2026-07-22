#!/usr/bin/env python3
"""Minimal keyboard teleop publisher to /cmd_vel (no external deps)."""
import sys, termios, tty, select
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

HELP = """
Keyboard teleop
---------------
   w        forward
a  s  d     left / stop / right
   x        backward
q / z       increase / decrease speed
CTRL-C      quit
"""

KEYS = {'w': (1, 0), 'x': (-1, 0), 'a': (0, 1), 'd': (0, -1), 's': (0, 0)}


class Teleop(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.lin = 0.22
        self.ang = 1.0
        self.get_logger().info(HELP)

    def get_key(self, settings):
        tty.setraw(sys.stdin.fileno())
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if r else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run(self):
        settings = termios.tcgetattr(sys.stdin)
        try:
            while rclpy.ok():
                key = self.get_key(settings)
                twist = Twist()
                if key in KEYS:
                    fx, fz = KEYS[key]
                    twist.linear.x = fx * self.lin
                    twist.angular.z = fz * self.ang
                elif key == 'q':
                    self.lin *= 1.1; self.ang *= 1.1
                elif key == 'z':
                    self.lin *= 0.9; self.ang *= 0.9
                elif key == '\x03':
                    break
                self.pub.publish(twist)
        finally:
            self.pub.publish(Twist())


def main():
    rclpy.init()
    node = Teleop()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
