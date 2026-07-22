import os
from glob import glob
from setuptools import setup

package_name = 'tf2_frames'

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
    description='Static and dynamic TF2 broadcasters: attach a sensor frame to the robot.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'static_frame = tf2_frames.static_broadcaster:main',
        'dynamic_frame = tf2_frames.dynamic_broadcaster:main',
        ],
    },
)
