# 🤖 ROS2 Humble Installation Guide (Ubuntu 22.04)

> Full installation tutorial for ROS2 Humble Hawksbill on Ubuntu Jammy (22.04) with 0 knowledge of linux commands It's Bash explained 🐚 

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
A locale is a set of parameters that defines the user's language, country, and character encoding preferences. ROS2 requires UTF-8 encoding.
UTF-8 stands for Unicode Transformation Format – 8-bit. It's the most widely used text encoding standard, capable of representing virtually every character from every language.

```bash
locale
```
explanation :
*Displays your current locale configuration. You're checking if UTF-8 is already set up before making changes.

If UTF-8 is missing:

```bash
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```
explanation :                      
* Installs the locales package, which provides tools to generate and manage locale settings on the system.
* locale-gen — generates the actual locale data files on disk based on what you specify. Here we generate:
 - en_US — basic American English locale.
 - en_US.UTF-8 — American English with full Unicode (UTF-8) support — this is what ROS2 needs.
* update-locale — writes the locale settings to /etc/default/locale, making them persistent across reboots.
* LC_ALL — stands for Locale Category ALL. It's an environment variable that overrides all individual locale categories at once (date format, number format, messages, etc.).
* LANG — stands for LANGuage. Sets the default language for the system when individual LC_* variables aren't set.
* export — makes the variable available to the current terminal session and all child processes immediately, without waiting for a reboot.
* his is needed because update-locale only writes to a file — it doesn't apply to the session you're currently in.

Verify:

```bash
locale
```
Run again to verify the changes. You should now see UTF-8 in every line.

---

# ➕ Add ROS2 Repository

## Install required packages

*A repository (or repo) is an online server that hosts software packages. By default, Ubuntu only knows about its own repositories. We need to add the official ROS2 repo so that apt can find and install ROS2 packages.

```bash
sudo apt install software-properties-common curl gnupg lsb-release -y
```
explaination: 

Installs four tools needed for the next steps:

- software-properties-common —: provides the (add-apt-repository) command to manage apt sources.
- curl : stands for Client URL. A command-line tool to transfer data from/to servers via URLs (HTTP, HTTPS, FTP, etc.).
- gnupg : stands for GNU Privacy Guard. Implements the GPG (GNU Privacy Guard) standard for encryption and digital signatures. Used to verify the authenticity of downloaded packages.
- lsb-release :provides the lsb_release command seen earlier, used to detect your Ubuntu version automatically in scripts.



## Add ROS2 GPG key

```bash
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
-o /usr/share/keyrings/ros-archive-keyring.gpg
```
expalination :
- curl — downloads the file from the URL.
-s — silent: hides the download progress bar.
-S — show-error: still displays error messages even in silent mode. -sS together = quiet but not blind.
-L — location: follows HTTP redirects automatically if the URL has moved.
- [https://raw.githubusercontent.com/...](https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
-o /usr/share/keyrings/ros-archive-keyring.gpg) — the direct URL to the official ROS GPG key hosted on GitHub. raw.githubusercontent.com serves raw file content (not the GitHub webpage).
-o — stands for output: saves the downloaded content to a file instead of printing it.
- usr/share/keyrings/ — the standard Linux directory for storing trusted apt signing keys.
- .gpg — file extension for a GPG (GNU Privacy Guard) key file. apt uses this to verify that packages from the ROS2 repo are legitimate and unmodified.
- \ — line continuation: tells bash the command continues on the next line (purely cosmetic, for readability).

