---
sidebar_position: 3
title: VSLAM and Navigation
---

# Visual SLAM and Navigation

In this section, we'll explore Visual Simultaneous Localization and Mapping (VSLAM) and how it enables robots to navigate in unknown environments. We'll learn about the principles of VSLAM, how to implement navigation algorithms, and how to use NVIDIA Isaac tools for visual navigation.

## Learning Objectives

By the end of this section, you will be able to:

- Understand the principles of Visual SLAM
- Implement feature detection and tracking algorithms
- Create occupancy grid maps from visual data
- Plan paths using visual SLAM information
- Integrate VSLAM with robot navigation systems

## Introduction to Visual SLAM

Visual SLAM (Simultaneous Localization and Mapping) is a technique that allows robots to create a map of an unknown environment while simultaneously localizing themselves within that map using visual sensors.

### VSLAM Pipeline

The VSLAM process typically involves:

1. **Feature Detection**: Identifying distinctive points in images
2. **Feature Tracking**: Following features across multiple frames
3. **Pose Estimation**: Estimating camera/robot motion
4. **Mapping**: Building a 3D map of the environment
5. **Loop Closure**: Recognizing previously visited locations

## Feature Detection and Tracking

Feature detection and tracking are fundamental to VSLAM systems.

### Common Feature Detectors

```python
import cv2
import numpy as np

class FeatureDetector:
    def __init__(self, detector_type='ORB'):
        if detector_type == 'ORB':
            self.detector = cv2.ORB_create(nfeatures=1000)
        elif detector_type == 'SIFT':
            self.detector = cv2.SIFT_create()
        elif detector_type == 'FAST':
            self.detector = cv2.FastFeatureDetector_create()

    def detect_features(self, image):
        """
        Detect features in the image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        keypoints = self.detector.detect(gray, None)
        keypoints, descriptors = self.detector.compute(gray, keypoints)
        return keypoints, descriptors

class FeatureTracker:
    def __init__(self):
        self.matcher = cv2.BFMatcher()
        self.prev_descriptors = None
        self.prev_keypoints = None

    def track_features(self, curr_image, prev_image=None):
        """
        Track features between current and previous frames
        """
        detector = FeatureDetector()
        curr_kp, curr_desc = detector.detect_features(curr_image)

        if self.prev_descriptors is not None:
            # Match features between frames
            matches = self.matcher.knnMatch(self.prev_descriptors, curr_desc, k=2)

            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)

            # Extract matched keypoints
            prev_matched = np.float32([self.prev_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            curr_matched = np.float32([curr_kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            return prev_matched, curr_matched, good_matches

        # Store current frame for next iteration
        self.prev_descriptors = curr_desc
        self.prev_keypoints = curr_kp

        return None, None, []
```

## Pose Estimation

Pose estimation determines the camera/robot motion between frames.

### Essential Matrix and Pose Recovery

```python
import numpy as np
import cv2

class PoseEstimator:
    def __init__(self, camera_matrix):
        self.camera_matrix = camera_matrix
        self.relative_pose = np.eye(4)  # Initial pose
        self.absolute_pose = np.eye(4)  # Global pose

    def estimate_pose(self, prev_points, curr_points):
        """
        Estimate relative pose between frames using essential matrix
        """
        # Compute essential matrix
        E, mask = cv2.findEssentialMat(
            prev_points,
            curr_points,
            self.camera_matrix,
            method=cv2.RANSAC,
            prob=0.999,
            threshold=1.0
        )

        if E is not None:
            # Recover pose from essential matrix
            _, R, t, _ = cv2.recoverPose(E, prev_points, curr_points, self.camera_matrix)

            # Create transformation matrix
            transformation = np.eye(4)
            transformation[:3, :3] = R
            transformation[:3, 3] = t.ravel()

            # Update relative pose
            self.relative_pose = transformation

            # Update absolute pose
            self.absolute_pose = self.absolute_pose @ np.linalg.inv(transformation)

            return self.relative_pose, self.absolute_pose

        return None, None
```

## Mapping

Mapping involves creating a representation of the environment from visual observations.

### Occupancy Grid Mapping

