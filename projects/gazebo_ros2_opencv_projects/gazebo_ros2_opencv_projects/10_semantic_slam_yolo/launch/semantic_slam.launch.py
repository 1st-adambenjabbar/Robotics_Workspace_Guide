#!/usr/bin/env python3
"""Project 10 bringup: YOLO detector + semantic mapper + SLAM.

This launch assumes a simulation is already (or also) providing:
  * an RGB image topic            (default /camera/image_raw)
  * a depth image + camera_info   (default /camera/depth/image_raw, .../camera_info)
  * TF: map -> ... -> camera_depth_optical_frame  (provided by SLAM + robot)

It starts slam_toolbox (async) for the map frame, then the two perception nodes.
Bring up the robot/world separately, e.g. a depth-capable robot like project 7's
depth_bot, or a TurtleBot3 waffle with a depth camera. Adjust the *_topic and
*_frame params to match your robot.

    export TURTLEBOT3_MODEL=waffle
    ros2 launch semantic_slam_yolo semantic_slam.launch.py
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    image_topic = LaunchConfiguration('image_topic', default='/camera/image_raw')
    depth_topic = LaunchConfiguration('depth_topic', default='/camera/depth/image_raw')
    info_topic = LaunchConfiguration('info_topic', default='/camera/depth/camera_info')
    camera_frame = LaunchConfiguration('camera_frame', default='camera_depth_optical_frame')
    use_slam = LaunchConfiguration('use_slam', default='true')

    args = [
        DeclareLaunchArgument('image_topic', default_value='/camera/image_raw'),
        DeclareLaunchArgument('depth_topic', default_value='/camera/depth/image_raw'),
        DeclareLaunchArgument('info_topic', default_value='/camera/depth/camera_info'),
        DeclareLaunchArgument('camera_frame', default_value='camera_depth_optical_frame'),
        DeclareLaunchArgument('use_slam', default_value='true'),
    ]

    # Optional SLAM for the map frame.
    slam_nodes = []
    try:
        slam = get_package_share_directory('slam_toolbox')
        slam_launch = os.path.join(slam, 'launch', 'online_async_launch.py')
        slam_nodes.append(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch),
            launch_arguments={'use_sim_time': 'true'}.items(),
            condition=IfCondition(use_slam)))
    except Exception:
        pass

    yolo = Node(
        package='semantic_slam_yolo', executable='yolo_detector_node',
        name='yolo_detector', output='screen',
        parameters=[{'image_topic': image_topic, 'model': 'yolov8n.pt'}])

    mapper = Node(
        package='semantic_slam_yolo', executable='semantic_mapper_node',
        name='semantic_mapper', output='screen',
        parameters=[{'depth_topic': depth_topic, 'info_topic': info_topic,
                     'camera_frame': camera_frame, 'map_frame': 'map'}])

    return LaunchDescription(args + slam_nodes + [yolo, mapper])
