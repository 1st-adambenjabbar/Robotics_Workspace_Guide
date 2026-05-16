# 🤖 Gazebo — Complete Simulation & Code Guide
> How to **write code** that simulates, controls, and reads sensors in Gazebo
> Python (`rclpy`) and C++ (`rclcpp`) — every concept explained from scratch 🐚

---

# 📑 Table of Contents

1. [How Simulation Code Differs from Real Robot Code](#1-how-simulation-code-differs-from-real-robot-code)
2. [Simulation Time — The Most Important Concept](#2-simulation-time--the-most-important-concept)
3. [Reading Sensor Data from Gazebo](#3-reading-sensor-data-from-gazebo)
4. [Controlling a Simulated Robot](#4-controlling-a-simulated-robot)
5. [Odometry — Tracking Robot Position](#5-odometry--tracking-robot-position)
6. [TF — Coordinate Frames](#6-tf--coordinate-frames)
7. [Full Example — Obstacle Avoidance Robot](#7-full-example--obstacle-avoidance-robot)
8. [Full Example — Wall Follower](#8-full-example--wall-follower)
9. [Writing Gazebo Plugins (C++)](#9-writing-gazebo-plugins-c)
10. [Designing Worlds Programmatically](#10-designing-worlds-programmatically)
11. [Visualizing with RViz2 Alongside Gazebo](#11-visualizing-with-rviz2-alongside-gazebo)
12. [Testing Your Simulation Code](#12-testing-your-simulation-code)
13. [Complete Launch File — Full Simulation Stack](#13-complete-launch-file--full-simulation-stack)
14. [Cheat Sheet](#14-cheat-sheet)

---

# 1. How Simulation Code Differs from Real Robot Code

The biggest advantage of ROS2: **your robot code is the same** for simulation and real hardware.
But there are a few simulation-specific things to know:

```
Real robot:                           Gazebo simulation:
┌─────────────────────────────┐       ┌─────────────────────────────┐
│ /scan  ← real LiDAR driver  │       │ /scan  ← Gazebo ray plugin  │
│ /odom  ← real encoders      │       │ /odom  ← Gazebo diff plugin  │
│ /imu   ← real IMU chip      │       │ /imu   ← Gazebo IMU plugin   │
│ /cmd_vel → real motor driver│       │ /cmd_vel → Gazebo motor sim  │
│                             │       │                              │
│ Time = system clock         │       │ Time = /clock topic          │
└─────────────────────────────┘       └─────────────────────────────┘
         same ROS2 node code works for both ✅
```

**The 3 things you must do differently in simulation:**

| # | What | Why |
|---|---|---|
| 1 | Set `use_sim_time: True` | Use Gazebo clock, not system clock |
| 2 | Source ROS2 before Gazebo | So the bridge plugins load correctly |
| 3 | Match topic names exactly | Simulation topics must match your node's topics |

---

# 2. Simulation Time — The Most Important Concept

> **The #1 source of bugs in Gazebo simulation is time.**

In real life, time moves at 1 second per second.
In Gazebo, simulation can run **faster or slower** than real time.

- Gazebo publishes its simulation clock on the `/clock` topic.
- If your node uses **system time** but Gazebo uses **sim time**, timestamps won't match.
- This causes **TF errors**, missed callbacks, and wrong sensor timestamps.

## 🐍 Python — Always Set use_sim_time

```python
import rclpy
from rclpy.node import Node

class SimNode(Node):

    def __init__(self):
        super().__init__('sim_node')

        # ── CRITICAL: declare use_sim_time FIRST, before anything else ──
        self.declare_parameter('use_sim_time', True)

        # Now get the clock — it will use Gazebo time automatically
        self.get_logger().info('Node using simulation time')

        # All timers, timestamps, and Duration calculations
        # will now use Gazebo's /clock automatically
        self.create_timer(1.0, self.loop)

    def loop(self):
        # self.get_clock().now() returns SIMULATION time, not wall time
        now = self.get_clock().now()
        self.get_logger().info(f'Sim time: {now.to_msg().sec} s')


def main(args=None):
    rclpy.init(args=args)
    node = SimNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

> - `declare_parameter('use_sim_time', True)` — tells ROS2 to subscribe to `/clock` and use Gazebo's time instead of the system clock. **Must be declared before creating any timer or making any time-based call.**
> - `self.get_clock().now()` — returns the current time. With `use_sim_time=True`, this is Gazebo sim time.
> - `.to_msg().sec` — converts the time object to a ROS2 message and extracts the seconds.

## ⚙️ C++ — Always Set use_sim_time

```cpp
#include "rclcpp/rclcpp.hpp"

class SimNode : public rclcpp::Node
{
public:
    SimNode() : Node("sim_node")
    {
        // ── CRITICAL: set use_sim_time before any timer or clock call ──
        this->set_parameter(rclcpp::Parameter("use_sim_time", true));

        // All time calls now use Gazebo's /clock topic
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&SimNode::loop, this)
        );
    }

private:
    void loop()
    {
        auto now = this->get_clock()->now();
        RCLCPP_INFO(this->get_logger(), "Sim time: %ld s", now.seconds());
    }

    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimNode>());
    rclcpp::shutdown();
    return 0;
}
```

> - `this->set_parameter(rclcpp::Parameter("use_sim_time", true))` — C++ way to set a parameter programmatically. `rclcpp::Parameter` wraps a name+value pair.
> - `this->get_clock()->now()` — returns the current clock time (sim time if enabled).
> - `.seconds()` — returns the time as a `double` in seconds.

## Setting use_sim_time from launch file (recommended)

```python
# In your launch file — cleaner than setting it in code
Node(
    package    = 'my_robot_pkg',
    executable = 'my_node',
    parameters = [{'use_sim_time': True}]   # ← set here for every node
)
```

> This is the **cleanest approach**: set `use_sim_time` from the launch file so you don't need to modify code when switching between simulation and real hardware.

---

# 3. Reading Sensor Data from Gazebo

## 3.1 — LiDAR (LaserScan)

The most common sensor in robotics. Gazebo publishes it on `/scan`.

```
LaserScan message structure:
┌─────────────────────────────────────────┐
│ header.stamp     → timestamp            │
│ header.frame_id  → "lidar_link"         │
│ angle_min        → -3.14 rad (-180°)    │
│ angle_max        → +3.14 rad (+180°)    │
│ angle_increment  → step between beams   │
│ range_min        → 0.1 m (min valid)    │
│ range_max        → 10.0 m (max valid)   │
│ ranges[]         → [r0, r1, r2, ...]    │
│   ranges[0]   = distance at angle_min   │
│   ranges[180] = distance directly ahead │
│   ranges[359] = distance at angle_max   │
└─────────────────────────────────────────┘
```

### 🐍 Python — Reading LiDAR

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class LidarReaderNode(Node):

    def __init__(self):
        super().__init__('lidar_reader')
        self.declare_parameter('use_sim_time', True)

        self.create_subscription(LaserScan, '/scan', self.on_scan, 10)

        # Store the latest scan
        self.latest_scan = None

    def on_scan(self, msg: LaserScan):
        self.latest_scan = msg

        # ── Filter invalid readings ───────────────────────────────
        valid_ranges = [
            r for r in msg.ranges
            if msg.range_min < r < msg.range_max  # ignore inf and 0
            and not math.isnan(r)                  # ignore NaN values
            and not math.isinf(r)                  # ignore infinite values
        ]

        if not valid_ranges:
            return

        # ── Basic distance analysis ───────────────────────────────
        min_dist = min(valid_ranges)          # closest obstacle
        max_dist = max(valid_ranges)          # furthest point
        avg_dist = sum(valid_ranges) / len(valid_ranges)

        # ── Extract specific directions ───────────────────────────
        # ranges[] goes from angle_min to angle_max
        # For a 360° scan with 360 samples: index = angle in degrees
        num_readings = len(msg.ranges)

        # Front of robot (index at 0° if angle_min = 0, or middle if centered)
        front_idx  = 0                          # depends on your URDF orientation
        front_dist = msg.ranges[front_idx] if not math.isinf(msg.ranges[front_idx]) else 10.0

        # Left side (90° = quarter of the array)
        left_idx   = num_readings // 4
        left_dist  = msg.ranges[left_idx]  if not math.isinf(msg.ranges[left_idx])  else 10.0

        # Right side (270° = three-quarters)
        right_idx  = 3 * num_readings // 4
        right_dist = msg.ranges[right_idx] if not math.isinf(msg.ranges[right_idx]) else 10.0

        self.get_logger().info(
            f'Front: {front_dist:.2f}m | Left: {left_dist:.2f}m | Right: {right_dist:.2f}m'
        )

    def get_sector_min(self, ranges, start_deg, end_deg, total_deg=360):
        """Get minimum distance in a sector (arc of the scan)"""
        n = len(ranges)
        start_idx = int(start_deg / total_deg * n)
        end_idx   = int(end_deg   / total_deg * n)
        sector    = ranges[start_idx:end_idx]
        valid     = [r for r in sector if not math.isinf(r) and not math.isnan(r)]
        return min(valid) if valid else float('inf')
```

> - `math.isnan(r)` — **isnan** = **is** **N**ot **a** **N**umber. Gazebo sometimes returns `NaN` for beams that hit nothing. Always filter these.
> - `math.isinf(r)` — **isinf** = **is** **inf**inite. Beams beyond `range_max` return `inf`. Always filter these too.
> - `msg.range_min < r < msg.range_max` — valid range filter: discard readings outside sensor bounds.
> - `//` — Python **integer division** (floor division). `7 // 2 = 3` (no remainder). Used for array index calculation.
> - `float('inf')` — Python's positive infinity. Used as a safe default ("no obstacle detected").
> - **NaN** = **N**ot **a** **N**umber. A special floating-point value representing an undefined/invalid result.

---

### ⚙️ C++ — Reading LiDAR

```cpp
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <algorithm>   // std::min_element
#include <cmath>       // std::isnan, std::isinf
#include <limits>      // std::numeric_limits
#include <vector>      // std::vector

class LidarReaderNode : public rclcpp::Node
{
public:
    LidarReaderNode() : Node("lidar_reader")
    {
        this->set_parameter(rclcpp::Parameter("use_sim_time", true));

        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10,
            std::bind(&LidarReaderNode::on_scan, this, std::placeholders::_1)
        );
    }

private:
    void on_scan(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        const auto& r = msg->ranges;

        // ── Filter valid readings ─────────────────────────────────
        std::vector<float> valid;
        for (const float& v : r) {
            if (!std::isnan(v) && !std::isinf(v) &&
                v >= msg->range_min && v <= msg->range_max) {
                valid.push_back(v);
            }
        }

        if (valid.empty()) return;

        // ── Min/max/average ───────────────────────────────────────
        float min_dist = *std::min_element(valid.begin(), valid.end());
        float max_dist = *std::max_element(valid.begin(), valid.end());

        // ── Front / Left / Right sectors ─────────────────────────
        size_t n          = r.size();
        float  front_dist = safe_get(r, 0);
        float  left_dist  = safe_get(r, n / 4);
        float  right_dist = safe_get(r, 3 * n / 4);

        RCLCPP_INFO(this->get_logger(),
            "Front: %.2f | Left: %.2f | Right: %.2f | Min: %.2f",
            front_dist, left_dist, right_dist, min_dist);
    }

    // Helper: safely get a range value, returning infinity if invalid
    float safe_get(const std::vector<float>& ranges, size_t idx)
    {
        if (idx >= ranges.size()) return std::numeric_limits<float>::infinity();
        float v = ranges[idx];
        return (std::isnan(v) || std::isinf(v)) ?
               std::numeric_limits<float>::infinity() : v;
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
};
```

> - `const auto& r = msg->ranges` — `const` = won't modify. `&` = reference (no copy). `auto` = compiler deduces type (`std::vector<float>`).
> - `for (const float& v : r)` — **range-based for loop**: iterates over every element. `const float&` = read-only reference to each element.
> - `std::isnan(v)`, `std::isinf(v)` — C++ standard library functions for NaN/infinity checks. From `<cmath>`.
> - `std::vector<float> valid` — a **dynamic array** of floats. `std::vector` = the C++ equivalent of Python's list.
> - `.push_back(v)` — appends an element to the end of the vector.
> - `size_t` — an **unsigned integer** type used for sizes and indices. Cannot be negative. `size_t n = r.size()` = number of elements.

---

## 3.2 — Camera (Image)

```
Image message structure:
┌─────────────────────────────────────────┐
│ header.stamp     → timestamp            │
│ header.frame_id  → "camera_link"        │
│ width            → 640 (pixels)         │
│ height           → 480 (pixels)         │
│ encoding         → "rgb8" or "bgr8"     │
│ data[]           → raw pixel bytes      │
│   size = width × height × channels      │
│   = 640 × 480 × 3 = 921,600 bytes       │
└─────────────────────────────────────────┘
```

### 🐍 Python — Reading Camera with OpenCV

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge     # converts ROS2 images ↔ OpenCV images
import cv2                          # OpenCV: computer vision library
import numpy as np                  # NumPy: numerical arrays

class CameraNode(Node):

    def __init__(self):
        super().__init__('camera_node')
        self.declare_parameter('use_sim_time', True)

        # cv_bridge converts between ROS2 Image msg and OpenCV Mat
        self.bridge = CvBridge()

        self.create_subscription(Image, '/camera/image_raw', self.on_image, 10)

    def on_image(self, msg: Image):

        # ── Convert ROS2 Image → OpenCV array ────────────────────
        # 'bgr8' = Blue Green Red, 8 bits per channel (OpenCV default)
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # cv_image is now a NumPy array: shape = (height, width, 3)
        h, w, channels = cv_image.shape
        self.get_logger().info(f'Image: {w}x{h}, {channels} channels')

        # ── Basic image processing ────────────────────────────────

        # Convert to grayscale (1 channel, faster processing)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur (reduces noise)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges with Canny algorithm
        edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

        # ── Read a specific pixel ─────────────────────────────────
        # image[row, col] = image[y, x]  (note: row=y, col=x in NumPy)
        center_pixel = cv_image[h // 2, w // 2]   # center pixel
        b, g, r = center_pixel                      # unpack BGR channels
        self.get_logger().info(f'Center pixel: R={r} G={g} B={b}')

        # ── Display the image (only works with display/GUI) ───────
        cv2.imshow('Gazebo Camera', cv_image)
        cv2.imshow('Edges', edges)
        cv2.waitKey(1)    # 1ms wait — required for OpenCV to update window


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    cv2.destroyAllWindows()   # close all OpenCV windows on exit
    rclpy.shutdown()
```

Install required packages:

```bash
sudo apt install python3-opencv ros-humble-cv-bridge -y
pip install numpy --break-system-packages
```

> - **OpenCV** = **Open** **C**omputer **V**ision library. The standard library for image processing: reading, transforming, detecting features.
> - **CvBridge** — a ROS package that converts between `sensor_msgs/Image` (ROS2 format) and OpenCV's `numpy` array (Python format). Without it, you'd have to manually unpack the raw `msg.data` bytes.
> - `bgr8` — OpenCV uses **BGR** (**B**lue **G**reen **R**ed) channel order by default (historically). ROS2 uses `rgb8`. Always specify the encoding when converting.
> - **NumPy array** — a fast multi-dimensional array. An image is a 3D array: `[height, width, channels]`. `shape` returns its dimensions.
> - `cv2.Canny` — the **Canny edge detection** algorithm. Finds boundaries between regions of different brightness. Named after John F. Canny (1986).
> - `cv2.waitKey(1)` — gives OpenCV's event loop `1ms` to process window events. **Required** after `imshow` — without it, the window won't render.
> - `cv2.GaussianBlur` — smooths the image using a **Gaussian** kernel (a bell-curve weighted average). Removes noise before edge detection.

---

## 3.3 — IMU (Inertial Measurement Unit)

```
Imu message structure:
┌─────────────────────────────────────────────────┐
│ header.stamp                                    │
│ orientation         → Quaternion (x,y,z,w)      │
│ angular_velocity    → Vector3 (rad/s per axis)  │
│   .x = roll rate                                │
│   .y = pitch rate                               │
│   .z = yaw rate (turning speed)                 │
│ linear_acceleration → Vector3 (m/s² per axis)   │
│   .x = forward/backward acceleration            │
│   .y = sideways acceleration                    │
│   .z = vertical (gravity ≈ 9.81 m/s²)          │
└─────────────────────────────────────────────────┘
```

### 🐍 Python — Reading IMU

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import math

class ImuNode(Node):

    def __init__(self):
        super().__init__('imu_node')
        self.declare_parameter('use_sim_time', True)

        self.create_subscription(Imu, '/imu', self.on_imu, 10)

    def on_imu(self, msg: Imu):

        # ── Angular velocity (how fast robot is rotating) ─────────
        yaw_rate   = msg.angular_velocity.z    # rad/s — turning speed
        pitch_rate = msg.angular_velocity.y    # rad/s — tilting forward/back
        roll_rate  = msg.angular_velocity.x    # rad/s — tilting sideways

        # ── Linear acceleration (forces acting on robot) ──────────
        acc_x = msg.linear_acceleration.x     # forward/backward (m/s²)
        acc_y = msg.linear_acceleration.y     # sideways (m/s²)
        acc_z = msg.linear_acceleration.z     # vertical — includes gravity (m/s²)

        # ── Orientation from quaternion → Euler angles ────────────
        # Quaternion: (x, y, z, w) — 3D rotation representation
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w

        # Convert quaternion to yaw angle (rotation around vertical axis)
        # Formula for yaw from quaternion:
        yaw = math.atan2(2.0 * (qw * qz + qx * qy),
                         1.0 - 2.0 * (qy * qy + qz * qz))

        yaw_deg = math.degrees(yaw)   # convert radians to degrees

        self.get_logger().info(
            f'Yaw: {yaw_deg:.1f}° | Yaw rate: {yaw_rate:.3f} rad/s | '
            f'Acc X: {acc_x:.3f} m/s²'
        )
```

> - **Quaternion** (x, y, z, w) — a 4-number representation of 3D rotation. More stable than Euler angles (avoids **gimbal lock**: a singularity where two rotation axes align and you lose a degree of freedom).
> - **Euler angles** — (roll, pitch, yaw): three angles describing rotation. Intuitive but suffer from gimbal lock.
> - `math.atan2(y, x)` — the **2-argument arctangent**. Returns angle in radians. More robust than `atan(y/x)` because it handles all quadrants and division-by-zero.
> - `math.degrees()` — converts **radians → degrees**. `rad × (180/π) = degrees`.
> - **Yaw** — rotation around the vertical (Z) axis. In robotics: the heading/direction the robot faces. Most important orientation for ground robots.
> - **Roll** — rotation around the forward (X) axis. Tilting sideways.
> - **Pitch** — rotation around the lateral (Y) axis. Tilting forward/backward.

---

## 3.4 — GPS / NavSatFix

```python
from sensor_msgs.msg import NavSatFix

class GpsNode(Node):

    def __init__(self):
        super().__init__('gps_node')
        self.declare_parameter('use_sim_time', True)
        self.create_subscription(NavSatFix, '/gps/fix', self.on_gps, 10)

    def on_gps(self, msg: NavSatFix):
        lat = msg.latitude    # degrees (positive = North)
        lon = msg.longitude   # degrees (positive = East)
        alt = msg.altitude    # metres above sea level

        # Status: 0=no fix, 1=GPS fix, 2=SBAS fix, 3=GBAS fix
        status = msg.status.status

        self.get_logger().info(
            f'GPS: lat={lat:.6f}° lon={lon:.6f}° alt={alt:.1f}m status={status}'
        )
```

> - `NavSatFix` — **Nav**igation **Sat**ellite **Fix**. The standard ROS2 message for GPS data.
> - **latitude** — angle north/south of the equator (-90° to +90°).
> - **longitude** — angle east/west of the prime meridian (-180° to +180°).
> - **SBAS** = **S**atellite-**B**ased **A**ugmentation **S**ystem. Improves GPS accuracy using ground stations.
> - **GBAS** = **G**round-**B**ased **A**ugmentation **S**ystem. Even more precise, used near airports.

---

# 4. Controlling a Simulated Robot

## 4.1 — Differential Drive Robot (most common)

```
         left wheel           right wheel
              │                    │
   faster ─▶  │  ←─ both equal  ─▶ │  ← faster
   left turns right              left turns left
```

### 🐍 Python — Velocity Controller

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DriveController(Node):

    # ── Class constants ──────────────────────────────────────────
    MAX_LINEAR  = 0.5    # m/s — maximum forward speed
    MAX_ANGULAR = 1.0    # rad/s — maximum turning speed

    def __init__(self):
        super().__init__('drive_controller')
        self.declare_parameter('use_sim_time', True)

        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def move_forward(self, speed: float):
        """Move straight forward"""
        cmd = Twist()
        cmd.linear.x  = min(speed, self.MAX_LINEAR)   # clamp to max
        cmd.angular.z = 0.0
        self.vel_pub.publish(cmd)

    def turn(self, angular_speed: float):
        """Turn in place"""
        cmd = Twist()
        cmd.linear.x  = 0.0
        cmd.angular.z = angular_speed   # positive = left, negative = right
        self.vel_pub.publish(cmd)

    def move_arc(self, linear: float, angular: float):
        """Move in a curved arc (forward + turn simultaneously)"""
        cmd = Twist()
        cmd.linear.x  = linear
        cmd.angular.z = angular
        self.vel_pub.publish(cmd)

    def stop(self):
        """Stop all motion — ALWAYS send zero before exit"""
        self.vel_pub.publish(Twist())   # empty Twist = all zeros

    def move_for_duration(self, linear, angular, duration_sec):
        """Move for a fixed time, then stop — basic open-loop control"""
        start = self.get_clock().now()

        while rclpy.ok():
            elapsed = (self.get_clock().now() - start).nanoseconds / 1e9
            if elapsed >= duration_sec:
                break
            self.move_arc(linear, angular)
            rclpy.spin_once(self)   # process callbacks once without blocking

        self.stop()
```

> - `Twist()` — creating an empty `Twist` object initializes all fields to **zero**. So `self.vel_pub.publish(Twist())` publishes a stop command — all velocities zero.
> - `min(speed, self.MAX_LINEAR)` — **clamping**: ensures the value never exceeds the maximum. Prevents sending dangerous speeds to a real robot.
> - `angular.z` positive = **left turn** (counter-clockwise). Negative = **right turn** (clockwise). This follows the **right-hand rule**: fingers curl from X (forward) to Y (left), thumb points up (Z). Counter-clockwise rotation around Z = positive.
> - `rclpy.spin_once(self)` — processes **one callback** (or waits up to default timeout) without entering the blocking `rclpy.spin()` loop. Used when you need manual control of the spin cycle.
> - `(time - start).nanoseconds / 1e9` — converts nanoseconds to seconds. `1e9 = 1,000,000,000`. ROS2 internally stores time in **nanoseconds** for precision.
> - **open-loop control** — no feedback; just sends commands and hopes the robot does what you want. The opposite is **closed-loop** (checks the result and corrects).

---

### ⚙️ C++ — Velocity Controller

```cpp
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

class DriveController : public rclcpp::Node
{
public:
    static constexpr double MAX_LINEAR  = 0.5;    // m/s
    static constexpr double MAX_ANGULAR = 1.0;    // rad/s

    DriveController() : Node("drive_controller")
    {
        this->set_parameter(rclcpp::Parameter("use_sim_time", true));
        vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
    }

    void move_forward(double speed)
    {
        auto cmd = geometry_msgs::msg::Twist();
        cmd.linear.x  = std::min(speed, MAX_LINEAR);   // clamp
        cmd.angular.z = 0.0;
        vel_pub_->publish(cmd);
    }

    void turn(double angular_speed)
    {
        auto cmd = geometry_msgs::msg::Twist();
        cmd.linear.x  = 0.0;
        cmd.angular.z = angular_speed;
        vel_pub_->publish(cmd);
    }

    void move_arc(double linear, double angular)
    {
        auto cmd = geometry_msgs::msg::Twist();
        cmd.linear.x  = linear;
        cmd.angular.z = angular;
        vel_pub_->publish(cmd);
    }

    void stop()
    {
        vel_pub_->publish(geometry_msgs::msg::Twist());  // all zeros
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub_;
};
```

> - `std::min(speed, MAX_LINEAR)` — `std::min` from `<algorithm>`. Returns the smaller of two values. Used here to clamp speed.
> - `geometry_msgs::msg::Twist()` — default-constructs a `Twist` with all fields = 0.0. Publishing this stops the robot.

---

# 5. Odometry — Tracking Robot Position

**Odometry** estimates the robot's **position and velocity** by integrating wheel encoder data.

```
Odometry message structure:
┌─────────────────────────────────────────────────┐
│ header.frame_id    → "odom"                     │
│ child_frame_id     → "base_link"                │
│                                                 │
│ pose.pose.position.x  → x position (metres)    │
│ pose.pose.position.y  → y position (metres)    │
│ pose.pose.orientation → Quaternion (heading)   │
│                                                 │
│ twist.twist.linear.x  → forward speed (m/s)   │
│ twist.twist.angular.z → turning speed (rad/s) │
└─────────────────────────────────────────────────┘
```

### 🐍 Python — Reading Odometry

```python
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomNode(Node):

    def __init__(self):
        super().__init__('odom_reader')
        self.declare_parameter('use_sim_time', True)

        # Current pose
        self.x   = 0.0
        self.y   = 0.0
        self.yaw = 0.0    # heading in radians

        self.create_subscription(Odometry, '/odom', self.on_odom, 10)

    def on_odom(self, msg: Odometry):

        # ── Position ──────────────────────────────────────────────
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # ── Orientation: quaternion → yaw ─────────────────────────
        q = msg.pose.pose.orientation
        self.yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

        # ── Velocity ──────────────────────────────────────────────
        vx  = msg.twist.twist.linear.x    # forward speed m/s
        wz  = msg.twist.twist.angular.z   # angular speed rad/s

        self.get_logger().info(
            f'Pos: ({self.x:.2f}, {self.y:.2f}) | '
            f'Heading: {math.degrees(self.yaw):.1f}° | '
            f'Speed: {vx:.2f} m/s'
        )

    def distance_to(self, target_x: float, target_y: float) -> float:
        """Euclidean distance from current position to a target"""
        return math.sqrt((target_x - self.x)**2 + (target_y - self.y)**2)

    def angle_to(self, target_x: float, target_y: float) -> float:
        """Angle from current position+heading to a target point"""
        angle_to_target = math.atan2(target_y - self.y, target_x - self.x)
        angle_error = angle_to_target - self.yaw
        # Normalize to [-π, π] to avoid spinning the wrong way
        while angle_error >  math.pi: angle_error -= 2 * math.pi
        while angle_error < -math.pi: angle_error += 2 * math.pi
        return angle_error
```

> - **odometry** — from Greek: **odo** = path, **metry** = measurement. Estimates position by counting wheel rotations. Accumulates error over time (the robot thinks it's at X but it drifted to X+error).
> - `msg.pose.pose` — double `.pose` because `Odometry.pose` is a `PoseWithCovariance` (pose + uncertainty matrix), and `.pose` inside it is the actual `Pose`.
> - `msg.twist.twist` — same reason: `Odometry.twist` is `TwistWithCovariance`.
> - **covariance** — a matrix representing the uncertainty/error of the estimate. Higher values = less confident.
> - `math.atan2(y, x)` — computes the angle of a 2D vector. Returns values in `[-π, π]`.
> - **Euclidean distance** — straight-line distance: `√((x2-x1)² + (y2-y1)²)`. Named after Euclid.
> - **normalize to [-π, π]** — ensures the angle error is always the shortest path (never spins 350° when you could spin -10°).

---

# 6. TF — Coordinate Frames

**TF** (**T**rans**F**orm) tracks the geometric relationship between every part of your robot and the world.

```
World frame tree:
map
 └── odom               (odometry: drifts over time)
      └── base_link     (robot center)
           ├── laser_link    (LiDAR position relative to robot)
           ├── camera_link   (camera position)
           ├── imu_link      (IMU position)
           ├── left_wheel    (wheel positions)
           └── right_wheel
```

### 🐍 Python — Reading TF Transforms

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs   # needed for do_transform_point

class TfNode(Node):

    def __init__(self):
        super().__init__('tf_node')
        self.declare_parameter('use_sim_time', True)

        # Buffer stores recent transforms for a time window
        self.tf_buffer   = Buffer()
        # Listener subscribes to /tf and /tf_static and fills the buffer
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.create_timer(1.0, self.read_transform)

    def read_transform(self):
        try:
            # Get transform from 'odom' frame to 'base_link' frame
            # = where is base_link relative to odom?
            transform = self.tf_buffer.lookup_transform(
                'odom',          # target frame
                'base_link',     # source frame
                rclpy.time.Time()  # time=0 → get latest available
            )

            t = transform.transform.translation
            r = transform.transform.rotation

            self.get_logger().info(
                f'base_link in odom: x={t.x:.2f} y={t.y:.2f} z={t.z:.2f}'
            )

        except Exception as e:
            self.get_logger().warn(f'TF not available yet: {e}')

    def transform_point(self, point_x, point_y, from_frame, to_frame):
        """Convert a point from one coordinate frame to another"""
        try:
            pt = PointStamped()
            pt.header.frame_id = from_frame
            pt.point.x = point_x
            pt.point.y = point_y
            pt.point.z = 0.0

            # Transform the point
            transformed = self.tf_buffer.transform(pt, to_frame)
            return transformed.point.x, transformed.point.y

        except Exception as e:
            self.get_logger().error(f'Transform failed: {e}')
            return None, None
```

Install:
```bash
sudo apt install ros-humble-tf2-ros ros-humble-tf2-geometry-msgs -y
```

> - `Buffer` — stores a time-history of transforms (by default: 10 seconds). Needed because transforms arrive on `/tf` continuously and you want the one at a specific timestamp.
> - `TransformListener` — subscribes to `/tf` and `/tf_static` automatically and populates the Buffer.
> - `lookup_transform(target, source, time)` — answers: "where is `source` frame relative to `target` frame at this time?"
> - `/tf_static` — transforms that never change (e.g. camera mounted rigidly on the robot). Published once, unlike `/tf` which streams continuously.
> - `rclpy.time.Time()` — `Time()` with no arguments = time zero = "give me the latest available transform". If you pass a specific timestamp, it interpolates.
> - `try/except` — **exception handling**: `lookup_transform` raises an exception if the transform isn't available yet (e.g. at startup). Always wrap in try/except.

---

# 7. Full Example — Obstacle Avoidance Robot

A complete simulation node: reads LiDAR, decides to go forward or turn, publishes velocity.

### 🐍 Python

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class ObstacleAvoider(Node):
    """
    Simple reactive obstacle avoidance:
    - If front is clear  → move forward
    - If obstacle ahead  → turn toward the more open side
    - If very close      → back up first
    """

    # ── Tunable parameters ───────────────────────────────────────
    SAFE_DIST    = 0.5     # metres — stop if closer than this
    CAUTION_DIST = 1.0     # metres — slow down in this zone
    LINEAR_SPEED = 0.3     # m/s — forward speed
    ANGULAR_SPEED = 0.6    # rad/s — turning speed
    BACKUP_SPEED  = -0.1   # m/s — reverse speed

    def __init__(self):
        super().__init__('obstacle_avoider')
        self.declare_parameter('use_sim_time', True)

        # Publishers
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscribers
        self.create_subscription(LaserScan, '/scan', self.on_scan, 10)

        # State variables
        self.front_dist = float('inf')
        self.left_dist  = float('inf')
        self.right_dist = float('inf')

        # Control loop at 10 Hz
        self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Obstacle Avoider started.')

    def on_scan(self, msg: LaserScan):
        """Process LiDAR — extract front/left/right distances"""
        ranges = msg.ranges
        n      = len(ranges)

        def sector_min(start_pct, end_pct):
            """Get min distance in a sector defined by % of scan"""
            s = int(start_pct * n)
            e = int(end_pct   * n)
            vals = [r for r in ranges[s:e]
                    if not math.isnan(r) and not math.isinf(r)
                    and msg.range_min < r < msg.range_max]
            return min(vals) if vals else float('inf')

        # Split the 360° scan into sectors
        # Adjust indices based on your robot's URDF/LiDAR orientation
        self.front_dist = sector_min(0.90, 1.00)   # 324°–360° (front right)
        self.front_dist = min(self.front_dist,
                              sector_min(0.00, 0.10))  # 0°–36° (front left)
        self.left_dist  = sector_min(0.10, 0.40)   # 36°–144° (left)
        self.right_dist = sector_min(0.60, 0.90)   # 216°–324° (right)

    def control_loop(self):
        """Main decision logic — runs 10x per second"""
        cmd = Twist()

        if self.front_dist < self.SAFE_DIST:
            # ── Very close: back up ───────────────────────────────
            cmd.linear.x  = self.BACKUP_SPEED
            cmd.angular.z = self.ANGULAR_SPEED if self.left_dist > self.right_dist else -self.ANGULAR_SPEED
            self.get_logger().warn(f'TOO CLOSE! {self.front_dist:.2f}m — backing up')

        elif self.front_dist < self.CAUTION_DIST:
            # ── Obstacle ahead: turn toward open space ────────────
            if self.left_dist > self.right_dist:
                cmd.angular.z =  self.ANGULAR_SPEED   # turn left
            else:
                cmd.angular.z = -self.ANGULAR_SPEED   # turn right
            cmd.linear.x = 0.0
            self.get_logger().info(
                f'Obstacle {self.front_dist:.2f}m | '
                f'L:{self.left_dist:.2f} R:{self.right_dist:.2f}'
            )

        else:
            # ── Clear ahead: move forward ─────────────────────────
            cmd.linear.x  = self.LINEAR_SPEED
            cmd.angular.z = 0.0

        self.vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop() if hasattr(node, 'stop') else node.vel_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()
```

> - **reactive control** — makes decisions based only on the current sensor reading, with no memory or planning. Fast but not very smart.
> - `sector_min(start_pct, end_pct)` — a **nested function** (defined inside another function). In Python, inner functions can access outer variables (`ranges`, `n`, `msg`).
> - `try/except/finally` — `finally` block **always** runs, even if an exception occurs or `KeyboardInterrupt` (Ctrl+C) is pressed. Use it to ensure the robot stops safely.
> - `KeyboardInterrupt` — raised in Python when the user presses **Ctrl+C**. In ROS2, this is how you stop a running node from the terminal.
> - `hasattr(node, 'stop')` — checks if an object has a specific attribute or method. Defensive coding.

---

# 8. Full Example — Wall Follower

A robot that follows the right wall at a fixed distance.

### 🐍 Python

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class WallFollower(Node):
    """
    Right-wall following algorithm:
    - Keep the right wall at TARGET_DIST
    - Use a P controller to correct distance error
    - Avoid front obstacles
    """

    TARGET_DIST  = 0.4    # metres — desired wall distance
    MAX_LINEAR   = 0.2    # m/s
    MAX_ANGULAR  = 0.8    # rad/s
    KP           = 2.0    # proportional gain (P controller)
    FRONT_STOP   = 0.5    # metres — stop turning if front clear

    def __init__(self):
        super().__init__('wall_follower')
        self.declare_parameter('use_sim_time', True)

        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(LaserScan, '/scan', self.on_scan, 10)

        self.front_dist = float('inf')
        self.right_dist = float('inf')

        self.create_timer(0.05, self.control_loop)   # 20 Hz

    def on_scan(self, msg: LaserScan):
        n = len(msg.ranges)

        def safe_min(start, end):
            vals = [r for r in msg.ranges[start:end]
                    if not math.isnan(r) and not math.isinf(r)]
            return min(vals) if vals else float('inf')

        # Front sector: ±20° around forward direction
        front_w     = int(0.056 * n)         # 20° / 360° * n
        self.front_dist = safe_min(0, front_w)
        self.front_dist = min(self.front_dist, safe_min(n - front_w, n))

        # Right sector: 90° to the right
        right_center = int(0.75 * n)         # 270° index for right
        right_w      = int(0.083 * n)        # ±30° window
        self.right_dist = safe_min(
            max(0, right_center - right_w),
            min(n, right_center + right_w)
        )

    def control_loop(self):
        cmd = Twist()

        if self.front_dist < self.FRONT_STOP:
            # ── Front obstacle: turn left ─────────────────────────
            cmd.linear.x  = 0.0
            cmd.angular.z = self.MAX_ANGULAR

        else:
            # ── P controller for wall distance ────────────────────
            # error > 0 → too far from wall → turn right (negative z)
            # error < 0 → too close to wall → turn left (positive z)
            error = self.right_dist - self.TARGET_DIST

            correction    = -self.KP * error   # proportional correction
            correction    = max(-self.MAX_ANGULAR,
                                min(self.MAX_ANGULAR, correction))  # clamp

            cmd.linear.x  = self.MAX_LINEAR
            cmd.angular.z = correction

        self.vel_pub.publish(cmd)
        self.get_logger().info(
            f'Front:{self.front_dist:.2f} Right:{self.right_dist:.2f} '
            f'Correction:{cmd.angular.z:.3f}'
        )
```

> - **P controller** (Proportional controller) — the simplest feedback controller. `output = Kp × error`. The correction is **proportional** to how far you are from the target. The **gain** `Kp` controls how aggressively it corrects.
> - `KP = 2.0` — the **proportional gain**. Higher = more aggressive response but may oscillate. Lower = slower but smoother. Tuning this is called **PID tuning**.
> - `error = right_dist - TARGET_DIST` — positive error means too far from wall (wall on the right, robot drifted left). Negative = too close.
> - `correction = -Kp * error` — negative sign because: if too far (positive error), we want to turn right (negative angular.z). If too close (negative error), turn left (positive angular.z).
> - `max(-MAX, min(MAX, value))` — **clamping** pattern: ensures value stays within `[-MAX, +MAX]`.

---

# 9. Writing Gazebo Plugins (C++)

A **Gazebo plugin** is a C++ shared library (`.so` file) that extends Gazebo's behavior:
- Model plugins: control a model (e.g. apply forces, read joint states)
- World plugins: modify the world (e.g. spawn models, change gravity)
- Sensor plugins: publish custom sensor data

### Basic Model Plugin (Gazebo Classic)

```cpp
// src/my_plugin.cpp
#include <gazebo/gazebo.hh>              // Core Gazebo headers
#include <gazebo/physics/physics.hh>    // Physics engine access
#include <gazebo/common/common.hh>      // Utilities

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

namespace gazebo   // all Gazebo code lives in the gazebo namespace
{

class MyModelPlugin : public ModelPlugin   // inherit from ModelPlugin
{
public:

    MyModelPlugin() : ModelPlugin() {}

    // ── Called once when the model loads ─────────────────────────
    void Load(physics::ModelPtr model, sdf::ElementPtr sdf) override
    {
        this->model = model;

        // Initialize ROS2 if not already done
        if (!rclcpp::ok()) {
            rclcpp::init(0, nullptr);
        }

        // Create a ROS2 node for this plugin
        node_ = std::make_shared<rclcpp::Node>("my_plugin_node");

        // Subscribe to velocity commands
        cmd_sub_ = node_->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 10,
            std::bind(&MyModelPlugin::on_cmd, this, std::placeholders::_1)
        );

        // Connect to Gazebo's update loop (called every physics step)
        update_connection_ = event::Events::ConnectWorldUpdateBegin(
            std::bind(&MyModelPlugin::OnUpdate, this)
        );

        gzmsg << "MyModelPlugin loaded for model: "
              << model->GetName() << std::endl;
    }

    // ── Called every physics step (1000x per second by default) ──
    void OnUpdate()
    {
        rclcpp::spin_some(node_);   // process ROS2 callbacks

        // Apply velocity to the model
        // GetLink("base_link") → gets the link named "base_link"
        auto base = model->GetLink("base_link");
        if (base) {
            ignition::math::Vector3d linear_vel(cmd_linear_, 0, 0);
            ignition::math::Vector3d angular_vel(0, 0, cmd_angular_);
            base->SetLinearVel(linear_vel);
            base->SetAngularVel(angular_vel);
        }
    }

private:

    void on_cmd(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        cmd_linear_  = msg->linear.x;
        cmd_angular_ = msg->angular.z;
    }

    physics::ModelPtr                                              model;
    event::ConnectionPtr                                           update_connection_;
    std::shared_ptr<rclcpp::Node>                                  node_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr     cmd_sub_;

    double cmd_linear_  = 0.0;
    double cmd_angular_ = 0.0;
};

// ── Register plugin with Gazebo ───────────────────────────────────
GZ_REGISTER_MODEL_PLUGIN(MyModelPlugin)

}  // namespace gazebo
```

### CMakeLists.txt for a plugin

```cmake
find_package(gazebo REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

# Plugins are SHARED LIBRARIES (.so), not executables
add_library(my_plugin SHARED src/my_plugin.cpp)

target_include_directories(my_plugin PUBLIC ${GAZEBO_INCLUDE_DIRS})
target_link_libraries(my_plugin ${GAZEBO_LIBRARIES})
ament_target_dependencies(my_plugin rclcpp geometry_msgs)

install(TARGETS my_plugin
    LIBRARY DESTINATION lib   # .so files go in lib/
)
```

### Load the plugin in your URDF

```xml
<gazebo>
  <plugin name="my_plugin" filename="libmy_plugin.so"/>
</gazebo>
```

> - `ModelPlugin` — the base class for plugins that affect a single model. Other types: `WorldPlugin`, `SensorPlugin`, `SystemPlugin`.
> - `Load(model, sdf)` — called **once** when Gazebo loads the model. `model` = pointer to the model. `sdf` = the `<plugin>` XML element (you can read custom parameters from it).
> - `ConnectWorldUpdateBegin` — registers your `OnUpdate()` to be called at the **beginning of every physics step**. This is Gazebo's main loop hook.
> - `gzmsg` — Gazebo's logging stream (like `std::cout` but goes to Gazebo's console).
> - `rclcpp::spin_some(node_)` — processes pending ROS2 callbacks **without blocking**. Used in plugin update loops where blocking is not allowed.
> - `add_library(name SHARED ...)` — compiles as a **shared library** (`.so`), not an executable. Plugins are loaded at runtime by Gazebo, not run as standalone programs.
> - `GZ_REGISTER_MODEL_PLUGIN(ClassName)` — a Gazebo **macro** that registers your class so Gazebo knows how to load it from the `.so` file.
> - **override** — C++ keyword meaning "this method overrides a virtual method from the parent class". Good practice to be explicit.

---

# 10. Designing Worlds Programmatically

Instead of editing XML by hand, you can generate world files with Python.

### 🐍 Python — World Generator

```python
#!/usr/bin/env python3
"""
Generates a Gazebo world file with random obstacles.
Run: python3 generate_world.py > my_world.world
"""

import random
import math

def make_box(name, x, y, z, size_x, size_y, size_z, static=True):
    """Generate SDF XML for a box model"""
    return f"""
    <model name="{name}">
      <static>{"true" if static else "false"}</static>
      <pose>{x} {y} {z} 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box><size>{size_x} {size_y} {size_z}</size></box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box><size>{size_x} {size_y} {size_z}</size></box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
          </material>
        </visual>
      </link>
    </model>"""

def make_cylinder(name, x, y, radius=0.2, height=1.0):
    """Generate SDF XML for a cylinder obstacle"""
    return f"""
    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {height/2} 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder><radius>{radius}</radius><length>{height}</length></cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder><radius>{radius}</radius><length>{height}</length></cylinder>
          </geometry>
        </visual>
      </link>
    </model>"""

def generate_world(num_obstacles=10, world_size=10.0):
    """Generate a complete Gazebo world with random obstacles"""

    models = []

    # ── Boundary walls ────────────────────────────────────────────
    half = world_size / 2
    wall_thickness = 0.2
    wall_height    = 1.0

    models.append(make_box('wall_north', 0,     half,  wall_height/2,
                            world_size, wall_thickness, wall_height))
    models.append(make_box('wall_south', 0,    -half,  wall_height/2,
                            world_size, wall_thickness, wall_height))
    models.append(make_box('wall_east',  half,  0,     wall_height/2,
                            wall_thickness, world_size, wall_height))
    models.append(make_box('wall_west', -half,  0,     wall_height/2,
                            wall_thickness, world_size, wall_height))

    # ── Random obstacles ──────────────────────────────────────────
    random.seed(42)    # seed for reproducibility
    for i in range(num_obstacles):
        x = random.uniform(-half + 1, half - 1)
        y = random.uniform(-half + 1, half - 1)

        # Alternate between boxes and cylinders
        if i % 2 == 0:
            models.append(make_box(
                f'box_{i}', x, y, 0.5,
                random.uniform(0.3, 0.8),
                random.uniform(0.3, 0.8),
                1.0
            ))
        else:
            models.append(make_cylinder(f'cyl_{i}', x, y,
                                        random.uniform(0.1, 0.3)))

    # ── Assemble the world ────────────────────────────────────────
    world_xml = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="generated_world">

    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    {''.join(models)}

  </world>
</sdf>"""

    return world_xml


if __name__ == '__main__':
    world = generate_world(num_obstacles=15, world_size=8.0)
    print(world)
```

```bash
# Generate and save the world
python3 generate_world.py > my_generated_world.world

# Launch it
gazebo my_generated_world.world
```

> - `random.seed(42)` — sets the **random seed**: makes random numbers **reproducible**. Every time you run with seed `42`, you get the same world. Useful for repeatable experiments.
> - `random.uniform(a, b)` — returns a random float between `a` and `b`.
> - `f"""..."""` — Python **triple-quoted f-string**: a multiline string with variable interpolation.
> - `''.join(models)` — concatenates a list of strings into one, with no separator between them.
> - **reproducibility** — critical in robotics research: you want to be able to re-run an experiment and get identical conditions.

---

# 11. Visualizing with RViz2 Alongside Gazebo

RViz2 and Gazebo run **simultaneously**: Gazebo simulates, RViz2 visualizes the ROS2 data.

```bash
# Terminal 1: Gazebo
ros2 launch gazebo_ros gazebo.launch.py

# Terminal 2: RViz2
ros2 run rviz2 rviz2
```

### 🐍 Python — Publish Markers to RViz2

```python
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
import rclpy
from rclpy.node import Node

class VisualizationNode(Node):

    def __init__(self):
        super().__init__('viz_node')
        self.declare_parameter('use_sim_time', True)

        self.marker_pub = self.create_publisher(
            MarkerArray, '/visualization_marker_array', 10
        )
        self.create_timer(0.5, self.publish_markers)
        self.marker_id = 0

    def publish_markers(self):
        markers = MarkerArray()

        # ── Arrow marker (shows direction) ────────────────────────
        arrow = Marker()
        arrow.header.frame_id = 'map'
        arrow.header.stamp    = self.get_clock().now().to_msg()
        arrow.ns              = 'robot_markers'    # namespace for grouping
        arrow.id              = 0                  # unique ID within namespace
        arrow.type            = Marker.ARROW
        arrow.action          = Marker.ADD         # ADD or DELETE or DELETEALL
        arrow.pose.position.x = 1.0
        arrow.pose.position.y = 0.0
        arrow.pose.orientation.w = 1.0             # no rotation
        arrow.scale.x = 0.5    # shaft length
        arrow.scale.y = 0.05   # shaft diameter
        arrow.scale.z = 0.05   # head diameter
        arrow.color.r = 1.0    # red
        arrow.color.a = 1.0    # alpha (opacity): 1.0 = fully opaque

        # ── Sphere marker (shows a point) ─────────────────────────
        sphere = Marker()
        sphere.header.frame_id = 'map'
        sphere.header.stamp    = self.get_clock().now().to_msg()
        sphere.ns              = 'robot_markers'
        sphere.id              = 1
        sphere.type            = Marker.SPHERE
        sphere.action          = Marker.ADD
        sphere.pose.position.x = 2.0
        sphere.pose.position.y = 1.0
        sphere.pose.orientation.w = 1.0
        sphere.scale.x = sphere.scale.y = sphere.scale.z = 0.3  # radius
        sphere.color   = ColorRGBA(r=0.0, g=1.0, b=0.0, a=0.8)  # green

        # ── Text marker ───────────────────────────────────────────
        text = Marker()
        text.header.frame_id = 'map'
        text.header.stamp    = self.get_clock().now().to_msg()
        text.ns   = 'robot_markers'
        text.id   = 2
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD
        text.pose.position.x = 2.0
        text.pose.position.y = 1.0
        text.pose.position.z = 0.5
        text.pose.orientation.w = 1.0
        text.scale.z = 0.2       # text height
        text.color   = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)  # white
        text.text    = 'Target'

        markers.markers = [arrow, sphere, text]
        self.marker_pub.publish(markers)
```

> - **Marker** — a visual primitive published to RViz2. Not visible in Gazebo — only in RViz2.
> - `Marker.ARROW`, `Marker.SPHERE`, `Marker.CUBE`, `Marker.TEXT_VIEW_FACING` — the type of shape.
> - `Marker.ADD` — add or update this marker. `Marker.DELETE` — remove it. `Marker.DELETEALL` — remove all.
> - `ns` — **n**ame**s**pace: groups markers. Each (ns, id) pair is unique. Same pair = update existing marker.
> - `alpha` — **opacity**: `1.0` = fully visible, `0.0` = invisible. Use `0.5` for semi-transparent overlays.
> - `ColorRGBA` — Red Green Blue Alpha, each 0.0–1.0.
> - `TEXT_VIEW_FACING` — text that always faces the camera (billboarded). The most readable text type in RViz2.

---

# 12. Testing Your Simulation Code

## Unit testing a ROS2 node

```python
# test/test_obstacle_avoider.py
import unittest
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import time

class TestObstacleAvoider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        rclpy.init()
        cls.node = rclpy.create_node('test_node')

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        cls.node.destroy_node()
        rclpy.shutdown()

    def make_scan(self, front_dist, left_dist=5.0, right_dist=5.0):
        """Helper: create a fake LaserScan with specified distances"""
        msg = LaserScan()
        msg.angle_min      = -math.pi
        msg.angle_max      =  math.pi
        msg.angle_increment = 2 * math.pi / 360
        msg.range_min = 0.1
        msg.range_max = 10.0

        # 360 readings: fill with large distances
        msg.ranges = [5.0] * 360

        # Override specific directions
        msg.ranges[0]   = front_dist    # front
        msg.ranges[90]  = left_dist     # left
        msg.ranges[270] = right_dist    # right

        return msg

    def test_clear_path_moves_forward(self):
        """If no obstacles: robot should move forward"""
        scan = self.make_scan(front_dist=5.0)
        # Check your avoider logic returns positive linear.x
        # ... test your node's control_loop() output

    def test_obstacle_ahead_turns(self):
        """If obstacle ahead: robot should turn"""
        scan = self.make_scan(front_dist=0.3)
        # Check your avoider logic returns angular.z != 0

    def test_turns_toward_open_space(self):
        """With obstacle ahead: turn toward more open side"""
        # More open on left
        scan = self.make_scan(front_dist=0.3, left_dist=4.0, right_dist=1.0)
        # angular.z should be positive (turn left)
```

> - `unittest` — Python's built-in test framework. Organizes tests into classes and methods.
> - `setUpClass` / `tearDownClass` — run once before/after the **entire** test class. Used for expensive setup like initializing ROS2. (vs `setUp`/`tearDown` which run before/after **each** test).
> - `@classmethod` — a **decorator** meaning this method belongs to the class, not an instance. Called with `cls` instead of `self`.
> - **unit test** — tests a small, isolated piece of code. The goal is to test one behavior at a time.
> - `make_scan()` — a **test helper** (also called a **fixture**): creates fake data so you can test without a real Gazebo running.

Run tests:

```bash
cd ~/ros2_ws
colcon test --packages-select my_robot_pkg
colcon test-result --verbose
```

> - `colcon test` — runs all test files found in your package's `test/` folder.
> - `colcon test-result --verbose` — shows the detailed results (passed/failed/error per test).

---

# 13. Complete Launch File — Full Simulation Stack

```python
# launch/full_simulation.launch.py

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription,
    TimerAction, LogInfo
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg       = get_package_share_directory('my_robot_pkg')
    urdf_file = os.path.join(pkg, 'urdf',   'robot.urdf.xacro')
    world     = os.path.join(pkg, 'worlds', 'my_world.world')
    rviz_cfg  = os.path.join(pkg, 'rviz',   'robot.rviz')

    robot_description = Command(['xacro ', urdf_file])

    # ── Arguments ─────────────────────────────────────────────────
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='true')
    world_arg        = DeclareLaunchArgument('world', default_value=world)

    # ── 1. Gazebo ─────────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('gazebo_ros'),
            '/launch/gazebo.launch.py'
        ]),
        launch_arguments={
            'world':   LaunchConfiguration('world'),
            'verbose': 'false',
            'pause':   'false'    # false = start running immediately
        }.items()
    )

    # ── 2. Robot State Publisher (publishes TF from URDF) ─────────
    robot_state_publisher = Node(
        package    = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters = [
            {'robot_description': robot_description},
            {'use_sim_time':      True}
        ]
    )

    # ── 3. Spawn robot (wait 3s for Gazebo to finish loading) ─────
    spawn_robot = TimerAction(
        period = 3.0,    # seconds to wait
        actions = [
            Node(
                package    = 'gazebo_ros',
                executable = 'spawn_entity.py',
                arguments  = [
                    '-entity', 'my_robot',
                    '-topic',  'robot_description',
                    '-x', '0', '-y', '0', '-z', '0.05'
                ],
                output = 'screen'
            )
        ]
    )

    # ── 4. Your controller node ───────────────────────────────────
    controller = TimerAction(
        period = 5.0,    # wait for robot to spawn first
        actions = [
            Node(
                package    = 'my_robot_pkg',
                executable = 'obstacle_avoider',
                parameters = [{'use_sim_time': True}],
                output     = 'screen'
            )
        ]
    )

    # ── 5. RViz2 (optional visualization) ─────────────────────────
    rviz = Node(
        package    = 'rviz2',
        executable = 'rviz2',
        arguments  = ['-d', rviz_cfg],       # -d = load config file
        parameters = [{'use_sim_time': True}]
    )

    return LaunchDescription([
        use_sim_time_arg,
        world_arg,
        LogInfo(msg='[1/5] Starting Gazebo...'),
        gazebo,
        LogInfo(msg='[2/5] Starting Robot State Publisher...'),
        robot_state_publisher,
        LogInfo(msg='[3/5] Spawning robot in 3s...'),
        spawn_robot,
        LogInfo(msg='[4/5] Starting controller in 5s...'),
        controller,
        LogInfo(msg='[5/5] Starting RViz2...'),
        rviz,
    ])
```

> - `TimerAction(period, actions)` — delays launching the inner actions by `period` seconds. **Essential**: Gazebo needs time to start before you can spawn a robot, and the robot needs time to spawn before the controller starts.
> - `'pause': 'false'` — Gazebo starts **unpaused** (simulation running). Set to `'true'` if you want to inspect the world before physics start.
> - `'-d', rviz_cfg` — loads a pre-saved RViz2 configuration file. Without it, RViz2 starts blank and you'd have to manually add displays every time.
> - `LogInfo(msg=...)` — prints a message to the launch log. Useful to track which step the launch is at.

---

# 14. Cheat Sheet

## Simulation-specific patterns

```python
# ALWAYS at the start of __init__:
self.declare_parameter('use_sim_time', True)

# ALWAYS get sim-aware clock:
now = self.get_clock().now()

# ALWAYS filter LaserScan:
valid = [r for r in msg.ranges if not math.isnan(r) and not math.isinf(r)]

# ALWAYS stop robot on exit:
finally:
    self.vel_pub.publish(Twist())   # zero velocity

# ALWAYS wrap TF lookups:
try:
    tf = self.tf_buffer.lookup_transform(...)
except Exception as e:
    self.get_logger().warn(str(e))
```

## Key topics from Gazebo

| Topic | Message type | Direction | Content |
|---|---|---|---|
| `/clock` | `rosgraph_msgs/Clock` | Gazebo → ROS2 | Simulation time |
| `/scan` | `sensor_msgs/LaserScan` | Gazebo → ROS2 | LiDAR distances |
| `/camera/image_raw` | `sensor_msgs/Image` | Gazebo → ROS2 | Camera image |
| `/imu` | `sensor_msgs/Imu` | Gazebo → ROS2 | Acceleration + rotation |
| `/odom` | `nav_msgs/Odometry` | Gazebo → ROS2 | Robot position estimate |
| `/cmd_vel` | `geometry_msgs/Twist` | ROS2 → Gazebo | Velocity commands |
| `/joint_states` | `sensor_msgs/JointState` | Gazebo → ROS2 | Joint angles/velocities |
| `/tf` | `tf2_msgs/TFMessage` | Gazebo → ROS2 | Coordinate frame tree |

## Abbreviation glossary

| Abbreviation | Full form |
|---|---|
| `SDF` | Simulation Description Format |
| `URDF` | Unified Robot Description Format |
| `TF` | Transform |
| `RTF` | Real Time Factor |
| `ODE` | Open Dynamics Engine |
| `IMU` | Inertial Measurement Unit |
| `CV` | Computer Vision |
| `BGR` | Blue Green Red (OpenCV channel order) |
| `RGB` | Red Green Blue (standard channel order) |
| `NaN` | Not a Number |
| `PID` | Proportional Integral Derivative |
| `SLAM` | Simultaneous Localization And Mapping |
| `Nav2` | Navigation 2 (ROS2 nav stack) |
| `OSRF` | Open Source Robotics Foundation |
| `xacro` | XML Macros (URDF templating language) |
| `WSL` | Windows Subsystem for Linux |
| `RTK` | Real-Time Kinematics (precision GPS) |
