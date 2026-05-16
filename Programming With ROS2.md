## I explained the essentials . I let Claude choose the examples for you.
# 🤖 ROS2 — Complete Coding Guide
> Everything you need to program nodes in Python (`rclpy`) and C++ (`rclcpp`)
> Every concept, keyword, and abbreviation explained from scratch.

---

# 📑 Table of Contents

1. [How a ROS2 Program is Structured](#1-how-a-ros2-program-is-structured)
2. [OOP — Object Oriented Programming in ROS2](#2-oop--object-oriented-programming-in-ros2)
3. [Publishers — Sending Data](#3-publishers--sending-data)
4. [Subscribers — Receiving Data](#4-subscribers--receiving-data)
5. [Timers — Running Code Periodically](#5-timers--running-code-periodically)
6. [Message Types](#6-message-types)
7. [Services — Request / Response](#7-services--request--response)
8. [Actions — Long Running Tasks](#8-actions--long-running-tasks)
9. [Parameters — Configurable Values](#9-parameters--configurable-values)
10. [Launch Files — Starting Multiple Nodes](#10-launch-files--starting-multiple-nodes)
11. [Package Files — package.xml & CMakeLists.txt](#11-package-files--packagexml--cmakeliststxt)
12. [Custom Messages](#12-custom-messages)
13. [Logging & Debugging](#13-logging--debugging)
14. [Full Node Examples](#14-full-node-examples)
15. [Cheat Sheet](#15-cheat-sheet)

---

# 1. How a ROS2 Program is Structured

Before writing a single line of code, understand what files exist in a ROS2 package:

```
my_robot_pkg/
 ├── package.xml            ← Declares the package, its name, and dependencies
 ├── setup.py               ← (Python only) Entry points so ros2 run finds your node
 ├── setup.cfg              ← (Python only) Build config
 ├── CMakeLists.txt         ← (C++ only) Compilation instructions
 ├── launch/
 │   └── my_launch.py       ← Starts multiple nodes at once
 ├── msg/
 │   └── MyMessage.msg      ← Custom message definition (optional)
 ├── srv/
 │   └── MyService.srv      ← Custom service definition (optional)
 └── my_robot_pkg/          ← (Python) or src/ (C++) — your actual code
     ├── __init__.py        ← Makes the folder a Python module (can be empty)
     ├── publisher_node.py
     ├── subscriber_node.py
     └── robot_controller.py
```

> - `package.xml` — the **manifest**: every ROS2 package must have this. It tells colcon what the package is and what it depends on.
> - `setup.py` — specific to Python. Defines **entry points**: the mapping between `ros2 run` command names and your Python functions.
> - `CMakeLists.txt` — specific to C++. Tells CMake (**C**ross-platform **M**ake) how to **compile** your `.cpp` files into executables.
> - `launch/` — optional folder for launch files. Convention: always put launch files here.
> - `msg/` / `srv/` — optional folders for custom message/service definitions.
> - `__init__.py` — an empty file that Python requires to treat a folder as a **module** (importable package).

---

# 2. OOP — Object Oriented Programming in ROS2

## What is OOP and why ROS2 uses it

**OOP** = **O**bject **O**riented **P**rogramming.
The idea: group related **data** (attributes) and **behavior** (methods) together inside a **class**.

In ROS2, your node is a **class** that **inherits** from the base `Node` class.
**Inheritance** means your class automatically gets all the ROS2 powers (publish, subscribe, log, timer...) without writing them yourself.

```
        Node  (ROS2 base class — has all ROS2 powers)
          │
          │  inherits
          ▼
      YourNode  (your class — adds your robot logic on top)
```

---

## 🐍 Python — OOP Basics

```python
# A class is a blueprint
class MyRobotNode(Node):       # MyRobotNode inherits from Node
    
    def __init__(self):        # Constructor: runs when you create an instance
        super().__init__('my_robot_node')  # Call parent constructor FIRST
        
        # Attributes: variables that belong to this object
        self.speed     = 0.5   # float attribute
        self.counter   = 0     # integer attribute
        self.is_moving = False  # boolean attribute
    
    def move(self):            # Method: function that belongs to this object
        self.speed = 1.0
        self.is_moving = True
    
    def stop(self):
        self.speed = 0.0
        self.is_moving = False
```

> - `class MyRobotNode(Node)` — defines a class. `(Node)` = inherits from `Node`.
> - `def __init__(self)` — the **constructor**. The double underscores `__` indicate a **dunder** (double under) method — a special Python method. It runs automatically when you do `MyRobotNode()`.
> - `super().__init__('name')` — calls the **parent class** (`Node`) constructor. **Must be the first line** — without it, none of the ROS2 methods (`create_publisher`, `create_timer`, etc.) will work.
> - `self` — refers to **this specific instance** of the class. Every method must have `self` as its first parameter. Every attribute must be accessed as `self.attribute`.
> - **instance** — a concrete object created from a class. `node = MyRobotNode()` creates one instance.

---

## ⚙️ C++ — OOP Basics

```cpp
#include "rclcpp/rclcpp.hpp"

class MyRobotNode : public rclcpp::Node   // Inherit from rclcpp::Node
{
public:                                    // Public section: accessible from outside

    // Constructor
    MyRobotNode() : Node("my_robot_node") // Parent constructor called here
    {
        speed_     = 0.5;
        counter_   = 0;
        is_moving_ = false;
    }

    void move()        // Public method
    {
        speed_     = 1.0;
        is_moving_ = true;
    }

private:                                   // Private section: only inside this class

    void internal_logic() { }             // Private method

    // Attributes (member variables)
    double speed_;      // the trailing _ is a C++ naming convention for members
    int    counter_;
    bool   is_moving_;
};
```

> - `: public rclcpp::Node` — C++ inheritance syntax. `public` means all public members of `Node` are accessible. `rclcpp::Node` = class `Node` inside the `rclcpp` **namespace**. `::` = **scope resolution operator**.
> - `: Node("my_robot_node")` — **member initializer list**. Calls the parent constructor before your constructor body `{ }` runs.
> - `public:` — anything below this label is accessible from outside the class.
> - `private:` — anything below this label is only accessible from inside the class. Publishers, subscribers, timers, and attributes always go here. Callbacks go here too.
> - **namespace** — a named scope that groups related code to avoid name conflicts. Like folders for code. `rclcpp` is the namespace of the ROS2 C++ library.
> - **trailing `_`** — a common C++ convention: member variables end with `_` to distinguish them from local variables.

---

# 3. Publishers — Sending Data

A **publisher** sends messages on a topic continuously.
Think of it as a radio station broadcasting on a frequency.

## 🐍 Python Publisher

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        # Basic publisher
        self.str_pub = self.create_publisher(
            String,      # 1. Message type
            '/chatter',  # 2. Topic name (always starts with /)
            10           # 3. QoS depth (queue size)
        )

        # Publisher for robot velocity
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Timer to publish periodically
        self.timer = self.create_timer(0.5, self.publish_data)

    def publish_data(self):
        # ── Publish a String ──────────────────────────────
        msg = String()           # Create an empty message object
        msg.data = 'Hello!'      # Fill the field
        self.str_pub.publish(msg) # Send it

        # ── Publish a velocity command ────────────────────
        cmd = Twist()
        cmd.linear.x  = 0.5     # Move forward at 0.5 m/s
        cmd.angular.z = 0.1     # Rotate at 0.1 rad/s
        self.vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

> - `QoS` — **Q**uality **o**f **S**ervice. Controls how messages are delivered. The number `10` is the **history depth**: how many messages to keep in queue if the subscriber is too slow.
> - `msg.data` — `data` is a **field** of the `String` message. Every message type has different fields (defined in the `.msg` file).
> - `linear.x` — forward/backward speed in m/s (x axis). `angular.z` — rotation speed in rad/s around vertical axis.
> - **rad/s** — **rad**ians per **s**econd. Unit of angular speed. `π rad = 180°`.

---

## ⚙️ C++ Publisher

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"

class PublisherNode : public rclcpp::Node
{
public:
    PublisherNode() : Node("publisher_node")
    {
        str_pub_ = this->create_publisher<std_msgs::msg::String>("/chatter", 10);
        vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&PublisherNode::publish_data, this)
        );
    }

private:
    void publish_data()
    {
        // ── Publish a String ──────────────────────────────
        auto str_msg = std_msgs::msg::String();
        str_msg.data = "Hello!";
        str_pub_->publish(str_msg);

        // ── Publish a velocity command ────────────────────
        auto cmd = geometry_msgs::msg::Twist();
        cmd.linear.x  = 0.5;
        cmd.angular.z = 0.1;
        vel_pub_->publish(cmd);
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr         str_pub_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr     vel_pub_;
    rclcpp::TimerBase::SharedPtr                                timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PublisherNode>());
    rclcpp::shutdown();
    return 0;
}
```

> - `create_publisher<Type>(topic, qos)` — the `<Type>` is a **template parameter**: C++'s way of making code generic. The compiler generates a specific version for your type at compile time.
> - `auto` — C++ keyword that lets the **compiler deduce the type** automatically. Instead of writing `std_msgs::msg::String str_msg`, you write `auto str_msg`. Cleaner.
> - `->publish(msg)` — `->` accesses members of a **pointer**. Since publishers are `SharedPtr` (pointers), you use `->` instead of `.`.
> - `std::bind(&PublisherNode::publish_data, this)` — creates a callable from a member function. `&` = address of (pointer to the function). `this` = the current object instance.

---

# 4. Subscribers — Receiving Data

A **subscriber** receives messages from a topic.
Think of it as a radio receiver tuned to a frequency — it reacts every time something is broadcast.

## 🐍 Python Subscriber

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SubscriberNode(Node):

    def __init__(self):
        super().__init__('subscriber_node')

        # Subscribe to a string topic
        self.create_subscription(String,    '/chatter',  self.on_string,  10)

        # Subscribe to velocity commands
        self.create_subscription(Twist,     '/cmd_vel',  self.on_velocity, 10)

        # Subscribe to LiDAR data
        self.create_subscription(LaserScan, '/scan',     self.on_scan,    10)

    # ── Callbacks ─────────────────────────────────────────────────

    def on_string(self, msg: String):
        # msg.data contains the string
        self.get_logger().info(f'Received: {msg.data}')

    def on_velocity(self, msg: Twist):
        # Access nested fields
        speed    = msg.linear.x
        rotation = msg.angular.z
        self.get_logger().info(f'Speed: {speed}, Rotation: {rotation}')

    def on_scan(self, msg: LaserScan):
        # LaserScan has an array of distances
        min_dist = min(msg.ranges)    # closest obstacle
        self.get_logger().info(f'Closest obstacle: {min_dist:.2f} m')
```

> - `: String` — a Python **type hint**. It tells you (and your IDE) what type `msg` will be. ROS2 doesn't enforce it but it helps with autocompletion.
> - **callback** — a function you write that ROS2 calls **for you** whenever a message arrives. You never call it yourself — you only pass a reference to it.
> - `msg.ranges` — `LaserScan` contains a `ranges` field: a **list** of distance measurements (one per laser beam).
> - `:.2f` — Python f-string format: print a float with 2 decimal places.
> - **IDE** — **I**ntegrated **D**evelopment **E**nvironment (VS Code, PyCharm, CLion, etc.).

---

## ⚙️ C++ Subscriber

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

class SubscriberNode : public rclcpp::Node
{
public:
    SubscriberNode() : Node("subscriber_node")
    {
        str_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/chatter", 10,
            std::bind(&SubscriberNode::on_string, this, std::placeholders::_1)
        );

        vel_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 10,
            std::bind(&SubscriberNode::on_velocity, this, std::placeholders::_1)
        );

        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10,
            std::bind(&SubscriberNode::on_scan, this, std::placeholders::_1)
        );
    }

private:

    void on_string(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received: '%s'", msg->data.c_str());
    }

    void on_velocity(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        double speed    = msg->linear.x;
        double rotation = msg->angular.z;
        RCLCPP_INFO(this->get_logger(), "Speed: %.2f, Rotation: %.2f", speed, rotation);
    }

    void on_scan(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        // Find minimum in ranges vector
        auto min_it = std::min_element(msg->ranges.begin(), msg->ranges.end());
        float min_dist = *min_it;   // dereference the iterator to get the value
        RCLCPP_INFO(this->get_logger(), "Closest obstacle: %.2f m", min_dist);
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr         str_sub_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr     vel_sub_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr   scan_sub_;
};
```

> - `std::placeholders::_1` — a placeholder meaning "pass the first argument (the message) to the callback". Used with `std::bind` when the callback takes parameters.
> - `const ... ::SharedPtr msg` — `const` = promise not to modify the message. `::SharedPtr` = shared pointer. Using `const` is good practice for callbacks.
> - `msg->data.c_str()` — `->` accesses pointer members. `.c_str()` converts `std::string` to C-style `char*` (needed by `printf`-style format strings).
> - `std::min_element(begin, end)` — STL algorithm that returns an **iterator** (pointer-like) to the smallest element.
> - `*min_it` — the `*` **dereferences** the iterator: gets the actual value it points to.
> - **STL** — **S**tandard **T**emplate **L**ibrary. C++'s built-in collection of containers (`vector`, `map`) and algorithms (`sort`, `min_element`).

---

# 5. Timers — Running Code Periodically

A **timer** calls a function automatically at a fixed time interval.
Essential for control loops, publishing sensor data, or periodic status updates.

## 🐍 Python Timers

```python
class TimerNode(Node):

    def __init__(self):
        super().__init__('timer_node')

        # Timer at 10 Hz (every 100ms)
        self.timer_fast = self.create_timer(0.1,  self.fast_loop)

        # Timer at 1 Hz (every 1 second)
        self.timer_slow = self.create_timer(1.0,  self.slow_loop)

        # Timer at 0.5 Hz (every 2 seconds)
        self.timer_very_slow = self.create_timer(2.0, self.very_slow_loop)

        self.count = 0

    def fast_loop(self):
        """Control loop — runs 10 times per second"""
        pass  # put your robot control code here

    def slow_loop(self):
        """Status update — runs once per second"""
        self.count += 1
        self.get_logger().info(f'Alive: {self.count}s')

    def very_slow_loop(self):
        """Heartbeat — runs every 2 seconds"""
        self.get_logger().warn('Still running...')

    def pause_fast_timer(self):
        self.timer_fast.cancel()   # Pause the timer

    def resume_fast_timer(self):
        self.timer_fast.reset()    # Resume the timer

    def one_shot_example(self):
        """Timer that runs only once"""
        self.one_shot = self.create_timer(5.0, self.run_once)

    def run_once(self):
        self.get_logger().info('This ran only once!')
        self.one_shot.cancel()    # Cancel inside callback = one shot
```

> - `pass` — Python keyword meaning "do nothing". Used as a placeholder when a function body must exist syntactically but has no code yet.
> - `cancel()` — stops the timer without deleting it.
> - `reset()` — restarts the timer from zero.
> - **Hz** = **H**ert**z** — frequency unit. `10 Hz` = 10 times per second. Formula: `period = 1 / frequency`.

### Frequency reference table:

| `create_timer(period)` | Frequency | Typical use |
|---|---|---|
| `0.001` s | 1000 Hz | Very high speed control |
| `0.01` s | 100 Hz | IMU, motor PID control |
| `0.02` s | 50 Hz | Sensor fusion |
| `0.05` s | 20 Hz | LiDAR processing |
| `0.1` s | 10 Hz | Navigation commands |
| `0.5` s | 2 Hz | Status messages |
| `1.0` s | 1 Hz | Heartbeat, logs |

> - **PID** — **P**roportional **I**ntegral **D**erivative. A classic feedback control algorithm used in motor control.
> - **IMU** — **I**nertial **M**easurement **U**nit. Sensor measuring acceleration and rotation (gyroscope + accelerometer).

---

## ⚙️ C++ Timers

```cpp
class TimerNode : public rclcpp::Node
{
public:
    TimerNode() : Node("timer_node"), count_(0)
    {
        // 10 Hz timer
        timer_fast_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&TimerNode::fast_loop, this)
        );

        // 1 Hz timer
        timer_slow_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&TimerNode::slow_loop, this)
        );
    }

private:
    void fast_loop()
    {
        // Control loop — runs 10x/second
    }

    void slow_loop()
    {
        count_++;
        RCLCPP_INFO(this->get_logger(), "Alive: %d s", count_);

        // One-shot: cancel after first call
        // timer_slow_->cancel();
    }

    rclcpp::TimerBase::SharedPtr timer_fast_;
    rclcpp::TimerBase::SharedPtr timer_slow_;
    int count_;
};
```

> - `create_wall_timer` — **wall clock** timer (real time). Use `create_timer` with a clock if you want simulation time compatibility.
> - `std::chrono::milliseconds(100)` — `chrono` = C++ time library. `milliseconds`, `seconds`, `microseconds` are duration types.
> - `, count_(0)` in the initializer list — initializes `count_` to `0` in the same step as the parent constructor. More efficient than assigning in the body.

---

# 6. Message Types

Every topic has a **message type** — the data structure of what's being sent.
Like a contract between publisher and subscriber.

## Standard message packages

```python
# ── std_msgs — basic types ───────────────────────────────────────
from std_msgs.msg import String    # msg.data : str
from std_msgs.msg import Bool      # msg.data : bool
from std_msgs.msg import Int32     # msg.data : int
from std_msgs.msg import Int64     # msg.data : int (larger)
from std_msgs.msg import Float32   # msg.data : float
from std_msgs.msg import Float64   # msg.data : float (more precise)

# ── geometry_msgs — spatial data ─────────────────────────────────
from geometry_msgs.msg import Twist     # linear.x/y/z, angular.x/y/z
from geometry_msgs.msg import Pose      # position (Point) + orientation (Quaternion)
from geometry_msgs.msg import Point     # x, y, z
from geometry_msgs.msg import Vector3   # x, y, z (direction, no position)
from geometry_msgs.msg import Quaternion # x, y, z, w (rotation in 3D)
from geometry_msgs.msg import PoseStamped # Pose + Header (timestamp + frame)

# ── sensor_msgs — sensor data ────────────────────────────────────
from sensor_msgs.msg import LaserScan   # ranges[], angle_min, angle_max, etc.
from sensor_msgs.msg import Image       # data[], width, height, encoding
from sensor_msgs.msg import Imu         # orientation, angular_velocity, linear_acceleration
from sensor_msgs.msg import NavSatFix   # GPS: latitude, longitude, altitude
from sensor_msgs.msg import PointCloud2 # 3D point cloud (from depth camera/LiDAR)

# ── nav_msgs — navigation ────────────────────────────────────────
from nav_msgs.msg import Odometry       # pose + twist (position + velocity)
from nav_msgs.msg import OccupancyGrid  # 2D map (from SLAM)
from nav_msgs.msg import Path           # list of PoseStamped waypoints
```

> - **Quaternion** — a mathematical representation of 3D rotation using 4 numbers (x, y, z, w). Avoids **gimbal lock** (a problem with Euler angles). ROS2 uses quaternions for all orientations.
> - **Stamped** (e.g. `PoseStamped`) — a message that includes a `header` with a **timestamp** and **frame_id**. Important for time-synchronized data.
> - **frame_id** — the coordinate frame this data is expressed in (e.g. `"base_link"`, `"map"`, `"odom"`). Used by the **TF** system.
> - **TF** = **T**rans**F**orm. ROS2 system that tracks the geometric relationship between all coordinate frames in a robot.
> - **PointCloud2** — a 3D array of (x,y,z) points, produced by depth cameras or 3D LiDARs.
> - **OccupancyGrid** — the SLAM map. Each cell = probability (0-100) that the cell is occupied by an obstacle.

## How to inspect a message type

```bash
ros2 interface show std_msgs/msg/String
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show sensor_msgs/msg/LaserScan
```

> `ros2 interface show` — prints the full field definition of any message, service, or action type. Use this whenever you don't know what fields a message has.

---

# 7. Services — Request / Response

A **service** is a one-time request/response communication.
Unlike topics (continuous stream), a service call happens once and returns a result.

```
Client node                              Server node
    │                                        │
    │──── request (e.g. turn LED on) ────▶  │
    │                                        │  does the work
    │◀─── response (e.g. success=true) ───  │
    │                                        │
```

## 🐍 Python — Service Server (the one that handles requests)

```python
from rclpy.node import Node
from std_srvs.srv import SetBool   # A standard service: request=bool, response=bool+string

class ServiceServerNode(Node):

    def __init__(self):
        super().__init__('service_server')

        self.srv = self.create_service(
            SetBool,              # Service type
            '/enable_motor',      # Service name
            self.handle_request   # Callback
        )

    def handle_request(self, request, response):
        if request.data:           # request.data is the bool sent by client
            self.get_logger().info('Motor ENABLED')
            response.success = True
            response.message = 'Motor is now on'
        else:
            self.get_logger().info('Motor DISABLED')
            response.success = False
            response.message = 'Motor is now off'
        return response            # Must return the response object
```

## 🐍 Python — Service Client (the one that sends requests)

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ServiceClientNode(Node):

    def __init__(self):
        super().__init__('service_client')

        self.client = self.create_client(SetBool, '/enable_motor')

        # Wait until the server is available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for service...')

        # Send the request
        self.send_request(True)

    def send_request(self, enable: bool):
        request = SetBool.Request()
        request.data = enable

        # Call the service (async = non-blocking)
        future = self.client.call_async(request)

        # Add a callback for when the result arrives
        future.add_done_callback(self.on_response)

    def on_response(self, future):
        response = future.result()
        self.get_logger().info(f'Success: {response.success}, Msg: {response.message}')
```

> - `SetBool` — a standard service type from `std_srvs`. Request has `.data` (bool). Response has `.success` (bool) and `.message` (string).
> - **srv** — abbreviation for **service**.
> - `wait_for_service(timeout_sec)` — blocks until the server is up. `timeout_sec` = how long to wait before checking again.
> - `call_async(request)` — sends the request **asynchronously** (non-blocking). Returns a `future`.
> - **async / asynchronous** — the program continues running while waiting for the response, instead of freezing.
> - **future** — an object representing a result that isn't available yet. When the response arrives, the future is "resolved".
> - `add_done_callback` — registers a function to call when the future resolves.

---

## ⚙️ C++ Service Server

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/set_bool.hpp"

class ServiceServerNode : public rclcpp::Node
{
public:
    ServiceServerNode() : Node("service_server")
    {
        srv_ = this->create_service<std_srvs::srv::SetBool>(
            "/enable_motor",
            std::bind(&ServiceServerNode::handle_request, this,
                      std::placeholders::_1, std::placeholders::_2)
        );
    }

private:
    void handle_request(
        const std_srvs::srv::SetBool::Request::SharedPtr  request,
        const std_srvs::srv::SetBool::Response::SharedPtr response)
    {
        if (request->data) {
            response->success = true;
            response->message = "Motor is now on";
        } else {
            response->success = false;
            response->message = "Motor is now off";
        }
        RCLCPP_INFO(this->get_logger(), "Request handled: %s", response->message.c_str());
    }

    rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr srv_;
};
```

> - `std::placeholders::_1, std::placeholders::_2` — two placeholders because the service callback takes **two arguments** (request AND response), unlike subscriber callbacks (one argument).

---

# 8. Actions — Long Running Tasks

An **action** is like a service but for tasks that take time.
It supports: **goal** (what to do), **feedback** (progress updates), and **result** (final outcome).

```
Client                              Server
  │─── send goal (navigate to X,Y) ──▶ │
  │                                     │  working...
  │◀── feedback (20% done) ────────── │
  │◀── feedback (60% done) ────────── │
  │◀── feedback (90% done) ────────── │
  │◀── result (success=true) ───────── │
  │
  │  (client can also cancel mid-way)
```

## 🐍 Python — Action Client

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose  # Nav2 navigation action
from geometry_msgs.msg import PoseStamped

class NavigationClient(Node):

    def __init__(self):
        super().__init__('navigation_client')

        self.action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.action_client.wait_for_server()

        self.send_goal(1.0, 2.0)   # Navigate to x=1.0, y=2.0

    def send_goal(self, x, y):
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = 'map'
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y

        future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.on_feedback
        )
        future.add_done_callback(self.on_goal_accepted)

    def on_feedback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback received')

    def on_goal_accepted(self, future):
        goal_handle = future.result()
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_result)

    def on_result(self, future):
        result = future.result().result
        self.get_logger().info('Navigation complete!')
```

> - `ActionClient(self, Type, name)` — creates an action client. Unlike services (where you use `self.create_client`), actions use a separate `ActionClient` class from `rclpy.action`.
> - `wait_for_server()` — blocks until the action server is ready.
> - `send_goal_async` — sends the goal without blocking. Returns a future.
> - **goal_handle** — a handle to the ongoing action. You can call `goal_handle.cancel_goal_async()` to cancel.
> - `header.frame_id = 'map'` — tells ROS2 the goal position is expressed in the `'map'` coordinate frame.

---

# 9. Parameters — Configurable Values

**Parameters** let you configure your node from outside (command line, launch file, YAML file) without recompiling or editing code.

## 🐍 Python Parameters

```python
class ParameterNode(Node):

    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('speed',       0.5)       # float
        self.declare_parameter('robot_name', 'default')  # string
        self.declare_parameter('debug_mode',  False)     # bool
        self.declare_parameter('max_range',   5.0)       # float

        # Read parameter values
        self.speed       = self.get_parameter('speed').value
        self.robot_name  = self.get_parameter('robot_name').value
        self.debug_mode  = self.get_parameter('debug_mode').value

        self.get_logger().info(f'Robot: {self.robot_name}, Speed: {self.speed}')

        # Listen for parameter changes at runtime
        self.add_on_set_parameters_callback(self.on_param_change)

    def on_param_change(self, params):
        from rcl_interfaces.msg import SetParametersResult
        for p in params:
            if p.name == 'speed':
                self.speed = p.value
                self.get_logger().info(f'Speed updated to: {self.speed}')
        return SetParametersResult(successful=True)
```

```bash
# Override parameters from command line
ros2 run my_pkg my_node --ros-args -p speed:=1.0 -p robot_name:=r2d2

# Or from a YAML file
ros2 run my_pkg my_node --ros-args --params-file config.yaml
```

```yaml
# config.yaml
parameter_node:
  ros__parameters:
    speed: 1.0
    robot_name: r2d2
    debug_mode: true
```

> - `declare_parameter(name, default)` — **must be called first** before reading. Registers the parameter with a default value. If you try to `get_parameter` without declaring first, it throws an error.
> - `.value` — the actual value stored in the parameter object.
> - **YAML** — **Y**et **A**nother **M**arkup **L**anguage. A human-readable format for configuration files. Indentation matters (like Python).
> - `-p name:=value` — syntax to pass a parameter from the command line. `:=` is the ROS2 parameter assignment operator.
> - **runtime** — while the program is running (as opposed to compile time or startup time).

---

## ⚙️ C++ Parameters

```cpp
class ParameterNode : public rclcpp::Node
{
public:
    ParameterNode() : Node("parameter_node")
    {
        // Declare parameters
        this->declare_parameter("speed",       0.5);
        this->declare_parameter("robot_name", std::string("default"));
        this->declare_parameter("debug_mode",  false);

        // Read parameters
        speed_      = this->get_parameter("speed").as_double();
        robot_name_ = this->get_parameter("robot_name").as_string();
        debug_mode_ = this->get_parameter("debug_mode").as_bool();

        RCLCPP_INFO(this->get_logger(), "Robot: %s, Speed: %.2f",
                    robot_name_.c_str(), speed_);
    }

private:
    double      speed_;
    std::string robot_name_;
    bool        debug_mode_;
};
```

> - `.as_double()`, `.as_string()`, `.as_bool()` — type-specific getters. Unlike Python's `.value`, C++ needs explicit type conversion.
> - `std::string("default")` — wrapping in `std::string()` is needed so C++ doesn't confuse it with a `char*`.

---

# 10. Launch Files — Starting Multiple Nodes

A **launch file** starts multiple nodes at once, passes parameters, and sets up the whole system.
Without launch files, you'd need a separate terminal for every node.

## 🐍 Python Launch File

```python
# launch/my_robot_launch.py

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # ── Declare arguments (can be overridden from CLI) ────────────
    speed_arg = DeclareLaunchArgument(
        'speed',
        default_value='0.5',
        description='Robot speed in m/s'
    )

    # ── Get package path (for config files) ──────────────────────
    pkg_path   = get_package_share_directory('my_robot_pkg')
    config_file = os.path.join(pkg_path, 'config', 'params.yaml')

    # ── Define nodes ─────────────────────────────────────────────
    controller_node = Node(
        package    = 'my_robot_pkg',
        executable = 'controller_node',
        name       = 'controller',
        output     = 'screen',
        parameters = [
            config_file,                              # from YAML
            {'speed': LaunchConfiguration('speed')}  # from argument
        ],
        remappings = [
            ('/cmd_vel', '/robot/cmd_vel')            # rename a topic
        ]
    )

    camera_node = Node(
        package    = 'my_robot_pkg',
        executable = 'camera_node',
        name       = 'camera',
        output     = 'screen'
    )

    lidar_node = Node(
        package    = 'my_robot_pkg',
        executable = 'lidar_node',
        name       = 'lidar',
        output     = 'log'   # logs to file instead of screen
    )

    return LaunchDescription([
        speed_arg,
        LogInfo(msg='Launching robot system...'),
        controller_node,
        camera_node,
        lidar_node,
    ])
```

```bash
# Launch with defaults
ros2 launch my_robot_pkg my_robot_launch.py

# Override an argument
ros2 launch my_robot_pkg my_robot_launch.py speed:=1.0
```

> - `generate_launch_description()` — the function ROS2 looks for in your launch file. Must be named exactly this.
> - `LaunchDescription([...])` — holds all the actions to execute.
> - `DeclareLaunchArgument` — declares a CLI argument that users can pass when calling `ros2 launch`.
> - `LaunchConfiguration('speed')` — reads the value of the `speed` argument at launch time.
> - `remappings` — changes a topic name at runtime without editing code. `('/cmd_vel', '/robot/cmd_vel')` means "any reference to `/cmd_vel` in this node becomes `/robot/cmd_vel`".
> - `get_package_share_directory` — finds the installed path of a package (where YAML configs, meshes, etc. are stored after `colcon build`).
> - `output='screen'` — prints logs to terminal. `output='log'` — writes to a file in `~/.ros/log/`.

---

# 11. Package Files — package.xml & CMakeLists.txt

## `package.xml` — for both Python and C++

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_robot_pkg</name>           <!-- Package name (must match folder name) -->
  <version>0.1.0</version>
  <description>My robot controller</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>MIT</license>

  <!-- Build tool -->
  <buildtool_depend>ament_python</buildtool_depend>   <!-- for Python -->
  <!-- OR -->
  <buildtool_depend>ament_cmake</buildtool_depend>    <!-- for C++ -->

  <!-- Runtime dependencies (what your code imports/includes) -->
  <depend>rclpy</depend>              <!-- Python ROS2 lib -->
  <depend>rclcpp</depend>             <!-- C++ ROS2 lib -->
  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>std_srvs</depend>

  <export>
    <build_type>ament_python</build_type>  <!-- or ament_cmake -->
  </export>
</package>
```

> - `<depend>` — declares a dependency. colcon and rosdep use this to know what to install/build first.
> - `<buildtool_depend>` — a tool needed only at **build time**, not at runtime.
> - `format="3"` — the package.xml format version. Always use 3 for ROS2.

---

## `setup.py` — Python only

```python
from setuptools import setup
import os
from glob import glob

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # Install config files
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            # 'command_name = package.module:function'
            'controller  = my_robot_pkg.controller_node:main',
            'camera_node = my_robot_pkg.camera_node:main',
            'lidar_node  = my_robot_pkg.lidar_node:main',
        ],
    },
)
```

> - `entry_points` — **the most important part**. Maps `ros2 run my_robot_pkg controller` to the `main()` function in `my_robot_pkg/controller_node.py`. Without this, `ros2 run` won't find your node.
> - `data_files` — tells colcon to copy extra files (launch, config, YAML) into the install directory. If you don't do this, your launch files won't be found at runtime.
> - `glob('launch/*.py')` — `glob` finds all files matching a pattern. Here: all `.py` files in the `launch/` folder.

---

## `CMakeLists.txt` — C++ only

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_pkg)              # Must match package.xml name

# ── Find dependencies ────────────────────────────────────────────
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# ── Build executables ────────────────────────────────────────────
add_executable(controller_node src/controller_node.cpp)
ament_target_dependencies(controller_node
    rclcpp std_msgs geometry_msgs sensor_msgs
)

add_executable(camera_node src/camera_node.cpp)
ament_target_dependencies(camera_node rclcpp sensor_msgs)

# ── Install executables ──────────────────────────────────────────
install(TARGETS
    controller_node
    camera_node
    DESTINATION lib/${PROJECT_NAME}    # where ros2 run looks for them
)

# ── Install launch and config files ──────────────────────────────
install(DIRECTORY launch config
    DESTINATION share/${PROJECT_NAME}
)

ament_package()    # MUST be the last line
```

> - `cmake_minimum_required` — the minimum CMake version needed. `3.8` is safe for ROS2 Humble.
> - `project(name)` — sets the project name. Must match `package.xml`.
> - `find_package(X REQUIRED)` — tells CMake to locate library `X`. `REQUIRED` = fail if not found.
> - `add_executable(name src/file.cpp)` — defines a binary to compile from a source file.
> - `ament_target_dependencies(target libs...)` — links your executable against ROS2 libraries. Handles include paths and linker flags automatically.
> - `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` — copies compiled binaries so `ros2 run` can find them. `${PROJECT_NAME}` = the `project()` name above.
> - `ament_package()` — **must be the last line**. Registers the package with ament.

---

# 12. Custom Messages

Sometimes the standard messages don't have the exact fields you need.
You can define your own message types.

## Create a custom message

```
my_robot_pkg/
 └── msg/
     └── RobotStatus.msg    ← your message definition
```

```
# RobotStatus.msg
string robot_name       # name of the robot
float64 battery_level   # battery percentage 0-100
bool is_moving          # is the robot currently moving
int32 error_code        # 0 = no error
geometry_msgs/Pose pose # current position (import another message type)
```

> - Message files use a simple format: `type field_name` on each line.
> - Lines starting with `#` are **comments**.
> - You can **embed other message types** (like `geometry_msgs/Pose`) inside yours.

## Add to `package.xml`:

```xml
<depend>geometry_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

## Add to `CMakeLists.txt` (C++):

```cmake
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
    "msg/RobotStatus.msg"
    DEPENDENCIES geometry_msgs
)
```

## Use the custom message:

```python
# Python
from my_robot_pkg.msg import RobotStatus

msg = RobotStatus()
msg.robot_name    = 'R2D2'
msg.battery_level = 85.0
msg.is_moving     = True
msg.error_code    = 0
```

```cpp
// C++
#include "my_robot_pkg/msg/robot_status.hpp"  // snake_case for file, CamelCase for class

auto msg = my_robot_pkg::msg::RobotStatus();
msg.robot_name    = "R2D2";
msg.battery_level = 85.0;
msg.is_moving     = true;
msg.error_code    = 0;
```

> - **rosidl** — **ROS** **I**nterface **D**efinition **L**anguage. The system that converts `.msg`/`.srv` files into Python and C++ code at build time.
> - In C++, the include path uses `snake_case` (e.g. `robot_status.hpp`), but the class is in `CamelCase` (`RobotStatus`). This is automatic — colcon generates both.

---

# 13. Logging & Debugging

## 🐍 Python Logging

```python
# Severity levels (from lowest to highest)
self.get_logger().debug('Detailed debug info (hidden by default)')
self.get_logger().info('Normal information')
self.get_logger().warn('Something unexpected but not fatal')
self.get_logger().error('Something went wrong')
self.get_logger().fatal('Critical failure — node may stop')

# With variables
speed = 1.5
self.get_logger().info(f'Current speed: {speed:.2f} m/s')

# Log only once (useful inside callbacks to avoid spam)
self.get_logger().info('This prints every call')
# Use a counter or flag to throttle if needed
```

## ⚙️ C++ Logging

```cpp
RCLCPP_DEBUG(this->get_logger(), "Debug: value = %d", value);
RCLCPP_INFO(this->get_logger(),  "Info: speed = %.2f", speed);
RCLCPP_WARN(this->get_logger(),  "Warning: battery low!");
RCLCPP_ERROR(this->get_logger(), "Error: sensor failed");
RCLCPP_FATAL(this->get_logger(), "Fatal: shutting down");

// Log only once (even if called many times)
RCLCPP_INFO_ONCE(this->get_logger(), "This prints only once");

// Log with throttle (at most once every N seconds)
RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000, "Every 2s");
```

> - `_ONCE` suffix — logs the message only the **first** time it's reached. Useful in callbacks.
> - `_THROTTLE` suffix — logs at most once per specified milliseconds. Useful for high-frequency loops.
> - `%d` — format for integer. `%f` — float. `%s` — string. `%.2f` — float with 2 decimals. Same as C `printf`.

## Debugging commands

```bash
# See all logs from a running node
ros2 run my_pkg my_node --ros-args --log-level DEBUG

# Inspect topics
ros2 topic list                  # all active topics
ros2 topic echo /cmd_vel         # print messages in real time
ros2 topic hz /cmd_vel           # measure publish frequency
ros2 topic info /cmd_vel         # how many pub/sub on this topic
ros2 topic bw /camera/image_raw  # measure bandwidth (bytes/sec)

# Inspect nodes
ros2 node list                   # all running nodes
ros2 node info /my_robot_node    # show subscriptions, publications, services

# Visual tools
rqt_graph                        # graph of nodes and topics
rqt_console                      # GUI log viewer
rviz2                            # 3D visualization
```

> - `--log-level DEBUG` — shows all log levels including `debug` (hidden by default).
> - `ros2 topic bw` — **b**and**w**idth. Shows how much data (bytes/second) flows on a topic. Useful for camera streams.
> - `rqt_console` — a GUI that shows all node logs with filtering by level and node name. Easier than reading the terminal.

---

# 14. Full Node Examples

## 🐍 Python — Complete Robot Controller

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

class RobotController(Node):
    """
    A robot controller that:
    - Reads LiDAR data
    - Avoids obstacles
    - Publishes velocity commands
    - Accepts enable/disable commands
    """

    SAFE_DISTANCE = 0.5    # metres — class constant

    def __init__(self):
        super().__init__('robot_controller')

        # ── Parameters ──────────────────────────────────────────
        self.declare_parameter('speed', 0.3)
        self.speed = self.get_parameter('speed').value

        # ── State ───────────────────────────────────────────────
        self.enabled     = False
        self.min_dist    = float('inf')   # infinity (no obstacle)

        # ── Publishers ──────────────────────────────────────────
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # ── Subscribers ─────────────────────────────────────────
        self.create_subscription(LaserScan, '/scan',   self.on_scan,   10)
        self.create_subscription(Bool,      '/enable', self.on_enable, 10)

        # ── Control loop: 10 Hz ──────────────────────────────────
        self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Robot Controller ready.')

    def on_scan(self, msg: LaserScan):
        """Process LiDAR data — find closest obstacle"""
        valid = [r for r in msg.ranges if 0.01 < r < 100.0]  # filter bad values
        self.min_dist = min(valid) if valid else float('inf')

    def on_enable(self, msg: Bool):
        """Enable or disable the robot"""
        self.enabled = msg.data
        state = 'ENABLED' if self.enabled else 'DISABLED'
        self.get_logger().info(f'Robot {state}')

    def control_loop(self):
        """Main control — runs 10 times per second"""
        cmd = Twist()

        if self.enabled:
            if self.min_dist > self.SAFE_DISTANCE:
                cmd.linear.x = self.speed    # Move forward
            else:
                cmd.linear.x  = 0.0          # Stop
                cmd.angular.z = 0.5          # Turn away
                self.get_logger().warn(f'Obstacle at {self.min_dist:.2f}m!')

        self.vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

> - `float('inf')` — Python's **infinity** value. Any real distance will be smaller, so it's a safe initial value for "no obstacle detected".
> - `[r for r in msg.ranges if condition]` — Python **list comprehension**: creates a new list by filtering another. Equivalent to a for loop with an if inside.
> - `if __name__ == '__main__'` — runs `main()` only when the script is executed directly, not when imported as a module. Good practice in every Python file.
> - `SAFE_DISTANCE = 0.5` — uppercase = **class constant** by Python convention. Never changes after definition.

---

## ⚙️ C++ — Complete Robot Controller

```cpp
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "std_msgs/msg/bool.hpp"
#include <algorithm>   // for std::min_element
#include <limits>      // for std::numeric_limits

class RobotController : public rclcpp::Node
{
public:
    RobotController() : Node("robot_controller"),
                        enabled_(false),
                        min_dist_(std::numeric_limits<float>::infinity())
    {
        // ── Parameters ──────────────────────────────────────────
        this->declare_parameter("speed", 0.3);
        speed_ = this->get_parameter("speed").as_double();

        // ── Publishers ──────────────────────────────────────────
        vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

        // ── Subscribers ─────────────────────────────────────────
        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10,
            std::bind(&RobotController::on_scan, this, std::placeholders::_1));

        enable_sub_ = this->create_subscription<std_msgs::msg::Bool>(
            "/enable", 10,
            std::bind(&RobotController::on_enable, this, std::placeholders::_1));

        // ── Control loop: 10 Hz ──────────────────────────────────
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&RobotController::control_loop, this));

        RCLCPP_INFO(this->get_logger(), "Robot Controller ready.");
    }

