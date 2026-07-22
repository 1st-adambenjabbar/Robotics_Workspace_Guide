import os
from glob import glob
from setuptools import setup

package_name = 'slam_mapping'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
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
    description='Build a map with slam_toolbox while a simple explorer spins and translates.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'explore_spin = slam_mapping.explore_spin_node:main',
        ],
    },
)
