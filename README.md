# Self-driving-car

My objective with this project is to guide myself through the development of a simulated autonomous vehicle. I will be using a combination of cutting-edge technologies, including PyTorch, NVIDIA Omniverse, Gazebo, and ROS 2. My ultimate goal is to create a system capable of lane following, object detection, and operation within a simulated environment, with an optional visualization component in Omniverse.

## 📖 Documentation & Guides

In this section, I will manually explain each part of the project and the installation processes:

*   [WSL Installation](./WSL%20Installation.md) — Setting up the Windows Subsystem for Linux.
*   [Docker & Git Setup](./Docker%20-%20Git.md) — Configuring version control and containerization.
*   [CUDA Installation](./Cuda%20Installation.md) — Enabling GPU acceleration for AI tasks.
*   [ROS2 Installation and Use](./Gazebo%20Installation%20and%20use.md) — Core robotics framework setup.
*   [Gazebo Installation and Use](./Gazebo%20Installation%20and%20use.md) — Simulation environment configuration.
*   [Omniverse Installation and Use](./Omniverse%20Installation%20and%20Use.md) — Advanced visualization setup.

---

## Table of Contents

1.  [My Final Objective](#my-final-objective)
2.  [My Project Strategy](#my-project-strategy)
3.  [My Detailed Step-by-Step Instructions](#my-detailed-step-by-step-instructions)
    *   [Step 1: Setting Up My Environment (ROS2 + Gazebo)](#step-1-setting-up-my-environment-ros2--gazebo)
    *   [Step 2: Implementing My Vision and Control (OpenCV)](#step-2-implementing-my-vision-and-control-opencv)
    *   [Step 3: Integrating My AI (PyTorch + CUDA)](#step-3-integrating-my-ai-pytorch--cuda)
    *   [Step 4: Enhancing My Visuals and Finalizing (Omniverse + Polishing)](#step-4-enhancing-my-visuals-and-finalizing-omniverse--polishing)
4.  [My Final Architecture](#my-final-architecture)
5.  [My Final Project Structure](#my-final-project-structure)
6.  [My Final Demonstration (What I Will Show)](#my-final-demonstration-what-i-will-show)
7.  [My Strict Rules (To Ensure My Completion)](#my-strict-rules-to-ensure-my-completion)
8.  [My Acquired Skills](#my-acquired-skills)
9.  [My Next Steps](#my-next-steps)

## My Final Objective

My objective is to develop a simulated car capable of:

*   Lane following using OpenCV.
*   Object detection using PyTorch with CUDA acceleration.
*   Operating within the Gazebo simulation environment.
*   (Optional) Being visualized in NVIDIA Omniverse.

## My Project Strategy

I will structure this project into **3 distinct layers** to ensure a progressive and manageable development approach:

### Layer 1 — Core Functionality

This foundational layer will establish the essential components of my project:

*   I will set up Gazebo and ROS2.
*   I will implement basic lane following using OpenCV.

### Layer 2 — AI Upgrade

This layer will integrate advanced artificial intelligence capabilities:

*   I will utilize PyTorch for object detection (e.g., YOLO).
*   I will leverage CUDA for GPU acceleration to ensure real-time performance.

### Layer 3 — Visual Enhancement (Optional)

This layer will focus on improving the visual fidelity and demonstration aspects of my project:

*   I will integrate NVIDIA Omniverse for advanced visualization (primarily for demonstration purposes).

## My Detailed Step-by-Step Instructions

This section provides a comprehensive, step-by-step guide to developing my simulated autonomous vehicle. Each step is designed to build upon the previous one, ensuring a structured and efficient development process.

### Step 1: Setting Up My Environment (ROS2 + Gazebo)

**My Objective:** I will establish the core simulation environment and integrate my vehicle model.

1.  **Install ROS2 and Gazebo:**
    *   **My Action:** I will install a stable ROS2 distribution (e.g., Humble Hawksbill, Iron Irwini, or Rolling Ridley) and a compatible version of Gazebo (often included with ROS2 or installed separately as Gazebo Garden/Fortress). I will ensure my system meets the prerequisites for both. I will create a ROS2 workspace, typically named `colcon_ws`, in my home directory. This workspace will house all my ROS2 packages.
    *   **My Commands:**
        ```bash
        # Example for ROS2 Humble on Ubuntu 22.04
        sudo apt update && sudo apt install locales
        sudo locale-gen en_US en_US.UTF-8
        sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
        export LANG=en_US.UTF-8
        
        sudo apt install software-properties-common
        sudo add-apt-repository universe
        
        sudo apt update && sudo apt install curl
        sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
        
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
        sudo apt update
        sudo apt upgrade
        sudo apt install ros-humble-desktop
        
        # Create ROS2 workspace
        mkdir -p ~/colcon_ws/src
        cd ~/colcon_ws
        colcon build
        source install/setup.bash
        ```
    *   **My Verification:** I will confirm that ROS2 commands like `ros2 run` and `ros2 topic list` are functional. I will launch Gazebo independently to ensure it starts without errors.

2.  **Create My ROS2 Package:**
    *   **My Action:** I will navigate to the `src` directory within my `colcon_ws` and create a new ROS2 package named `self_driving_car`. This package will encapsulate all my project-specific nodes, launch files, and configurations. I will ensure I specify `rclpy` as a dependency for Python-based nodes.
    *   **My Commands:**
        ```bash
        cd ~/colcon_ws/src
        ros2 pkg create --build-type ament_python self_driving_car --dependencies rclpy
        ```
    *   **My Verification:** I will check for the creation of the `self_driving_car` directory and its basic structure (e.g., `self_driving_car/__init__.py`, `setup.py`, `package.xml`).

3.  **Load My Vehicle Model and Gazebo World:**
    *   **My Action:** I will obtain a suitable 3D model of a car (e.g., URDF or XACRO format) and place it within my `self_driving_car` package (e.g., in a `urdf` directory). I will create a simple Gazebo world file (`.world`) that includes my car model and a basic environment (e.g., a flat plane with a road texture). I will develop a ROS2 launch file to spawn my car model into the Gazebo world.
    *   **My Commands (Example `launch` file structure):**
        ```python
        # ~/colcon_ws/src/self_driving_car/launch/spawn_car.launch.py
        import os
        from ament_index_python.packages import get_package_share_directory
        from launch import LaunchDescription
        from launch_ros.actions import Node
        
        def generate_launch_description():
            pkg_path = get_package_share_directory("self_driving_car")
            urdf_file = os.path.join(pkg_path, "urdf", "my_car.urdf") # Replace with my URDF file
            world_file = os.path.join(pkg_path, "worlds", "my_world.world") # Replace with my world file

            return LaunchDescription([
                Node(
                    package="gazebo_ros",
                    executable="spawn_entity.py",
                    arguments=["-entity", "my_car", "-file", urdf_file],
                    output="screen"
                ),
                Node(
                    package="gazebo_ros",
                    executable="gazebo_ros",
                    arguments=[world_file],
                    output="screen"
                )
            ])
        ```
    *   **My Verification:** I will execute my launch file (`ros2 launch self_driving_car spawn_car.launch.py`) and observe my car model appearing in the Gazebo simulation environment.

4.  **Configure My Camera Sensor:**
    *   **My Action:** I will modify my car's URDF/XACRO file to include a camera sensor. I will define its position, orientation, field of view, and the ROS2 topic it will publish images to (e.g., `/camera/image_raw`). I will ensure the camera plugin is correctly configured to publish `sensor_msgs/Image` messages.
    *   **My Verification:** After launching my car in Gazebo, I will use `ros2 topic list` to confirm the camera topic is active. Then, I will use `ros2 topic echo /camera/image_raw` to verify that image data is being published. I can also use `rqt_image_view` to visualize the camera feed.

**✅ Outcome of Step 1:** I will have a functional robot with a camera sensor operating correctly within the Gazebo simulation environment, publishing image data via a ROS2 topic.

### Step 2: Implementing My Vision and Control (OpenCV)

**My Objective:** I will enable my car to autonomously follow a lane.

1.  **Install OpenCV and Read Camera Images:**
    *   **My Action:** I will install OpenCV for Python (`opencv-python`). I will develop a new ROS2 Python node (e.g., `lane_detection_node.py` within `self_driving_car/scripts`) that subscribes to the camera image topic (`/camera/image_raw`). I will use `cv_bridge` to convert ROS `sensor_msgs/Image` messages into OpenCV-compatible images.
    *   **My Commands:**
        ```bash
        # Install OpenCV and cv_bridge
        sudo apt install python3-opencv ros-humble-cv-bridge
        
        # Example Python node structure (self_driving_car/scripts/lane_detection_node.py)
        import rclpy
        from rclpy.node import Node
        from sensor_msgs.msg import Image
        from cv_bridge import CvBridge
        import cv2
        
        class LaneDetectionNode(Node):
            def __init__(self):
                super().__init__("lane_detection_node")
                self.subscription = self.create_subscription(
                    Image,
                    "/camera/image_raw",
                    self.image_callback,
                    10)
                self.bridge = CvBridge()
                self.get_logger().info("Lane Detection Node Started")

            def image_callback(self, msg):
                try:
                    cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                    # Process image here
                    # cv2.imshow("Camera Feed", cv_image)
                    # cv2.waitKey(1)
                except Exception as e:
                    self.get_logger().error(f"Error converting image: {e}")

        def main(args=None):
            rclpy.init(args=args)
            node = LaneDetectionNode()
            rclpy.spin(node)
            node.destroy_node()
            rclpy.shutdown()

        if __name__ == "__main__":
            main()
        ```
    *   **My Verification:** I will run my `lane_detection_node.py` and ensure it can subscribe to the camera topic and process images without errors. I can temporarily add `cv2.imshow` to visualize the feed.

2.  **Implement My Lane Detection:**
    *   **My Action:** Within my `image_callback` function, I will implement a robust lane detection pipeline. This typically involves:
        *   **Grayscale Conversion:** I will convert the BGR image to grayscale.
        *   **Gaussian Blur:** I will apply a Gaussian blur to reduce noise.
        *   **Canny Edge Detection:** I will use the Canny algorithm to detect edges in the image.
        *   **Region of Interest (ROI):** I will define a polygonal region of interest to focus on the road ahead and ignore irrelevant parts of the image.
        *   **Hough Transform:** I will apply the Hough Line Transform to detect straight lines within the ROI, representing lane lines.
        *   **Lane Line Averaging:** I will average and extrapolate the detected lines to form clear left and right lane boundaries.
    *   **My Verification:** I will visualize the output of each step (grayscale, edges, ROI, Hough lines) to debug and refine my lane detection algorithm. I will ensure clear lane lines are consistently detected.

3.  **Calculate My Lane Center and Steering Logic:**
    *   **My Action:** Based on the detected left and right lane lines, I will calculate the perceived center of the lane. I will determine the car's deviation from this center. I will develop a proportional-integral-derivative (PID) controller or a simpler proportional controller to generate steering commands (e.g., angular velocity) based on this deviation. My goal is to steer the car back to the center of the lane.
    *   **My Verification:** I will print the calculated lane center and steering commands to the console. I will manually move the car in Gazebo and observe if the steering commands react appropriately to keep the car centered.

4.  **Connect My Control to Robot Movement:**
    *   **My Action:** I will create a new ROS2 publisher in my `lane_detection_node.py` (or a separate `control_node.py`) that publishes `geometry_msgs/Twist` messages to the car's command velocity topic (e.g., `/cmd_vel`). I will map my calculated steering commands (angular velocity) and a constant forward speed (linear velocity) to this `Twist` message. I will ensure my car model in Gazebo is configured to receive and act upon these `cmd_vel` messages.
    *   **My Commands (Example `control_node.py` publishing `Twist` messages):**
        ```python
        # ~/colcon_ws/src/self_driving_car/scripts/control_node.py
        import rclpy
        from rclpy.node import Node
        from geometry_msgs.msg import Twist
        
        class ControlNode(Node):
            def __init__(self):
                super().__init__("control_node")
                self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
                self.timer = self.create_timer(0.1, self.publish_cmd_vel) # 10 Hz
                self.linear_speed = 0.5 # m/s
                self.angular_speed = 0.0 # rad/s (will be updated by lane detection)
                self.get_logger().info("Control Node Started")

            def update_steering(self, new_angular_speed):
                self.angular_speed = new_angular_speed

            def publish_cmd_vel(self):
                twist_msg = Twist()
                twist_msg.linear.x = self.linear_speed
                twist_msg.angular.z = self.angular_speed
                self.publisher_.publish(twist_msg)

        def main(args=None):
            rclpy.init(args=args)
            node = ControlNode()
            # In a real scenario, this node would receive steering commands from lane_detection_node
            # For now, it publishes constant speed and zero angular speed
            rclpy.spin(node)
            node.destroy_node()
            rclpy.shutdown()

        if __name__ == "__main__":
            main()
        ```
    *   **My Verification:** I will launch my `lane_detection_node` and `control_node` simultaneously. I will observe the car in Gazebo. It should start moving forward and attempt to follow the lane lines I've defined in my world. I will debug any erratic behavior by examining the published `Twist` messages and the lane detection output.

**✅ Outcome of Step 2:** My simulated car will autonomously follow a lane within the Gazebo environment, demonstrating basic vision-based control.

### Step 3: Integrating My AI (PyTorch + CUDA)

**My Objective:** I will enhance my car's perception with object detection capabilities using deep learning.

1.  **Install PyTorch with CUDA:**
    *   **My Action:** I will install PyTorch, ensuring I select the version compatible with my NVIDIA GPU and CUDA toolkit. This is crucial for leveraging GPU acceleration for real-time object detection. I will follow the official PyTorch installation instructions for my specific setup.
    *   **My Commands:**
        ```bash
        # Example for CUDA 11.8
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        ```
    *   **My Verification:** I will open a Python interpreter and run `import torch; print(torch.cuda.is_available())`. It must return `True` to confirm successful CUDA integration.

2.  **Select and Load a Pre-trained Object Detection Model:**
    *   **My Action:** I will choose a suitable pre-trained object detection model, such as YOLOv5, YOLOv8, or a model from the PyTorch Video library. I will download the model's weights and integrate them into a new ROS2 node (e.g., `object_detection_node.py`).
    *   **My Verification:** I will test the model on sample images to ensure it can correctly identify objects like other cars, pedestrians, or traffic signs.

3.  **Process Camera Feed for Object Detection:**
    *   **My Action:** Within my `object_detection_node.py`, I will subscribe to the `/camera/image_raw` topic. I will pass each received image through the loaded PyTorch model. I will extract the bounding boxes, labels, and confidence scores for detected objects.
    *   **My Verification:** I will visualize the detection results by drawing bounding boxes on the camera feed and displaying it using `cv2.imshow`.

4.  **Implement Obstacle Avoidance Logic:**
    *   **My Action:** Based on the detected objects and their proximity to the car (which can be estimated from the bounding box size or by integrating a depth sensor/LiDAR), I will develop logic to avoid collisions. This might involve stopping the car, slowing down, or steering away from the obstacle. I will integrate this logic with my existing steering and speed control.
    *   **My Verification:** I will place obstacles in the Gazebo world and observe if the car detects them and takes appropriate action to avoid a collision.

**✅ Outcome of Step 3:** My car will be able to detect and react to obstacles in its environment using a deep learning-based perception system.

### Step 4: Enhancing My Visuals and Finalizing (Omniverse + Polishing)

**My Objective (Optional):** I will integrate NVIDIA Omniverse for high-fidelity visualization and finalize my project.

1.  **Install and Configure NVIDIA Omniverse:**
    *   **My Action:** I will install NVIDIA Omniverse and the necessary extensions for ROS2 integration (e.g., `omni.isaac.ros2_bridge`). I will set up a connection between my ROS2 workspace and Omniverse.
    *   **My Verification:** I will ensure I can send simple ROS2 messages and see their effects within the Omniverse environment.

2.  **Import Vehicle Model and World into Omniverse:**
    *   **My Action:** I will import my car model and the Gazebo world (or a more detailed version of it) into Omniverse. I will configure the materials, lighting, and cameras to achieve high-quality visuals.
    *   **My Verification:** I will visualize my car within the Omniverse scene and ensure it looks as expected.

3.  **Synchronize Gazebo and Omniverse:**
    *   **My Action:** I will use the ROS2 bridge to synchronize the state of my car in Gazebo with its representation in Omniverse. This will allow me to see the car's movements in Gazebo reflected in real-time within the high-fidelity Omniverse environment.
    *   **My Verification:** I will move the car in Gazebo and confirm that its position and orientation are accurately updated in Omniverse.

4.  **Final Testing and Polishing:**
    *   **My Action:** I will conduct thorough testing of the entire system, ensuring all components work seamlessly together. I will refine my code, add comments, and create clear documentation. I will also record a demonstration video showcasing the car's autonomous capabilities and the high-fidelity visualization in Omniverse.
    *   **My Verification:** I will perform a final run-through of the project and ensure it meets all my initial objectives.

**✅ Outcome of Step 4:** I will have a complete, well-documented, and visually impressive simulated autonomous vehicle project.

---

## My Final Architecture

I will implement a modular architecture for my autonomous vehicle system, consisting of several interconnected ROS2 nodes:

*   **`spawn_car.launch.py`:** A launch file that initializes the Gazebo simulation, loads the car model and the world, and starts the necessary ROS2 bridges.
*   **`lane_detection_node.py`:** Subscribes to the camera feed, performs image processing using OpenCV to detect lane lines, and calculates the required steering commands.
*   **`object_detection_node.py`:** Subscribes to the camera feed, utilizes a pre-trained PyTorch model for object detection, and identifies obstacles in the car's path.
*   **`control_node.py`:** Receives steering commands from the lane detection node and obstacle information from the object detection node. It implements the final control logic and publishes `Twist` messages to the car's `/cmd_vel` topic.
*   **Omniverse Bridge:** (Optional) Synchronizes the car's state between Gazebo and NVIDIA Omniverse for high-fidelity visualization.

## My Final Project Structure

I will organize my project into a clear and logical directory structure:

```text
self_driving_car/
├── launch/
│   └── spawn_car.launch.py
├── scripts/
│   ├── lane_detection_node.py
│   ├── object_detection_node.py
│   └── control_node.py
├── urdf/
│   └── my_car.urdf
├── worlds/
│   └── my_world.world
├── models/
│   └── (Pre-trained PyTorch models)
├── config/
│   └── (Configuration files)
├── package.xml
└── setup.py
```

## My Final Demonstration (What I Will Show)

For my final demonstration, I will showcase the following:

1.  **Autonomous Lane Following:** A video of the car successfully navigating a track in Gazebo, staying within the lane lines.
2.  **Obstacle Detection and Avoidance:** A demonstration of the car identifying and reacting to various obstacles (e.g., other cars, pedestrians) placed in its path.
3.  **Real-time Visualization:** A side-by-side view of the Gazebo simulation and the high-fidelity Omniverse visualization, showing the synchronized movement of the car.
4.  **System Performance:** A brief overview of the system's performance, including the frame rate of the object detection and the responsiveness of the control system.

## My Strict Rules (To Ensure My Completion)

I will adhere to the following rules to ensure the successful completion of this project:

*   **Rule 1: Progressive Development:** I will complete each step thoroughly before moving on to the next one.
*   **Rule 2: Modular Design:** I will keep my code modular and well-organized to facilitate debugging and future enhancements.
*   **Rule 3: Regular Testing:** I will test each component independently and as part of the larger system on a regular basis.
*   **Rule 4: Clear Documentation:** I will document my code and the overall system architecture to ensure it's easy to understand and maintain.
*   **Rule 5: Focus on Core Functionality:** I will prioritize the core functionality (lane following and object detection) before spending time on optional features like Omniverse integration.

## My Acquired Skills

Through this project, I will acquire and demonstrate proficiency in the following areas:

*   **Robotics Frameworks:** ROS2 (Humble, Iron, or Rolling)
*   **Simulation Environments:** Gazebo (Garden/Fortress)
*   **Computer Vision:** OpenCV
*   **Deep Learning:** PyTorch
*   **GPU Acceleration:** CUDA
*   **Visualization:** NVIDIA Omniverse
*   **Programming:** Python
*   **System Integration:** Combining multiple technologies into a cohesive system.

## My Next Steps

After completing this project, I plan to:

*   **Implement more advanced control algorithms:** Explore Model Predictive Control (MPC) or Reinforcement Learning (RL) for more sophisticated driving behavior.
*   **Integrate additional sensors:** Add LiDAR or radar for improved obstacle detection and environmental mapping.
*   **Develop more complex simulation scenarios:** Create more realistic and challenging environments with traffic, weather conditions, and diverse road types.
*   **Explore deployment on real hardware:** Investigate the possibility of deploying the developed system on a small-scale physical robot car.
