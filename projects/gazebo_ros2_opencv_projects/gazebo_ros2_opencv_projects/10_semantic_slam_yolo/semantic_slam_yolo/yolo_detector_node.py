#!/usr/bin/env python3
"""Project 10 (node 1/2) - YOLO Object Detector.

Run a YOLOv8 model on the camera stream and publish 2D detections. Kept
deliberately separate from the mapper so you can reuse it standalone.

Concepts introduced
-------------------
* Wrapping a deep model (ultralytics YOLOv8) inside a ROS2 node
* Publishing vision_msgs/Detection2DArray (a standard detection interface)
* Keeping inference off the callback's critical path (throttle / resize)
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from cv_bridge import CvBridge
import cv2

try:
    from ultralytics import YOLO
    _HAVE_YOLO = True
except Exception:                       # pragma: no cover
    _HAVE_YOLO = False


class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('model', 'yolov8n.pt')
        self.declare_parameter('conf', 0.4)
        self.conf = float(self.get_parameter('conf').value)

        if not _HAVE_YOLO:
            self.get_logger().error(
                'ultralytics not installed. Run: pip install ultralytics')
            raise SystemExit(1)

        model_path = self.get_parameter('model').value
        self.model = YOLO(model_path)
        self.names = self.model.names

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.bridge = CvBridge()
        self.create_subscription(Image, self.get_parameter('image_topic').value,
                                 self.on_image, qos)
        self.det_pub = self.create_publisher(Detection2DArray, '/yolo/detections', 10)
        self.img_pub = self.create_publisher(Image, '/yolo/image', 10)
        self.get_logger().info(f'YOLO detector ready ({model_path}).')

    def on_image(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        results = self.model(frame, conf=self.conf, verbose=False)[0]

        out = Detection2DArray()
        out.header = msg.header
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            score = float(box.conf[0])

            d = Detection2D()
            d.header = msg.header
            d.bbox.center.position.x = (x1 + x2) / 2.0
            d.bbox.center.position.y = (y1 + y2) / 2.0
            d.bbox.size_x = x2 - x1
            d.bbox.size_y = y2 - y1
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = self.names[cls]
            hyp.hypothesis.score = score
            d.results.append(hyp)
            out.detections.append(d)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'{self.names[cls]} {score:.2f}', (int(x1), int(y1) - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        self.det_pub.publish(out)
        self.img_pub.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))
        cv2.imshow('yolo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
