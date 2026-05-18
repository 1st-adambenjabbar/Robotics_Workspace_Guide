import rclpy
from rclpy.node import Node

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.get_logger().info('Simple ROS 2 Node has been started.')

def main(args=None):
    rclpy.init(args=args)
    node = SimplePublisher()
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
