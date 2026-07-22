#!/usr/bin/env python3
"""Project 07 bringup: obstacles world + self-contained depth_bot + avoider node.

No TurtleBot3 needed here; depth_bot.sdf carries its own depth camera.
    ros2 launch depth_obstacle_avoidance depth_avoidance.launch.py
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('depth_obstacle_avoidance')
    world = os.path.join(pkg_share, 'worlds', 'obstacles.world')
    robot_sdf = os.path.join(pkg_share, 'worlds', 'depth_bot.sdf')

    gz = get_package_share_directory('gazebo_ros')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world}.items())
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz, 'launch', 'gzclient.launch.py')))

    spawn = Node(
        package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-entity', 'depth_bot', '-file', robot_sdf,
                   '-x', '0.0', '-y', '0.0', '-z', '0.1'],
        output='screen')

    avoider = Node(
        package='depth_obstacle_avoidance', executable='depth_avoider_node',
        name='depth_avoider', output='screen')

    return LaunchDescription([
        gzserver, gzclient,
        TimerAction(period=3.0, actions=[spawn]),
        TimerAction(period=6.0, actions=[avoider]),
    ])