private:
    static constexpr float SAFE_DISTANCE = 0.5f;   // metres

    void on_scan(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        auto& r = msg->ranges;
        auto  it = std::min_element(r.begin(), r.end());
        min_dist_ = (it != r.end()) ? *it : std::numeric_limits<float>::infinity();
    }

    void on_enable(const std_msgs::msg::Bool::SharedPtr msg)
    {
        enabled_ = msg->data;
        RCLCPP_INFO(this->get_logger(), "Robot %s", enabled_ ? "ENABLED" : "DISABLED");
    }

    void control_loop()
    {
        auto cmd = geometry_msgs::msg::Twist();

        if (enabled_) {
            if (min_dist_ > SAFE_DISTANCE) {
                cmd.linear.x = speed_;
            } else {
                cmd.linear.x  = 0.0;
                cmd.angular.z = 0.5;
                RCLCPP_WARN(this->get_logger(), "Obstacle at %.2f m!", min_dist_);
            }
        }
        vel_pub_->publish(cmd);
    }

    // Publishers / Subscribers / Timers
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr         vel_pub_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr    scan_sub_;
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr            enable_sub_;
    rclcpp::TimerBase::SharedPtr                                    timer_;

    // State
    bool   enabled_;
    float  min_dist_;
    double speed_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RobotController>());
    rclcpp::shutdown();
    return 0;
}
```

> - `static constexpr float` — `static` = belongs to the class, not an instance. `constexpr` = **const**ant **expr**ession: evaluated at **compile time**, not runtime. The safest way to define a class constant in C++.
> - `std::numeric_limits<float>::infinity()` — C++'s portable way to get the infinity value for a float. From `<limits>`.
> - `auto& r = msg->ranges` — `&` = **reference** (no copy). `r` is an alias to `msg->ranges`. More efficient than copying the whole array.
> - `enabled_ ? "ENABLED" : "DISABLED"` — the **ternary operator**: `condition ? value_if_true : value_if_false`. A compact if/else.
> - `#include <algorithm>` — includes STL algorithms like `std::min_element`, `std::sort`, `std::find`.
> - `#include <limits>` — includes `std::numeric_limits` for min/max values of numeric types.

