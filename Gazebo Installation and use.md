# 🤖 Gazebo — Complete Installation & Usage Guide
> For **Ubuntu 22.04** (native) and **WSL2 on Windows 11 x64**
> Every command, abbreviation, and concept explained from scratch — Bash 🐚

---

# 📑 Table of Contents

1. [What is Gazebo?](#1-what-is-gazebo)
2. [Gazebo Versions — Which One to Use?](#2-gazebo-versions--which-one-to-use)
3. [Install on Ubuntu 22.04 (Native)](#3-install-on-ubuntu-2204-native)
4. [Install on WSL2 — Windows 11 x64](#4-install-on-wsl2--windows-11-x64)
5. [First Launch — Verify it Works](#5-first-launch--verify-it-works)
6. [Gazebo Interface Explained](#6-gazebo-interface-explained)
7. [Worlds — The Simulation Environment](#7-worlds--the-simulation-environment)
8. [Robots (Models) — Spawning into the World](#8-robots-models--spawning-into-the-world)
9. [Connecting Gazebo to ROS2](#9-connecting-gazebo-to-ros2)
10. [URDF & SDF — Describing Your Robot](#10-urdf--sdf--describing-your-robot)
11. [Sensors in Gazebo](#11-sensors-in-gazebo)
12. [Launch Gazebo from ROS2](#12-launch-gazebo-from-ros2)
13. [Common Fixes & Troubleshooting](#13-common-fixes--troubleshooting)
14. [Useful Commands Cheat Sheet](#14-useful-commands-cheat-sheet)

---

# 1. What is Gazebo?

**Gazebo** is a **robot simulation software**. It creates a virtual 3D world with realistic physics where you can:

- Test your robot code **without a real robot**
- Simulate **sensors** (LiDAR, camera, IMU, GPS)
- Apply **physics** (gravity, friction, collisions, inertia)
- Run **dangerous scenarios** safely (cliffs, obstacles, unknown terrain)

```
Real world:                     Gazebo simulation:
┌─────────────────────┐         ┌─────────────────────┐
│  Physical robot     │         │  Virtual robot       │
│  Real sensors       │  ───▶   │  Simulated sensors   │
│  Real environment   │  same   │  Virtual world       │
│  Damage possible    │  code   │  No damage risk      │
└─────────────────────┘         └─────────────────────┘
```

> Your ROS2 code runs **exactly the same** whether connected to real hardware or Gazebo. Gazebo publishes fake sensor data on the same topics a real robot would — your code doesn't know the difference.

---

# 2. Gazebo Versions — Which One to Use?

This is **important** — there are two completely different Gazebo generations:

| Name | Also called | Status | Use with |
|---|---|---|---|
| **Gazebo Classic** | `gazebo`, `gazebo11` | Old, still works | ROS2 Humble ✅ |
| **Gazebo Harmonic** (new) | `gz sim`, `Ignition` | New, recommended | ROS2 Humble ✅ |

> - **Gazebo Classic** — the original Gazebo (versions 1–11). Launched with `gazebo` command. Simpler, more tutorials available, but no longer actively developed.
> - **Gazebo Harmonic** (formerly **Ignition Gazebo**) — the next generation. Launched with `gz sim`. Better architecture, actively developed. More complex to set up.
> - For **beginners with ROS2 Humble**: use **Gazebo Classic (gazebo11)**. It's simpler and has far more tutorials.
> - **Ignition** — the project was renamed from "Ignition Gazebo" to just "Gazebo" (confusingly). The old Gazebo became "Gazebo Classic". This guide covers **both**.

---

# 3. Install on Ubuntu 22.04 (Native)

## Step 1 — Update your system first

```bash
sudo apt update && sudo apt upgrade -y
```

> Always update before installing. This avoids dependency conflicts between outdated and new packages.

---

## Step 2A — Install Gazebo Classic (gazebo11) — Recommended for beginners

```bash
sudo apt install gazebo -y
```

> Installs `gazebo11` (the version compatible with Ubuntu 22.04). The package is simply called `gazebo` but installs version 11 automatically.

Then install the **ROS2–Gazebo bridge** (the connector between them):

```bash
sudo apt install ros-humble-gazebo-ros-pkgs -y
```

> - `ros-humble-gazebo-ros-pkgs` — a set of ROS2 packages that:
>   - Make Gazebo **publish** simulated sensor data as ROS2 topics
>   - Let ROS2 **control** objects in Gazebo
>   - Provide **plugins** (code add-ons that add features to Gazebo)
> - **pkgs** = **p**ac**k**a**g**e**s**
> - **plugins** — loadable modules that extend Gazebo's functionality (e.g. a LiDAR plugin, a camera plugin, a differential drive plugin).

Also install useful extras:

```bash
sudo apt install ros-humble-gazebo-ros         -y   # core ROS2-Gazebo tools
sudo apt install ros-humble-gazebo-plugins     -y   # sensor and actuator plugins
sudo apt install ros-humble-gazebo-msgs        -y   # Gazebo message types
```

Verify:

```bash
gazebo --version
```

> Prints the installed Gazebo version. You should see `Gazebo multi-robot simulator, version 11.x.x`.

---

## Step 2B — Install Gazebo Harmonic (new generation) — Optional

```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
```

> Downloads the GPG key for the OSRF (Open Source Robotics Foundation) repository.
> - **OSRF** = **O**pen **S**ource **R**obotics **F**oundation — the organization that develops both ROS and Gazebo.

```bash
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable \
  $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
```

> Adds the OSRF Gazebo repository, same pattern as adding the ROS2 repo earlier.
> `lsb_release -cs` — prints the Ubuntu codename (`jammy` for 22.04).

```bash
sudo apt update
sudo apt install gz-harmonic -y
```

> Installs **Gazebo Harmonic**. Launched with `gz sim` instead of `gazebo`.

Install the ROS2 bridge for Harmonic:

```bash
sudo apt install ros-humble-ros-gz -y
```

> `ros-gz` — the ROS2 ↔ Gazebo Harmonic bridge package. Equivalent of `gazebo-ros-pkgs` for the new Gazebo.

---

# 4. Install on WSL2 — Windows 11 x64

## What is WSL2?

> - **WSL** = **W**indows **S**ubsystem for **L**inux. A feature of Windows that runs a real Linux kernel inside Windows.
> - **WSL2** = version 2, which uses a **full Linux kernel** (unlike WSL1 which translated syscalls). Much better performance and compatibility.
> - **x64** = 64-bit Intel/AMD architecture (`amd64`). The standard for modern laptops and desktops.
> - **WSLg** = **WSL** **G**raphics. Built into Windows 11. Allows running Linux **GUI applications** (like Gazebo) directly on Windows without extra software.

---

## Step 1 — Enable WSL2 on Windows 11

Open **PowerShell as Administrator** (right-click → Run as administrator):

```powershell
wsl --install
```

> Installs WSL2 with Ubuntu by default. Requires a **reboot** after.

If WSL is already installed, update it:

```powershell
wsl --update
wsl --set-default-version 2
```

> - `--update` — updates the WSL2 kernel to the latest version. Important for GPU and display support.
> - `--set-default-version 2` — makes WSL2 the default for all new distros.

Check your WSL version:

```powershell
wsl --list --verbose
```

> Shows all installed Linux distributions and which WSL version they use. You should see `VERSION 2` next to Ubuntu.

---

## Step 2 — Install Ubuntu 22.04 on WSL2

```powershell
wsl --install -d Ubuntu-22.04
```

> Installs the Ubuntu 22.04 distribution. `-d` = **d**istribution.
> After installation, it opens an Ubuntu terminal and asks you to create a username and password.

---

## Step 3 — Verify WSLg (display) is working

Inside your Ubuntu WSL2 terminal:

```bash
echo $DISPLAY
```

> `$DISPLAY` — an environment variable that tells Linux applications where to render their GUI window.
> On WSL2 with WSLg, it should print something like `:0` or a socket path. If it's empty, WSLg isn't set up.

Test with a simple GUI app:

```bash
sudo apt install x11-apps -y
xeyes
```

> `xeyes` — a tiny X11 demo app that shows a pair of eyes following your cursor. If a window appears, your display is working.
> - **X11** — the standard Linux display protocol. WSLg provides a built-in X11 server on Windows 11.

---

## Step 4 — Install ROS2 Humble inside WSL2

Follow the exact same steps as the Ubuntu installation (the guide assumes you already have ROS2 Humble). Inside WSL2, Ubuntu behaves identically to a real Ubuntu machine.

```bash
# Verify ROS2 is installed
source /opt/ros/humble/setup.bash
ros2 --version
```

---

## Step 5 — Install Gazebo inside WSL2

```bash
sudo apt update
sudo apt install gazebo ros-humble-gazebo-ros-pkgs -y
```

> Exactly the same command as native Ubuntu. WSL2 Ubuntu is a full Ubuntu — package installation is identical.

---

## Step 6 — Handle GPU & display for WSL2

WSL2 on Windows 11 uses **WSLg** for display — it should work out of the box. But Gazebo needs **OpenGL** for 3D rendering.

### Check OpenGL support:

```bash
sudo apt install mesa-utils -y
glxinfo | grep "OpenGL renderer"
```

> - `mesa-utils` — provides `glxinfo` and `glxgears`, OpenGL diagnostic tools.
> - `glxinfo` — displays detailed OpenGL information.
> - `| grep "OpenGL renderer"` — filters output to show only the renderer line.
> - **OpenGL** = **Open** **G**raphics **L**ibrary. The standard API for 3D rendering. Gazebo requires it to draw the simulation.
> - **Mesa** — the open-source OpenGL implementation for Linux. Provides software rendering if no GPU driver is found.

Expected output (WSL2 with no dedicated GPU):
```
OpenGL renderer string: llvmpipe (LLVM 15, 256 bits)
```

Expected output (WSL2 with NVIDIA GPU):
```
OpenGL renderer string: NVIDIA GeForce RTX XXXX/PCIe/SSE2
```

> - `llvmpipe` — **software rendering** using the CPU. Gazebo will work but slowly.
> - If you have an NVIDIA GPU, install the **CUDA WSL driver** on **Windows** (not inside WSL) from nvidia.com. WSL2 automatically uses it.

---

## Step 7 — Fix Gazebo display issues on WSL2

If Gazebo crashes or shows a black screen, add these environment variables:

```bash
# Add to ~/.bashrc for permanent fix
echo 'export LIBGL_ALWAYS_SOFTWARE=0'        >> ~/.bashrc
echo 'export MESA_GL_VERSION_OVERRIDE=3.3'   >> ~/.bashrc
echo 'export GAZEBO_IP=127.0.0.1'            >> ~/.bashrc
echo 'export DISPLAY=:0'                     >> ~/.bashrc
source ~/.bashrc
```

> - `LIBGL_ALWAYS_SOFTWARE=0` — do **not** force software rendering (use GPU if available). Set to `1` if Gazebo won't start at all (forces CPU rendering as fallback).
> - `MESA_GL_VERSION_OVERRIDE=3.3` — tells Mesa to report OpenGL version 3.3 even if auto-detected as lower. Gazebo needs at least OpenGL 3.3. This is a **compatibility workaround** common on WSL2.
> - `GAZEBO_IP=127.0.0.1` — tells Gazebo to bind to the **loopback** address (localhost). Avoids network issues inside WSL2. `127.0.0.1` = localhost = your own machine.
> - `DISPLAY=:0` — explicitly sets the display. WSLg sets this automatically but sometimes fails.

If Gazebo is still slow or crashing, force software rendering:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
gazebo
```

> `export VAR=value` without `>>` only applies to the **current terminal session**. Useful for testing before making it permanent.

---

## Step 8 — WSL2-specific performance tips

```bash
# Limit WSL2 memory and CPU usage — create/edit this file on WINDOWS
# Path: C:\Users\YourName\.wslconfig
```

Create `C:\Users\YourName\.wslconfig` on Windows with Notepad:

```ini
[wsl2]
memory=8GB          ; How much RAM WSL2 can use (adjust to your machine)
processors=4        ; How many CPU cores WSL2 can use
swap=2GB            ; Virtual memory
gpuSupport=true     ; Enable GPU passthrough (needed for Gazebo rendering)
```

> - `.wslconfig` — a Windows-side configuration file for WSL2. Restart WSL2 after editing: `wsl --shutdown` then reopen.
> - `gpuSupport=true` — enables GPU passthrough from Windows to WSL2. Requires the NVIDIA or Intel WSL2 driver installed on Windows.
> - **RAM** = **R**andom **A**ccess **M**emory. Gazebo uses a lot of it — give at least 4-8 GB.
> - **swap** — virtual memory on disk used when RAM is full. Slower than RAM.

Apply changes:

```powershell
# In PowerShell (Windows side)
wsl --shutdown
# Then reopen Ubuntu
```

---

# 5. First Launch — Verify it Works

## Launch Gazebo Classic

```bash
source /opt/ros/humble/setup.bash
gazebo
```

> - `source /opt/ros/humble/setup.bash` — always source ROS2 before launching Gazebo with ROS2 support. Otherwise the bridge won't work.
> - `gazebo` — launches Gazebo with an **empty world** and the GUI.

You should see a window with a grey ground plane and sky. That's Gazebo working.

## Launch Gazebo with a demo world

```bash
gazebo --verbose worlds/willowgarage.world
```

> - `--verbose` — prints detailed logs to the terminal. Very useful for debugging crashes.
> - `worlds/willowgarage.world` — a pre-installed demo world (an indoor office environment).
> - **world** — a file describing the 3D environment: objects, lighting, physics settings.

## Launch Gazebo Harmonic (if installed)

```bash
gz sim
```

> `gz sim` — launches the new Gazebo Harmonic with an empty world. The command is completely different from classic Gazebo.

```bash
gz sim shapes.sdf
```

> Launches with a demo world containing basic 3D shapes. `.sdf` = **S**imulation **D**escription **F**ormat — the file format for Gazebo worlds and models.

---

# 6. Gazebo Interface Explained

```
┌─────────────────────────────────────────────────────────────────┐
│  Menu Bar  [File] [Edit] [Camera] [View] [Window] [Help]        │
├──────────┬──────────────────────────────────────┬───────────────┤
│          │                                      │               │
│  LEFT    │         3D VIEWPORT                  │  RIGHT        │
│  PANEL   │    (the simulation world)             │  PANEL        │
│          │                                      │               │
│ World    │   ┌──────────────────────────┐        │  Properties   │
│ Models   │   │  Ground plane            │        │  of selected  │
│ Lights   │   │  Your robot here         │        │  object       │
│ Physics  │   │  Obstacles               │        │               │
│          │   └──────────────────────────┘        │               │
├──────────┴──────────────────────────────────────┴───────────────┤
│  BOTTOM: Time controls  [Play ▶] [Pause ⏸] [Step ⏭]  Real time │
└─────────────────────────────────────────────────────────────────┘
```

## Mouse controls

| Action | Mouse |
|---|---|
| **Rotate** view | Left click + drag |
| **Pan** (move sideways) | Scroll click + drag (middle button) |
| **Zoom** | Scroll wheel |
| **Select** object | Left click on object |
| **Move** object | Select + drag (with translate tool active) |

## Keyboard shortcuts

| Key | Action |
|---|---|
| `Ctrl+R` | Reset simulation time to 0 |
| `Ctrl+Z` | Undo |
| `Space` | Pause / Resume |
| `T` | Translate tool (move objects) |
| `R` | Rotate tool |
| `S` | Scale tool |
| `Esc` | Deselect |

## Left panel tabs

> - **World** — shows all objects in the scene (models, lights, plugins). Click any to see its properties.
> - **Models** — lists all inserted robot models.
> - **Insert** — browse and insert pre-built models from Gazebo's model library.
> - **Layers** — show/hide visual layers.

## Bottom time controls

> - **Real Time Factor (RTF)** — how fast simulation runs compared to real time. `RTF = 1.0` = same speed as reality. `RTF < 1.0` = simulation is slower than real time (too many physics calculations). Try to keep RTF close to 1.0.
> - **Step** — advance simulation by exactly one physics time step without playing.

---

# 7. Worlds — The Simulation Environment

A **world** is a `.world` or `.sdf` file describing everything in the simulation:
physics parameters, lighting, ground, obstacles, and pre-placed robots.

## Pre-installed worlds (Gazebo Classic)

```bash
ls /usr/share/gazebo-11/worlds/
```

> Lists all built-in worlds. `ls` = **l**i**s**t. `/usr/share/gazebo-11/worlds/` = the directory where Gazebo stores its built-in world files.

Common ones:

```bash
gazebo worlds/empty.world          # Empty world — just ground
gazebo worlds/willowgarage.world   # Indoor office environment
gazebo worlds/shapes.world         # Simple geometric shapes
gazebo worlds/robocup14_spl_field.world  # Soccer field
```

## Write your own world file

```xml
<!-- my_world.world -->
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="my_world">

    <!-- Physics engine settings -->
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <!-- 1000 Hz physics update rate -->
    </physics>

    <!-- Sunlight -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- A static box obstacle -->
    <model name="box_obstacle">
      <static>true</static>       <!-- does not move (no physics) -->
      <pose>2 0 0.5 0 0 0</pose> <!-- x y z roll pitch yaw -->
      <link name="link">
        <collision name="collision">
          <geometry><box><size>1 1 1</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>1 1 1</size></box></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

```bash
gazebo my_world.world
```

> - **SDF** = **S**imulation **D**escription **F**ormat. An XML-based format for describing worlds and models.
> - **XML** = e**X**tensible **M**arkup **L**anguage. A text format using `<tags>` to structure data.
> - `<pose>x y z roll pitch yaw</pose>` — position (metres) and orientation (radians) of an object.
>   - `x y z` = position in space. `z=0.5` = 0.5 metres above ground.
>   - `roll pitch yaw` = rotation around X, Y, Z axes in radians.
> - `<static>true</static>` — the object doesn't respond to physics (won't fall, won't be pushed). Good for walls and floors.
> - **ODE** = **O**pen **D**ynamics **E**ngine. The default physics engine used by Gazebo Classic.
> - `<collision>` — the invisible shape used for **physics calculations** (what objects collide with).
> - `<visual>` — the visible 3D shape rendered in the viewport. Can differ from collision shape.

---

# 8. Robots (Models) — Spawning into the World

## Use pre-built models from Gazebo's library

```bash
# In terminal — while Gazebo is running
gz model --spawn-file=/path/to/model.sdf --model-name=my_robot
```

Or from the Gazebo GUI: **Insert tab → search model name → click to place**.

## Download models from Gazebo's online library

Gazebo can auto-download models from `app.gazebosim.org`:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/.gazebo/models
```

> - `GAZEBO_MODEL_PATH` — environment variable listing directories where Gazebo looks for models.
> - `~/.gazebo/models` — the user's local model cache. Gazebo downloads models here automatically.
> - `$VAR:addition` — appends to an existing variable using `:` as separator (like `PATH`).

## Spawn a model via ROS2

```bash
# While Gazebo + ROS2 bridge are running
ros2 run gazebo_ros spawn_entity.py \
  -file /path/to/model.urdf \
  -entity my_robot \
  -x 0 -y 0 -z 0.1
```

> - `spawn_entity.py` — a ROS2 script provided by `gazebo_ros` that places a robot into a running Gazebo simulation.
> - `-file` — path to the robot description file (URDF or SDF).
> - `-entity` — the name to give this robot instance in Gazebo.
> - `-x -y -z` — spawn position in the world (metres).
> - **URDF** = **U**nified **R**obot **D**escription **F**ormat. An XML format for describing a robot's structure. Covered in section 10.

## Use TurtleBot3 (ready-to-use demo robot)

```bash
# Install TurtleBot3 packages
sudo apt install ros-humble-turtlebot3-gazebo -y

# Set the robot model
export TURTLEBOT3_MODEL=burger
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc

# Launch TurtleBot3 in an empty world
ros2 launch turtlebot3_gazebo empty_world.launch.py

# Or in a more complex maze world
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

> - `TURTLEBOT3_MODEL` — tells TurtleBot3 packages which model to simulate: `burger` (small, 2-wheel), `waffle` (larger), `waffle_pi` (with Raspberry Pi camera).
> - `turtlebot3_world` — a pre-built maze environment designed for testing navigation.

Control it with keyboard:

```bash
# In a new terminal
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard
```

> - `teleop` — short for **tele**operation: controlling a robot remotely (here, via keyboard).
> - Use `W/A/S/D` or arrow keys to drive. `Space` to stop.

---

# 9. Connecting Gazebo to ROS2

The **gazebo_ros_pkgs** bridge makes Gazebo appear as a set of ROS2 topics/services.

## Start Gazebo with ROS2 support

```bash
source /opt/ros/humble/setup.bash

# Method 1: Use the ROS2-aware Gazebo launcher
ros2 launch gazebo_ros gazebo.launch.py

# Method 2: Standard Gazebo (bridge auto-loads if sourced)
gazebo
```

> The key is to always `source` ROS2 **before** launching Gazebo. This loads the bridge plugins automatically.

## What topics Gazebo creates

Once Gazebo is running with a robot, check available topics:

```bash
ros2 topic list
```

You'll see topics like:

```
/clock                          ← simulation time
/cmd_vel                        ← velocity commands to the robot
/odom                           ← robot odometry (position estimate)
/scan                           ← LiDAR laser scan data
/camera/image_raw               ← camera image
/joint_states                   ← state of each robot joint (angle, velocity)
/tf                             ← coordinate transform tree
/gazebo/model_states            ← position of every model in the world
```

> - `/clock` — Gazebo publishes simulation time here. ROS2 nodes can use this to stay synchronized with the simulation instead of wall clock time.
> - `/odom` — **odom**etry: estimates the robot's position by integrating wheel encoder data. Accumulates error over time (drifts).
> - `/joint_states` — the angle and velocity of every motorized joint on the robot. Published by Gazebo's joint state plugin.
> - `/tf` — the **T**rans**F**orm tree: the geometric relationship between every coordinate frame (base_link → wheels, base_link → camera, map → odom → base_link).

## Control a simulated robot from ROS2

```bash
# Publish a velocity command manually (moves forward at 0.5 m/s)
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

> - `ros2 topic pub` — publishes a single message or streams messages to a topic from the command line.
> - The `{...}` syntax is **YAML inline format** for constructing a message.
> - This is the same `/cmd_vel` your Python/C++ node would publish to.

---

# 10. URDF & SDF — Describing Your Robot

Before Gazebo can simulate your robot, it needs a **description** of its shape, joints, mass, and sensors.

## URDF — Unified Robot Description Format

```xml
<!-- my_robot.urdf -->
<?xml version="1.0"?>
<robot name="my_robot">

  <!-- BASE LINK (the robot body) -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.1"/>   <!-- 30cm x 20cm x 10cm box -->
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>     <!-- r g b alpha (0-1 scale) -->
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>          <!-- kg -->
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0"
               izz="0.01"/>
    </inertial>
  </link>

  <!-- WHEEL LINK -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>  <!-- wheel shape -->
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0" ixz="0"
               iyy="0.001" iyz="0"
               izz="0.001"/>
    </inertial>
  </link>

  <!-- JOINT connecting base to wheel -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="-0.1 0.12 0" rpy="1.5707 0 0"/>  <!-- position + rotation -->
    <axis xyz="0 0 1"/>    <!-- rotation axis (spin around Z) -->
  </joint>

  <!-- GAZEBO PLUGIN: differential drive (makes the robot move) -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.24</wheel_separation>  <!-- distance between wheels (m) -->
      <wheel_diameter>0.1</wheel_diameter>
      <publish_odom>true</publish_odom>
      <ros>
        <remapping>cmd_vel:=/cmd_vel</remapping>
        <remapping>odom:=/odom</remapping>
      </ros>
    </plugin>
  </gazebo>

</robot>
```

> - **URDF** = **U**nified **R**obot **D**escription **F**ormat. XML format that describes robot links and joints.
> - `<link>` — a rigid body part of the robot (body, wheel, arm segment, camera mount).
> - `<joint>` — connects two links. Types:
>   - `continuous` — rotates freely (wheel).
>   - `revolute` — rotates within limits (elbow joint).
>   - `prismatic` — slides linearly (linear actuator).
>   - `fixed` — no movement (rigid connection like a mounted sensor).
> - `<inertial>` — the **mass** and **inertia tensor** of the link. Needed for realistic physics. Without it, Gazebo can't simulate correct forces.
> - **inertia tensor** — a 3×3 matrix describing how mass is distributed around each axis. Affects how the object rotates when forces are applied.
> - `rpy` = **R**oll **P**itch **Y**aw (rotation in radians). `1.5707 ≈ π/2 = 90°`.
> - `libgazebo_ros_diff_drive.so` — a **shared library** (`.so` = **s**hared **o**bject, Linux's equivalent of `.dll` on Windows) plugin that simulates differential drive locomotion.
> - **differential drive** — a robot with two independently driven wheels and no steering. Most simple wheeled robots use this.

## Convert URDF to SDF (for Gazebo)

```bash
gz sdf -p my_robot.urdf > my_robot.sdf
```

> `gz sdf -p` — converts a URDF file to SDF format. `-p` = **p**rint the output. `>` redirects output to a file.

## Use xacro to write cleaner URDF

**xacro** (**X**ML **macro**s) lets you use variables and macros in URDF to avoid repetition:

```xml
<!-- my_robot.urdf.xacro -->
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Define a variable -->
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_length" value="0.02"/>

  <!-- Define a reusable macro (like a function) -->
  <xacro:macro name="wheel_link" params="name">
    <link name="${name}">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_length}"/>
        </geometry>
      </visual>
    </link>
  </xacro:macro>

  <!-- Use the macro -->
  <xacro:wheel_link name="left_wheel"/>
  <xacro:wheel_link name="right_wheel"/>

</robot>
```

Convert xacro to URDF:

```bash
xacro my_robot.urdf.xacro > my_robot.urdf
```

> - `xacro` — an XML preprocessor for URDF. Like a templating language: define once, use many times.
> - `${variable}` — inserts the value of a xacro variable. Like f-strings in Python.
> - **macro** — a reusable code template. Here: define a wheel once, instantiate it twice with different names.

---

# 11. Sensors in Gazebo

Sensors are added as **Gazebo plugins** inside your URDF/SDF.
Each plugin makes Gazebo simulate a sensor and publish its data as a ROS2 topic.

## LiDAR (Laser Scanner)

```xml
<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar">
    <pose>0 0 0 0 0 0</pose>
    <always_on>true</always_on>
    <update_rate>10</update_rate>   <!-- Hz -->
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>      <!-- number of laser beams -->
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>   <!-- -180° in radians -->
          <max_angle>3.14159</max_angle>    <!-- +180° in radians -->
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>    <!-- minimum detection range (m) -->
        <max>10.0</max>   <!-- maximum detection range (m) -->
      </range>
    </ray>
    <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <remapping>~/out:=/scan</remapping>   <!-- publish to /scan -->
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
  </sensor>
</gazebo>
```

> - `<sensor type="ray">` — a ray sensor = LiDAR. Casts virtual laser beams and measures distance to first collision.
> - `<samples>360</samples>` — 360 laser beams = one per degree (full 360° scan).
> - `<update_rate>10</update_rate>` — publishes 10 scans per second.
> - `libgazebo_ros_ray_sensor.so` — the plugin that converts Gazebo's internal ray data to a ROS2 `LaserScan` message.
> - `~/out:=/scan` — `~` refers to the plugin's private namespace. This remaps it to the standard `/scan` topic.

## Camera

```xml
<gazebo reference="camera_link">
  <sensor type="camera" name="camera">
    <update_rate>30</update_rate>    <!-- 30 fps -->
    <camera name="camera">
      <horizontal_fov>1.3962634</horizontal_fov>  <!-- 80° in radians -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>      <!-- RGB, 8 bits per channel -->
      </image>
      <clip>
        <near>0.1</near>   <!-- don't render closer than 0.1m -->
        <far>100</far>     <!-- don't render further than 100m -->
      </clip>
    </camera>
    <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
      <ros>
        <remapping>image_raw:=/camera/image_raw</remapping>
        <remapping>camera_info:=/camera/camera_info</remapping>
      </ros>
    </plugin>
  </sensor>
</gazebo>
```

> - `<horizontal_fov>` — **F**ield **O**f **V**iew in radians. `1.3962634 rad ≈ 80°`. The angle the camera can see.
> - `R8G8B8` — RGB color format: **R**ed **G**reen **B**lue, 8 bits (0–255) per channel.
> - `640x480` — image resolution in pixels (**VGA** resolution). Higher = more detail but more data.
> - `/camera/camera_info` — metadata about the camera (focal length, distortion). Used by computer vision algorithms.
> - **fps** = **f**rames **p**er **s**econd. `update_rate=30` = 30 fps.

## IMU (Inertial Measurement Unit)

```xml
<gazebo reference="imu_link">
  <sensor type="imu" name="imu">
    <update_rate>100</update_rate>    <!-- 100 Hz -->
    <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <remapping>~/out:=/imu</remapping>
      </ros>
    </plugin>
  </sensor>
</gazebo>
```

> - `<sensor type="imu">` — simulates an IMU: measures linear acceleration (m/s²) and angular velocity (rad/s).
> - `update_rate=100` — IMUs typically run at high frequency (100–1000 Hz) for accurate motion tracking.
> - Publishes `sensor_msgs/Imu` messages on `/imu`.

---

# 12. Launch Gazebo from ROS2

## Full launch file — Gazebo + Robot + Controller

```python
# launch/simulation.launch.py

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_path      = get_package_share_directory('my_robot_pkg')
    urdf_file     = os.path.join(pkg_path, 'urdf', 'my_robot.urdf.xacro')
    world_file    = os.path.join(pkg_path, 'worlds', 'my_world.world')

    # ── 1. Convert xacro to URDF at launch time ───────────────────
    robot_description = Command(['xacro ', urdf_file])

    # ── 2. Launch Gazebo with our world ──────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': world_file}.items()
    )

    # ── 3. Publish the robot description to /robot_description ────
    robot_state_publisher = Node(
        package    = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters = [{'robot_description': robot_description}]
    )

    # ── 4. Spawn the robot into Gazebo ────────────────────────────
    spawn_robot = Node(
        package    = 'gazebo_ros',
        executable = 'spawn_entity.py',
        arguments  = [
            '-entity',           'my_robot',
            '-topic',            'robot_description',  # reads from the topic
            '-x', '0', '-y', '0', '-z', '0.1'         # spawn position
        ],
        output = 'screen'
    )

    # ── 5. Your controller node ───────────────────────────────────
    controller = Node(
        package    = 'my_robot_pkg',
        executable = 'controller_node',
        output     = 'screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        controller,
    ])
```

```bash
ros2 launch my_robot_pkg simulation.launch.py
```

> - `IncludeLaunchDescription` — includes another launch file inside yours. Like `#include` in C++ for launch files. Here we include the standard `gazebo.launch.py` from `gazebo_ros`.
> - `launch_arguments` — passes arguments to the included launch file (here, which world file to load).
> - `robot_state_publisher` — a standard ROS2 node that reads the URDF from `/robot_description` and publishes the TF tree. **Required** for RViz2 and most navigation nodes to work.
> - `Command(['xacro ', urdf_file])` — runs `xacro` as a subprocess at launch time and uses its output (the URDF XML) as the parameter value.
> - `-topic robot_description` — instead of reading from a file, the spawner reads the URDF from the `/robot_description` topic (published by `robot_state_publisher`).

---

# 13. Common Fixes & Troubleshooting

## Gazebo won't open / crashes immediately

```bash
# Check for error messages
gazebo --verbose

# Kill any stuck Gazebo processes
pkill -f gzserver
pkill -f gzclient
```

> - `--verbose` — the single most useful flag. Always use it when debugging.
> - `pkill -f pattern` — kills all processes whose **full command line** matches the pattern.
>   - `gzserver` — the **Gazebo server**: the physics engine process (runs headless, no GUI).
>   - `gzclient` — the **Gazebo client**: the GUI visualization process.
>   - Gazebo is split into two processes: server (physics) + client (display). They can be run separately.

## Black screen / no rendering (especially WSL2)

```bash
export LIBGL_ALWAYS_SOFTWARE=1    # Force CPU software rendering
gazebo --verbose
```

> Useful on WSL2 when GPU drivers aren't set up. Slower but works.

## "No namespace found" / ROS topics not appearing

```bash
# Make sure ROS2 is sourced BEFORE launching Gazebo
source /opt/ros/humble/setup.bash
gazebo
```

> If you launch Gazebo before sourcing ROS2, the bridge plugins won't load and no ROS2 topics will appear.

## Models not found / download fails

```bash
# Manually set the model path
export GAZEBO_MODEL_PATH=~/.gazebo/models:/usr/share/gazebo-11/models

# Download all Gazebo models manually (useful offline)
git clone https://github.com/osrf/gazebo_models.git ~/.gazebo/models
```

> - `GAZEBO_MODEL_PATH` — colon-separated list of directories. Gazebo searches them in order for model files.
> - `osrf/gazebo_models` — the official GitHub repository of all Gazebo pre-built models.

## Simulation running too slow (RTF < 1.0)

```bash
# Reduce physics update rate in your world file:
<real_time_update_rate>500</real_time_update_rate>  <!-- default 1000, try 500 -->

# Or reduce sensor update rates in your URDF:
<update_rate>5</update_rate>   <!-- reduce LiDAR from 10Hz to 5Hz -->
```

> The physics engine is the most CPU-intensive part. Reducing update rate trades accuracy for speed.

## Port conflict / multiple Gazebo instances

```bash
# Kill everything Gazebo-related
pkill gzserver && pkill gzclient

# Clear any leftover shared memory
rm -rf /tmp/gazebo*
```

> `/tmp/` — the Linux **temp**orary directory. Gazebo stores runtime files there. Stale files from crashed sessions can prevent Gazebo from restarting.

## WSL2 — "cannot connect to X server"

```bash
# Check if WSLg is running
echo $DISPLAY
ls /tmp/.X11-unix/

# Restart WSL from PowerShell (Windows)
wsl --shutdown
# Then reopen Ubuntu
```

> `/tmp/.X11-unix/` — directory containing **Unix domain sockets** for X11 display connections. WSLg creates these automatically. If the directory is empty, WSLg isn't running.

## RViz2 and Gazebo out of sync (TF errors)

```bash
# Make sure you're using simulation time
ros2 param set /your_node use_sim_time true
```

```python
# Or set it in your node's parameters:
Node(
    ...
    parameters=[{'use_sim_time': True}]
)
```

> - `use_sim_time` — when `True`, your node uses `/clock` from Gazebo instead of the system clock. **Critical**: if your node uses wall time but Gazebo publishes sim time, timestamps won't match and TF will throw errors.
> - **TF errors** — usually appear as "extrapolation into the past" or "frame does not exist" in the terminal. Almost always caused by time synchronization issues.

---

# 14. Useful Commands Cheat Sheet

## Gazebo CLI commands

```bash
# Launch
gazebo                                    # empty world
gazebo my_world.world                     # specific world
gazebo --verbose my_world.world           # with debug output
gazebo -s libgazebo_ros_init.so           # load a specific plugin
ros2 launch gazebo_ros gazebo.launch.py   # via ROS2 launcher

# Process management
pkill gzserver      # kill physics engine
pkill gzclient      # kill GUI
gazebo --version    # check version
```

## Gazebo Harmonic CLI commands

```bash
gz sim                          # empty world
gz sim shapes.sdf               # with a world
gz sim -v 4 shapes.sdf          # verbose level 4 (most detail)
gz model --list                 # list all models in running simulation
gz topic --list                 # list all Gazebo internal topics
gz topic --echo /topic_name     # print messages on a Gazebo topic
```

> - `-v 4` — verbosity level. 0 = silent, 4 = maximum debug output.
> - `gz topic` — Gazebo Harmonic has its **own** internal topic system (separate from ROS2 topics). The bridge connects the two.

## ROS2 commands useful with Gazebo

```bash
ros2 topic list                         # see all topics Gazebo is publishing
ros2 topic echo /scan                   # print LiDAR data
ros2 topic echo /odom                   # print robot position
ros2 topic echo /clock                  # print simulation time
ros2 topic hz /scan                     # measure LiDAR publish rate
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}}"  # drive forward

ros2 run robot_state_publisher robot_state_publisher  # publish TF tree
ros2 run rviz2 rviz2                                  # open 3D visualizer
ros2 run rqt_graph rqt_graph                          # node/topic graph
```

## Environment variables summary

```bash
# ROS2
export ROS_DOMAIN_ID=0              # isolate ROS2 network (0-232)

# Gazebo
export GAZEBO_MODEL_PATH=~/.gazebo/models     # where to find models
export GAZEBO_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/gazebo-11/plugins  # where to find plugins
export GAZEBO_RESOURCE_PATH=/usr/share/gazebo-11  # textures, meshes, worlds

# WSL2 display
export DISPLAY=:0                   # X11 display
export LIBGL_ALWAYS_SOFTWARE=1      # force CPU rendering (fallback)
export MESA_GL_VERSION_OVERRIDE=3.3 # fix OpenGL version detection
export GAZEBO_IP=127.0.0.1          # fix Gazebo networking in WSL2
```

> - `ROS_DOMAIN_ID` — isolates your ROS2 network from others on the same LAN. All nodes with the same Domain ID can communicate. Change it if you have multiple robots/users on the same network (0 is default).
> - `GAZEBO_PLUGIN_PATH` — where Gazebo looks for `.so` plugin files. Add custom plugin directories here.
> - **LAN** = **L**ocal **A**rea **N**etwork. The network your machine is connected to (home WiFi, lab Ethernet, etc.).

## Quick diagnosis checklist

```bash
# 1. Is ROS2 sourced?
echo $ROS_DISTRO                 # should print: humble

# 2. Is Gazebo installed?
gazebo --version

# 3. Is the bridge installed?
ros2 pkg list | grep gazebo      # should list gazebo_ros packages

# 4. Is display working? (WSL2)
echo $DISPLAY                    # should not be empty

# 5. Is OpenGL working?
glxinfo | grep renderer          # shows GPU or llvmpipe

# 6. Are Gazebo topics visible in ROS2?
gazebo &                         # launch Gazebo in background
sleep 3
ros2 topic list                  # should show /clock etc.
```

> - `echo $ROS_DISTRO` — prints the currently sourced ROS2 distribution name. Empty = not sourced.
> - `ros2 pkg list | grep gazebo` — `grep` filters lines containing "gazebo". If nothing appears, `gazebo_ros_pkgs` isn't installed.
> - `gazebo &` — the `&` runs the command **in the background**, returning the terminal prompt immediately.
> - `sleep 3` — waits 3 seconds (gives Gazebo time to start before checking topics).
