import os
import subprocess

def check_ros2():
    print("Checking ROS 2 Environment...")
    ros_distro = os.environ.get('ROS_DISTRO')
    if ros_distro:
        print(f"ROS 2 Distro: {ros_distro}")
    else:
        print("ROS 2 is not sourced. Please source your ROS 2 installation.")

if __name__ == "__main__":
    check_ros2()