```python
import numpy as np
import matplotlib.pyplot as plt

class OccupancyGridMapper:
    def __init__(self, resolution=0.1, width=100, height=100):
        self.resolution = resolution  # meters per cell
        self.grid = np.zeros((height, width))  # Log odds representation
        self.origin = np.array([width//2, height//2])  # Center of grid

    def update_grid(self, robot_pose, laser_scan):
        """
        Update occupancy grid based on robot pose and laser scan
        """
        # Convert robot pose to grid coordinates
        robot_x = int(robot_pose[0, 3] / self.resolution) + self.origin[0]
        robot_y = int(robot_pose[1, 3] / self.resolution) + self.origin[1]

        # Process each laser beam
        for angle, distance in enumerate(laser_scan):
            if distance < 0.1 or distance > 30.0:  # Skip invalid readings
                continue

            # Calculate beam endpoint
            beam_angle = angle * np.pi / 180  # Assuming 1 degree per beam
            beam_x = int((robot_pose[0, 3] + distance * np.cos(beam_angle)) / self.resolution) + self.origin[0]
            beam_y = int((robot_pose[1, 3] + distance * np.sin(beam_angle)) / self.resolution) + self.origin[1]

            # Bresenham's line algorithm to update free space
            self.update_free_space(robot_x, robot_y, beam_x, beam_y)

            # Mark endpoint as occupied
            if 0 <= beam_x < self.grid.shape[1] and 0 <= beam_y < self.grid.shape[0]:
                self.grid[beam_y, beam_x] += 0.9  # Increase occupancy

    def update_free_space(self, x0, y0, x1, y1):
        """
        Update grid to mark free space along a line
        """
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        x, y = x0, y0
        while True:
            if 0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]:
                self.grid[y, x] -= 0.3  # Decrease occupancy (mark as free)
                self.grid[y, x] = max(-2.0, self.grid[y, x])  # Clamp to reasonable range

            if x == x1 and y == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def get_map(self):
        """
        Convert log odds to probability
        """
        prob_map = 1 - 1 / (1 + np.exp(self.grid))
        return prob_map
```

## Visual SLAM Integration with ROS 2

Integrating VSLAM with ROS 2 enables seamless navigation.

### ROS 2 VSLAM Node

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
import cv2
from cv_bridge import CvBridge
import numpy as np

class VSLAMNode(Node):
    def __init__(self):
        super().__init__('vslam_node')

        # Initialize VSLAM components
        self.feature_detector = FeatureDetector()
        self.feature_tracker = FeatureTracker()
        self.pose_estimator = PoseEstimator(self.get_camera_matrix())
        self.occupancy_mapper = OccupancyGridMapper()

        # Initialize OpenCV bridge
        self.cv_bridge = CvBridge()

        # Create subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera_info',
            self.camera_info_callback,
            10
        )

        # Create publishers
        self.odom_pub = self.create_publisher(Odometry, '/vslam/odometry', 10)
        self.pose_pub = self.create_publisher(PoseStamped, '/vslam/pose', 10)

        # Initialize TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Store camera matrix
        self.camera_matrix = None
        self.prev_image = None

    def camera_info_callback(self, msg):
        """
        Store camera calibration information
        """
        self.camera_matrix = np.array(msg.k).reshape(3, 3)

    def image_callback(self, msg):
        """
        Process incoming camera images for VSLAM
        """
        # Convert ROS image to OpenCV format
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        if self.prev_image is not None:
            # Track features between frames
            prev_matched, curr_matched, matches = self.feature_tracker.track_features(cv_image, self.prev_image)

            if len(matches) > 10:  # Require minimum matches for reliable pose
                # Estimate pose
                relative_pose, absolute_pose = self.pose_estimator.estimate_pose(prev_matched, curr_matched)

                if relative_pose is not None:
                    # Publish odometry
                    self.publish_odometry(absolute_pose, msg.header.stamp)

                    # Update occupancy map (if laser scan is available)
                    # self.occupancy_mapper.update_grid(absolute_pose, laser_scan)

        # Store current image for next iteration
        self.prev_image = cv_image.copy()

    def publish_odometry(self, pose, stamp):
        """
        Publish odometry information
        """
        odom_msg = Odometry()
        odom_msg.header.stamp = stamp
        odom_msg.header.frame_id = 'map'
        odom_msg.child_frame_id = 'camera'

        # Set position
        odom_msg.pose.pose.position.x = pose[0, 3]
        odom_msg.pose.pose.position.y = pose[1, 3]
        odom_msg.pose.pose.position.z = pose[2, 3]

        # Convert rotation matrix to quaternion
        quat = self.rotation_matrix_to_quaternion(pose[:3, :3])
        odom_msg.pose.pose.orientation.x = quat[0]
        odom_msg.pose.pose.orientation.y = quat[1]
        odom_msg.pose.pose.orientation.z = quat[2]
        odom_msg.pose.pose.orientation.w = quat[3]

        # Publish odometry
        self.odom_pub.publish(odom_msg)

        # Broadcast transform
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'map'
        t.child_frame_id = 'camera'
        t.transform.translation.x = pose[0, 3]
        t.transform.translation.y = pose[1, 3]
        t.transform.translation.z = pose[2, 3]
        t.transform.rotation.x = quat[0]
        t.transform.rotation.y = quat[1]
        t.transform.rotation.z = quat[2]
        t.transform.rotation.w = quat[3]

        self.tf_broadcaster.sendTransform(t)

    def rotation_matrix_to_quaternion(self, R):
        """
        Convert rotation matrix to quaternion
        """
        trace = np.trace(R)
        if trace > 0:
            s = np.sqrt(trace + 1.0) * 2
            w = 0.25 * s
            x = (R[2, 1] - R[1, 2]) / s
            y = (R[0, 2] - R[2, 0]) / s
            z = (R[1, 0] - R[0, 1]) / s
        else:
            if R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
                s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
                w = (R[2, 1] - R[1, 2]) / s
                x = 0.25 * s
                y = (R[0, 1] + R[1, 0]) / s
                z = (R[0, 2] + R[2, 0]) / s
            elif R[1, 1] > R[2, 2]:
                s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
                w = (R[0, 2] - R[2, 0]) / s
                x = (R[0, 1] + R[1, 0]) / s
                y = 0.25 * s
                z = (R[1, 2] + R[2, 1]) / s
            else:
                s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
                w = (R[1, 0] - R[0, 1]) / s
                x = (R[0, 2] + R[2, 0]) / s
                y = (R[1, 2] + R[2, 1]) / s
                z = 0.25 * s

        return np.array([x, y, z, w])

    def get_camera_matrix(self):
        """
        Get default camera matrix (should be replaced with actual calibration)
        """
        return np.array([
            [500.0, 0.0, 320.0],  # fx, 0, cx
            [0.0, 500.0, 240.0],  # 0, fy, cy
            [0.0, 0.0, 1.0]       # 0, 0, 1
        ])