## Add repository

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```
explaination : 

This long command builds and saves a ROS2 apt source entry. Breaking it down:

- echo "deb [...]" — prints the apt source line as text.
- deb — stands for Debian package. This keyword tells apt this is a binary package source (as opposed to deb-src for source code).
- arch=$(dpkg --print-architecture) — command substitution $(...): runs dpkg --print-architecture and inserts its output. dpkg is the low-level Debian Package manager. --print-architecture returns your CPU architecture: amd64 (64-bit Intel/AMD), arm64 (ARM 64-bit, used by Raspberry Pi 4), etc.
- signed-by=... — tells apt to verify packages using the GPG key we just downloaded. This is a security measure.
- http://packages.ros.org/ros2/ubuntu — the URL of the official Open Robotics ROS2 package server.
- $(. /etc/os-release && echo $UBUNTU_CODENAME) — another command substitution:

  . /etc/os-release — the . (dot) command sources the file, loading its variables into the shell. /etc/os-release is a standard Linux file containing OS metadata.
  $UBUNTU_CODENAME — an environment variable loaded from that file. On Ubuntu 22.04 it equals jammy. This makes the command automatically adapt to any Ubuntu version.

- main — refers to the main section of the ROS2 repository (the primary, fully-supported packages).
- I — the pipe operator. Takes the output (stdout) of the left command and feeds it as input (stdin) to the right command.
- sudo tee /etc/apt/sources.list.d/ros2.list — tee reads from stdin and writes to a file and stdout simultaneously. We use tee with sudo because writing to /etc/apt/sources.list.d/ requires root privileges. A plain sudo echo ... > file won't work because the shell handles the > redirection before sudo applies.
- > /dev/null — redirects stdout to /dev/null, a special Linux file that discards everything written to it. We don't need to see the output in the terminal.
- /etc/apt/sources.list.d/ — the directory where apt looks for additional repository source files. Each .list file inside it adds a new repository.
---

# 🔄 Update Package Index

```bash
sudo apt update
```
Now that the ROS2 repository is registered, apt update fetches the package catalog from it. After this, apt knows about all ros-humble-* packages and can install them.

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
Installs the complete ROS2 Humble environment, including:

RViz2 — ROS Visualization: a 3D GUI tool to visualize robot sensors, transforms, maps, and more.
Gazebo support — integration packages for the Gazebo physics simulator.
Navigation — the Nav2 stack (path planning, obstacle avoidance).
Demo nodes — ready-to-run example programs (talker, listener, etc.) to test your installation.
Visualization tools — rqt, rqt_graph, etc.
The package name follows the pattern ros-<distro>-<package>. humble is the ROS2 distribution name (like a version), named after Humble Hawksbill (ROS distributions are named after sea turtles 🐢).

---

# ⚙️ Source ROS2 Environment
Sourcing a file means executing it inside your current shell session, so that all variables and paths it defines become available immediately. ROS2 installs to /opt/ros/humble/ which your shell doesn't know about by default.

Temporary:

```bash
source /opt/ros/humble/setup.bash
```
- source — executes the script in the current shell (not a subprocess). This is essential: if you ran it with bash setup.bash, the environment variables would be set in a child process and disappear when it exits.
- /opt/ros/humble/setup.bash — a script auto-generated by ROS2 that exports all necessary paths: PATH, AMENT_PREFIX_PATH, PYTHONPATH, etc.
- /opt/ — stands for optional. The standard Linux directory for optional, third-party software not managed by the distro's core package system.
Permanent:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
- echo "..." — prints the text to stdout.
- >> — append redirection: adds the text to the end of the file without erasing its contents. (Unlike > which would overwrite the whole file.)
- ~/.bashrc — ~ is shorthand for your home directory (/home/yourusername). .bashrc is a hidden file (. prefix = hidden in Linux) that bash executes automatically every time you open a new terminal. Appending the source line here makes ROS2 available in every terminal from now on.
- source ~/.bashrc — reloads .bashrc immediately so the change takes effect in the current terminal without closing it.
---

# 🛠 Install Development Tools

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool -y
```
Installs three essential ROS2 development tools:

- python3-colcon-common-extensions — colcon stands for COLlective CONstruction. It's the build system used to compile ROS2 packages. The python3- prefix means it's a Python 3 package. common-extensions adds standard plugins (parallel builds, symlink install, etc.).
- python3-rosdep — rosdep stands for ROS DEPendency manager. It automatically resolves and installs system-level dependencies required by a ROS package, based on its package.xml file.
- python3-vcstool — vcs stands for Version Control System tool. It allows cloning multiple git repositories at once from a .repos manifest file. Very useful for multi-package workspaces.

---

# 🔧 Initialize rosdep

```bash
sudo rosdep init
rosdep update
```
- Initializes rosdep by creating its configuration directory at /etc/ros/rosdep/sources.list.d/ and writing the default sources. Must be run once with sudo. If you see "file already exists", rosdep is already initialized.
- Downloads the latest dependency databases from the internet. Run this without sudo — running as root can cause file permission issues that break rosdep later. Re-run this periodically to keep the database up to date.

---

# ✅ Test ROS2 Installation

We test with the classic pub/sub (publish/subscribe) demo. This verifies the ROS2 communication middleware (DDS) is working.

