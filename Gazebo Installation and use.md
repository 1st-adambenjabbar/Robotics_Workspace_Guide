# 🤖 ROS2 Humble Installation Guide (Ubuntu 22.04)

> Full installation tutorial for ROS2 Humble Hawksbill on Ubuntu Jammy (22.04)

---

# 📌 Requirements

- Ubuntu 22.04 LTS (long term support) : the only where i personnally found it possible to install ros 
- Internet connection
- sudo privilege (super User DO)

Check Ubuntu version:

```bash
lsb_release -a
```
*  explanation : lsb_release ( stands for Linux Standard Base release. It's a command that displays information about your Linux distribution.)
* -a : flag meaning "all": shows all available information (distributor ID, description, release number, codename).

You should see:

```bash
Ubuntu 22.04
```

---

# 🔄 Update System

```bash
sudo apt update && sudo apt upgrade -y

```
explanation :
* sudo — runs the command as administrator (superuser).
* apt — stands for Advanced Package Tool. It's Ubuntu's built-in package manager, used to install, update, and remove software.
* update — fetches the list of available packages from all configured repositories. It does not install anything — it just refreshes the catalog.
* && — logical AND operator in bash. Runs the second command only if the first one succeeded (exit code 0).
* upgrade — actually downloads and installs newer versions of all packages already installed on your system.
* -y — stands for "yes". Automatically confirms any prompts so you don't have to type y manually.
---

# 🌍 Setup Locale

ROS2 requires UTF-8 locale.

```bash
locale
```

If UTF-8 is missing:

```bash
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Verify:

```bash
locale
```

---

# ➕ Add ROS2 Repository

## Install required packages

```bash
sudo apt install software-properties-common curl gnupg lsb-release -y
```

## Add ROS2 GPG key

```bash
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
-o /usr/share/keyrings/ros-archive-keyring.gpg
```

## Add repository

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

---

# 🔄 Update Package Index

```bash
sudo apt update
```

---

# 📦 Install ROS2 Humble

## Full Desktop Version (Recommended)

Includes:
- RViz2
- Gazebo support
- Navigation
- Demo nodes
- Visualization tools

```bash
sudo apt install ros-humble-desktop -y
```

---

# ⚙️ Source ROS2 Environment

Temporary:

```bash
source /opt/ros/humble/setup.bash
```

Permanent:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

# 🛠 Install Development Tools

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool -y
```

---

# 🔧 Initialize rosdep

```bash
sudo rosdep init
rosdep update
```

---

# ✅ Test ROS2 Installation

## Terminal 1

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

## Terminal 2

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

If installation works:

- Terminal 1 sends messages
- Terminal 2 receives messages

---

# 🚀 Create a ROS2 Workspace

## Create workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

## Build workspace

```bash
colcon build
```

## Source workspace

```bash
source install/setup.bash
```

Permanent:

```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

# 📂 ROS2 Workspace Structure

```bash
ros2_ws/
 ├── build/
 ├── install/
 ├── log/
 └── src/
```

---

# 📦 Create Your First Package

Go into src:

```bash
cd ~/ros2_ws/src
```

Create Python package:

```bash
ros2 pkg create my_robot_pkg --build-type ament_python --dependencies rclpy
```

Build package:

```bash
cd ~/ros2_ws
colcon build
```

Source workspace:

```bash
source install/setup.bash
```

---

# 🔍 Useful ROS2 Commands

## List topics

```bash
ros2 topic list
```

## List nodes

```bash
ros2 node list
```

## List services

```bash
ros2 service list
```

## Show running topics

```bash
ros2 topic echo /topic_name
```

## Visual graph

```bash
rqt_graph
```

## Open RViz2

```bash
rviz2
```

---

# 🤖 Install Gazebo Simulation

```bash
sudo apt install gazebo ros-humble-gazebo-ros-pkgs -y
```

Launch Gazebo:

```bash
gazebo
```

---

# 🧠 Install TurtleBot3 (Optional)

## Install packages

```bash
sudo apt install ros-humble-turtlebot3* -y
```

## Set model

```bash
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```

## Launch simulation

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

---

# 🔥 Common Fixes

## Reload ROS environment

```bash
source ~/.bashrc
```

## Fix dependencies

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## Clean workspace

```bash
rm -rf build install log
```

Rebuild:

```bash
colcon build
```

---

# 📚 Useful ROS2 Tools

| Tool | Purpose |
|---|---|
| RViz2 | Visualization |
| Gazebo | Simulation |
| rqt_graph | Node graph |
| colcon | Build system |
| rosdep | Dependency manager |

---

# 🎯 Final Check

Run:

```bash
ros2 doctor
```

If no major errors appear → ROS2 Humble is fully installed 🚀