```

## NVIDIA Isaac ROS VSLAM

NVIDIA Isaac provides optimized VSLAM implementations:

### Isaac ROS Visual SLAM Pipeline

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

class IsaacROSVisualSLAMNode(Node):
    def __init__(self):
        super().__init__('isaac_ros_vslam')

        # Subscribe to stereo camera or RGB-D input
        self.left_image_sub = self.create_subscription(
            Image,
            '/camera/left/image_rect_color',
            self.left_image_callback,
            10
        )

        self.right_image_sub = self.create_subscription(
            Image,
            '/camera/right/image_rect_color',
            self.right_image_callback,
            10
        )

        self.left_camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/left/camera_info',
            self.camera_info_callback,
            10
        )

        # Publish results
        self.pose_pub = self.create_publisher(PoseStamped, '/visual_slam/pose', 10)
        self.path_pub = self.create_publisher(Path, '/visual_slam/path', 10)

        # Initialize Isaac ROS VSLAM components
        self.initialized = False
        self.path = Path()
        self.path.header.frame_id = 'map'

    def left_image_callback(self, msg):
        """
        Process left camera image for stereo VSLAM
        """
        if not self.initialized:
            return

        # This would interface with Isaac ROS VSLAM pipeline
        # Process visual features and estimate pose
        pass

    def right_image_callback(self, msg):
        """
        Process right camera image for stereo VSLAM
        """
        if not self.initialized:
            return

        # Process right image for stereo matching
        pass

    def camera_info_callback(self, msg):
        """
        Handle camera calibration information
        """
        if not self.initialized:
            # Initialize VSLAM with camera parameters
            self.initialized = True
```

## Practical Exercise

Implement a basic VSLAM system that:

1. Detects and tracks visual features in camera images
2. Estimates camera pose using feature correspondences
3. Builds an occupancy grid map from visual observations
4. Publishes pose and map information via ROS 2

## Summary

In this section, we covered:

- Principles of Visual SLAM
- Feature detection and tracking algorithms
- Pose estimation using essential matrix
- Occupancy grid mapping from visual data
- Integration with ROS 2 for navigation

VSLAM enables robots to navigate in unknown environments using only visual sensors, making it a powerful approach for autonomous navigation.