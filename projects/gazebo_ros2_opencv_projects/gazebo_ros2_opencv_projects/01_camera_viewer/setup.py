from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'camera_viewer'

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
    description='camera_viewer - part of the Gazebo/ROS2/OpenCV learning series',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'viewer_node=camera_viewer.viewer_node:main',        ],
    },
)