DDS — stands for Data Distribution Service. It's the underlying communication protocol ROS2 uses to send messages between nodes. Unlike ROS1 which used a central master node, ROS2's DDS is fully decentralized (peer-to-peer).

## Terminal 1

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```
ros2 run — the CLI command to run an executable from a ROS2 package.
CLI = Command Line Interface.
demo_nodes_cpp — the package name. A C++ demo package installed with ros-humble-desktop.
cpp = C++ (C Plus Plus).
talker — the node name. This node publishes (sends) "Hello World: X" messages on the /chatter topic.
A topic in ROS2 is a named communication channel. Nodes publish to topics or subscribe to them.

## Terminal 2

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

demo_nodes_py — same demo package but written in Python (py = Python).
listener — a node that subscribes to the /chatter topic and prints each message it receives.


✅ If Terminal 2 prints [INFO] I heard: Hello World: 1, 2, 3... → ROS2 is working.

---

# 🚀 Create a ROS2 Workspace

## Create workspace

A workspace is a directory structure where you organize and build your ROS2 packages. It's the equivalent of a project folder.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```
- mkdir — stands for MaKe DIRectory. Creates a new directory.
- -p — stands for parents. Creates all intermediate directories in the path if they don't exist yet. Without -p, mkdir ~/ros2_ws/src would fail if ros2_ws doesn't exist yet.
- ~/ros2_ws/src — the conventional workspace structure. src (source) is where your package source code lives.
- cd — stands for Change Directory. Moves your current working location to the specified path.
## Build workspace

```bash
colcon build
```
Builds all packages found in the src/ directory. colcon automatically detects package types (Python with ament_python, C++ with ament_cmake) and builds them appropriately.
- ament — the build framework used by ROS2. It wraps CMake and Python's setuptools.
- cmake — stands for Cross-platform MAKEfile. A build system generator widely used for C/C++ projects.

## Source workspace

```bash
source install/setup.bash
```
After building, colcon generates a new setup.bash in install/. Sourcing it overlays your workspace on top of the base ROS2 installation, making your custom packages available.
 *  overlay — in ROS2, workspaces can be stacked. Your workspace "overlays" the base ROS2 install,and your packages take priority if there's a name conflict.

Permanent:

```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
Same logic as before — appends to .bashrc so your workspace is automatically sourced in every new terminal.

---

# 📂 ROS2 Workspace Structure

```bash
ros2_ws/
 ├── build/      ← Intermediate build files (object files, CMake cache, etc.)
 ├── install/    ← Final installed files (executables, libraries, setup scripts)
 ├── log/        ← Build logs for debugging colcon issues
 └── src/        ← Your package source code lives here (git repos, .py, .cpp files)
```
These 4 directories are auto-generated by colcon build. You only manually work inside src/. Never edit build/ or install/ directly — they get regenerated on every build.

---

# 📦 Create Your First Package

Go into src:

```bash
cd ~/ros2_ws/src
```
Navigate into the src/ folder — packages must be created here so colcon can find them.

Create Python package:

```bash
ros2 pkg create my_robot_pkg --build-type ament_python --dependencies rclpy
```
- ros2 pkg create — the ROS2 CLI command to scaffold (auto-generate) a new package with all required files.
- my_robot_pkg — the name you give your package. By convention, use snake_case (lowercase with underscores).
- --build-type ament_python — specifies this is a Python package using the ament_python build system. Use ament_cmake for C++ packages instead.
- --dependencies rclpy — automatically adds rclpy as a dependency in package.xml and setup.py.

- rclpy — stands for ROS Client Library for Python. It's the Python API to write ROS2 nodes (publish, subscribe, create services, etc.). The C++ equivalent is rclcpp.
- package.xml — the manifest file that describes your package: its name, version, author, and dependencies.
- setup.py — the Python build script that tells colcon how to install your Python package and its entry points (executable scripts).

Build package:

```bash
cd ~/ros2_ws
colcon build
```
Source workspace:

```bash
source install/setup.bash
```
Build the workspace after creating the package, then source to make it available.

---

# 🔍 Useful ROS2 Commands

## List topics

```bash
ros2 topic list
```
Lists all topics currently active in the ROS2 network. A topic is a named bus over which nodes exchange messages (e.g., /scan, /cmd_vel, /odom).

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
