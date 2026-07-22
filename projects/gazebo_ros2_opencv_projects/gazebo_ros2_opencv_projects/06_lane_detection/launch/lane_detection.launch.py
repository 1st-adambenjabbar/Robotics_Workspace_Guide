#!/usr/bin/env python3
"""Auto-generated bringup: custom Gazebo world + TurtleBot3 (waffle) + the lane_detection node.

Prereqs:  export TURTLEBOT3_MODEL=waffle
          ros2 launch lane_detection lane_detection.launch.py
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('lane_detection')
    world = os.path.join(pkg_share, 'worlds', 'road.world')

    gz = get_package_share_directory('gazebo_ros')
    tb3 = get_package_share_directory('turtlebot3_gazebo')
    tb3_launch = os.path.join(tb3, 'launch')

    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world}.items())
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz, 'launch', 'gzclient.launch.py')))
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(tb3_launch, 'robot_state_publisher.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items())
    spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(tb3_launch, 'spawn_turtlebot3.launch.py')),
        launch_arguments={'x_pose': x_pose, 'y_pose': y_pose}.items())

    return LaunchDescription([
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        gzserver, gzclient, rsp, spawn,
        Node(
            package='lane_detection', executable='lane_detector_node', name='lane_detector',
            output='screen',
        ),
    ])
