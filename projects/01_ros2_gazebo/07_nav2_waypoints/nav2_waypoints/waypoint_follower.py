#!/usr/bin/env python3
"""Drive a TurtleBot3 through waypoints using the Nav2 Simple Commander API."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


WAYPOINTS = [
    # (x, y, yaw_w)
    (1.5,  0.5, 1.0),
    (1.5, -1.0, 1.0),
    (-1.0, -1.0, 1.0),
    (0.0,  0.0, 1.0),
]


def make_pose(nav, x, y, w):
    p = PoseStamped()
    p.header.frame_id = 'map'
    p.header.stamp = nav.get_clock().now().to_msg()
    p.pose.position.x = float(x)
    p.pose.position.y = float(y)
    p.pose.orientation.w = float(w)
    return p


def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()
    goals = [make_pose(nav, *wp) for wp in WAYPOINTS]
    nav.followWaypoints(goals)
    while not nav.isTaskComplete():
        fb = nav.getFeedback()
        if fb:
            nav.get_logger().info(
                f'Heading to waypoint {fb.current_waypoint + 1}/{len(goals)}')
    result = nav.getResult()
    nav.get_logger().info(f'Result: {result}')
    nav.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
