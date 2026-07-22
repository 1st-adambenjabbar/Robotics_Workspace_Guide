from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'semantic_slam_yolo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Adam',
    maintainer_email='adam@example.com',
    description='semantic_slam_yolo - part of the Gazebo/ROS2/OpenCV learning series',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yolo_detector_node=semantic_slam_yolo.yolo_detector_node:main',
            'semantic_mapper_node=semantic_slam_yolo.semantic_mapper_node:main',        ],
    },
)