---

# 15. Cheat Sheet

## Python vs C++ — Side by Side

| What | Python (`rclpy`) | C++ (`rclcpp`) |
|---|---|---|
| Import library | `import rclpy` | `#include "rclcpp/rclcpp.hpp"` |
| Import message | `from std_msgs.msg import String` | `#include "std_msgs/msg/string.hpp"` |
| Inherit Node | `class My(Node):` | `class My : public rclcpp::Node` |
| Parent constructor | `super().__init__('name')` | `: Node("name")` |
| Create publisher | `self.create_publisher(Type, '/t', 10)` | `this->create_publisher<Type>("/t", 10)` |
| Create subscriber | `self.create_subscription(T,'/t',cb,10)` | `this->create_subscription<T>("/t",10,bind(...))` |
| Create timer | `self.create_timer(1.0, self.cb)` | `this->create_wall_timer(chrono::seconds(1), bind(...))` |
| Publish | `self.pub.publish(msg)` | `pub_->publish(msg)` |
| Declare param | `self.declare_parameter('x', 1.0)` | `this->declare_parameter("x", 1.0)` |
| Get param | `self.get_parameter('x').value` | `this->get_parameter("x").as_double()` |
| Log info | `self.get_logger().info('msg')` | `RCLCPP_INFO(this->get_logger(), "msg")` |
| Log warn | `self.get_logger().warn('msg')` | `RCLCPP_WARN(this->get_logger(), "msg")` |
| Initialize | `rclpy.init()` | `rclcpp::init(argc, argv)` |
| Spin | `rclpy.spin(node)` | `rclcpp::spin(node)` |
| Shutdown | `rclpy.shutdown()` | `rclcpp::shutdown()` |

## Communication patterns

| Pattern | When to use | Keywords |
|---|---|---|
| **Topic (pub/sub)** | Continuous data streams | `create_publisher`, `create_subscription` |
| **Service** | One-shot request/response | `create_service`, `create_client` |
| **Action** | Long task + feedback + cancel | `ActionServer`, `ActionClient` |
| **Parameter** | Configurable values | `declare_parameter`, `get_parameter` |

## Key abbreviations

| Abbreviation | Full form |
|---|---|
| `rclpy` | ROS Client Library for Python |
| `rclcpp` | ROS Client Library for C++ |
| `QoS` | Quality of Service |
| `DDS` | Data Distribution Service |
| `TF` | Transform |
| `OOP` | Object Oriented Programming |
| `CLI` | Command Line Interface |
| `IMU` | Inertial Measurement Unit |
| `SLAM` | Simultaneous Localization And Mapping |
| `Nav2` | Navigation 2 (ROS2 navigation stack) |
| `STL` | Standard Template Library (C++) |
| `YAML` | Yet Another Markup Language |
| `PID` | Proportional Integral Derivative |
| `Hz` | Hertz (frequency unit) |
| `rad/s` | Radians per second |
| `m/s` | Metres per second |
