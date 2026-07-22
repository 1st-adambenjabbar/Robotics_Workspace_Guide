#!/usr/bin/env python3
"""Bring up TurtleBot3 in the standard Gazebo world and start the camera viewer.

Requires the turtlebot3 simulation packages and the env var TURTLEBOT3_MODEL.
Run:  export TURTLEBOT3_MODEL=waffle   (waffle has a camera)
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    image_topic = LaunchConfiguration('image_topic')

    tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    world_launch = os.path.join(tb3_gazebo, 'launch', 'turtlebot3_world.launch.py')

    return LaunchDescription([
        DeclareLaunchArgument('image_topic', default_value='/camera/image_raw'),

        IncludeLaunchDescription(PythonLaunchDescriptionSource(world_launch)),

        Node(
            package='camera_viewer',
            executable='viewer_node',
            name='camera_viewer',
            output='screen',
            parameters=[{'image_topic': image_topic}],
        ),
    ])
