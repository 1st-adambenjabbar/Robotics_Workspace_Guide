from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    tb3_gazebo = FindPackageShare('turtlebot3_gazebo').find('turtlebot3_gazebo')
    world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo, 'launch', 'turtlebot3_world.launch.py')))
    teleop = ExecuteProcess(
        cmd=['ros2', 'run', 'teleop_spawn', 'teleop'],
        output='screen', prefix='xterm -e')
    return LaunchDescription([world, teleop])
