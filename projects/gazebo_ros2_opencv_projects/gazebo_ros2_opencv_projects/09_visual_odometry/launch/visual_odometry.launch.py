#!/usr/bin/env python3
"""Project 09 bringup: TurtleBot3 in the standard world + visual odometry node.

    export TURTLEBOT3_MODEL=waffle
    ros2 launch visual_odometry visual_odometry.launch.py

Drive the robot (teleop) and watch the estimated trajectory vs ground-truth /odom.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    tb3 = get_package_share_directory('turtlebot3_gazebo')
    world_launch = os.path.join(tb3, 'launch', 'turtlebot3_world.launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(world_launch)),
        Node(
            package='visual_odometry', executable='visual_odometry_node',
            name='visual_odometry', output='screen',
        ),
    ])
