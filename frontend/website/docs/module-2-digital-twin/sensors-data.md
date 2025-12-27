---
sidebar_position: 4
title: Sensor Data Simulation
---

# Sensor Data Simulation

In this section, we'll explore how to simulate various sensors used in robotics, including LiDAR, depth cameras, and IMUs. We'll learn how to generate realistic sensor data for use in robotics algorithms and simulation environments.

## Learning Objectives

By the end of this section, you will be able to:

- Simulate LiDAR sensors with realistic noise and limitations
- Generate depth camera data with realistic distortion
- Model IMU sensors with bias and noise characteristics
- Integrate sensor simulation with ROS 2 message formats
- Validate sensor fusion algorithms using simulated data

## Introduction to Sensor Simulation

Robotic systems rely on various sensors to perceive their environment and navigate safely. Sensor simulation is crucial for:

- Testing algorithms without physical hardware
- Creating diverse training data for machine learning
- Validating sensor fusion techniques
- Prototyping robot behaviors in simulation

## LiDAR Sensor Simulation

LiDAR (Light Detection and Ranging) sensors provide 2D or 3D range measurements by emitting laser pulses and measuring return times.

### LiDAR Data Format

LiDAR data is typically published as `sensor_msgs/LaserScan` messages with fields:
- `ranges`: Array of distance measurements
- `intensities`: Array of return intensities (optional)
- `angle_min`, `angle_max`: Angular range of the scan
- `angle_increment`: Angular resolution
- `time_increment`: Time between measurements
- `scan_time`: Total time to complete scan
- `range_min`, `range_max`: Valid range limits

### Simulating LiDAR Noise

Real LiDAR sensors have various sources of error:

```python
import numpy as np
from sensor_msgs.msg import LaserScan

def add_lidar_noise(scan_ranges, std_dev=0.01):
    """
    Add realistic noise to LiDAR measurements
    """
    # Add Gaussian noise
    noisy_ranges = np.array(scan_ranges) + np.random.normal(0, std_dev, len(scan_ranges))

    # Apply minimum range (sensor blind spot)
    noisy_ranges = np.maximum(noisy_ranges, 0.1)

    # Apply maximum range (infinite distance readings)
    noisy_ranges = np.where(np.array(scan_ranges) > 30.0, float('inf'), noisy_ranges)

    return noisy_ranges.tolist()

def simulate_lidar_scan(ground_truth_ranges, angle_increment, angle_min, angle_max):
    """
    Simulate a complete LiDAR scan with noise
    """
    scan_msg = LaserScan()
    scan_msg.angle_min = angle_min
    scan_msg.angle_max = angle_max
    scan_msg.angle_increment = angle_increment
    scan_msg.time_increment = 0.0  # Simplified
    scan_msg.scan_time = 0.1  # 10Hz
    scan_msg.range_min = 0.1
    scan_msg.range_max = 30.0

    # Add realistic noise to measurements
    scan_msg.ranges = add_lidar_noise(ground_truth_ranges)

    return scan_msg
```

## Depth Camera Simulation

Depth cameras provide distance measurements for each pixel in their field of view, creating a 2D array of depth values.

### Depth Camera Data Format

Depth camera data is typically published as `sensor_msgs/Image` messages with:
- `encoding`: Often "32FC1" for 32-bit float depth values
- `data`: Array of depth values in meters
- `width`, `height`: Image dimensions

### Simulating Depth Camera Noise

```python
import numpy as np
from sensor_msgs.msg import Image
import cv2

def add_depth_noise(depth_image, base_noise_std=0.01, distance_factor=0.001):
    """
    Add realistic noise to depth image
    Noise increases with distance (1/r^2 relationship)
    """
    # Calculate distance-dependent noise
    noise_std = base_noise_std + distance_factor * depth_image

    # Add Gaussian noise
    noisy_depth = depth_image + np.random.normal(0, noise_std, depth_image.shape)

    # Apply minimum depth (avoid negative values)
    noisy_depth = np.maximum(noisy_depth, 0.1)

    return noisy_depth

def simulate_depth_camera(ground_truth_depth):
    """
    Simulate depth camera with realistic noise
    """
    # Add noise to ground truth depth
    noisy_depth = add_depth_noise(ground_truth_depth)

    # Convert to ROS Image message
    depth_msg = Image()
    depth_msg.height = noisy_depth.shape[0]
    depth_msg.width = noisy_depth.shape[1]
    depth_msg.encoding = "32FC1"
    depth_msg.is_bigendian = False
    depth_msg.step = 4 * noisy_depth.shape[1]  # 4 bytes per float

    # Convert to bytes
    depth_msg.data = noisy_depth.astype(np.float32).tobytes()

    return depth_msg
```

## IMU Sensor Simulation

Inertial Measurement Units (IMUs) provide measurements of acceleration, angular velocity, and sometimes magnetic field.

### IMU Data Format

IMU data is typically published as `sensor_msgs/Imu` messages with:
- `linear_acceleration`: Acceleration in x, y, z axes
- `angular_velocity`: Angular velocity in x, y, z axes
- `orientation`: Orientation as quaternion
- `linear_acceleration_covariance`: Covariance matrix for acceleration
- `angular_velocity_covariance`: Covariance matrix for angular velocity
- `orientation_covariance`: Covariance matrix for orientation

### Simulating IMU Characteristics

```python
import numpy as np
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3, Quaternion

class IMUSimulator:
    def __init__(self, accel_bias_std=0.01, gyro_bias_std=0.001,
                 accel_noise_std=0.005, gyro_noise_std=0.0005):
        self.accel_bias = np.random.normal(0, accel_bias_std, 3)
        self.gyro_bias = np.random.normal(0, gyro_bias_std, 3)
        self.accel_noise_std = accel_noise_std
        self.gyro_noise_std = gyro_noise_std

    def simulate_imu(self, true_accel, true_gyro, true_orientation):
        """
        Simulate IMU measurements with bias and noise
        """
        # Add bias and noise to accelerometer
        accel_measurement = true_accel + self.accel_bias + \
                           np.random.normal(0, self.accel_noise_std, 3)

        # Add bias and noise to gyroscope
        gyro_measurement = true_gyro + self.gyro_bias + \
                          np.random.normal(0, self.gyro_noise_std, 3)

        # Add noise to orientation
        orientation_noise = np.random.normal(0, 0.01, 4)
        orientation_measurement = true_orientation + orientation_noise
        # Normalize quaternion
        orientation_measurement = orientation_measurement / np.linalg.norm(orientation_measurement)

        # Create ROS IMU message
        imu_msg = Imu()
        imu_msg.linear_acceleration = Vector3(
            x=accel_measurement[0],
            y=accel_measurement[1],
            z=accel_measurement[2]
        )
        imu_msg.angular_velocity = Vector3(
            x=gyro_measurement[0],
            y=gyro_measurement[1],
            z=gyro_measurement[2]
        )
        imu_msg.orientation = Quaternion(
            x=orientation_measurement[0],
            y=orientation_measurement[1],
            z=orientation_measurement[2],
            w=orientation_measurement[3]
        )

        # Set covariance matrices (diagonal values)
        imu_msg.linear_acceleration_covariance = [
            self.accel_noise_std**2, 0, 0,
            0, self.accel_noise_std**2, 0,
            0, 0, self.accel_noise_std**2
        ]
        imu_msg.angular_velocity_covariance = [
            self.gyro_noise_std**2, 0, 0,
            0, self.gyro_noise_std**2, 0,
            0, 0, self.gyro_noise_std**2
        ]
        imu_msg.orientation_covariance = [
            0.01, 0, 0,
            0, 0.01, 0,
            0, 0, 0.01
        ]

        return imu_msg
```

## Sensor Fusion Simulation

Sensor fusion combines data from multiple sensors to improve perception accuracy.

### Example: LiDAR-Camera Fusion

```python
import numpy as np

class SensorFusionSimulator:
    def __init__(self):
        self.lidar_sim = None  # LiDAR simulator instance
        self.camera_sim = None  # Camera simulator instance
        self.imu_sim = IMUSimulator()  # IMU simulator instance

    def simulate_sensor_data(self, robot_state):
        """
        Simulate all sensor data based on robot state
        """
        # Get ground truth from simulation
        true_position = robot_state.position
        true_velocity = robot_state.velocity
        true_orientation = robot_state.orientation
        true_angular_velocity = robot_state.angular_velocity
        true_acceleration = robot_state.acceleration

        # Simulate individual sensors
        lidar_data = self.lidar_sim.simulate_lidar_scan(
            self.get_ground_truth_lidar(robot_state)
        )

        camera_data = self.camera_sim.simulate_camera_image(
            self.get_ground_truth_image(robot_state)
        )

        imu_data = self.imu_sim.simulate_imu(
            true_acceleration,
            true_angular_velocity,
            true_orientation
        )

        return {
            'lidar': lidar_data,
            'camera': camera_data,
            'imu': imu_data
        }

    def get_ground_truth_lidar(self, robot_state):
        """
        Calculate ground truth LiDAR measurements based on environment
        """
        # This would typically involve raycasting in a 3D environment
        # For simulation, we return ideal measurements
        ground_truth_ranges = [2.0] * 360  # 360 degree scan
        return ground_truth_ranges

    def get_ground_truth_image(self, robot_state):
        """
        Calculate ground truth camera image based on environment
        """
        # This would typically involve rendering in a 3D environment
        # For simulation, we return an ideal depth image
        height, width = 480, 640
        ground_truth_depth = np.ones((height, width)) * 2.0  # 2m to nearest obstacle
        return ground_truth_depth
```

## ROS 2 Message Integration

All sensor data must be properly formatted as ROS 2 messages:

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image, Imu
import numpy as np

class SensorSimulatorNode(Node):
    def __init__(self):
        super().__init__('sensor_simulator')

        # Create publishers for different sensor types
        self.lidar_publisher = self.create_publisher(LaserScan, '/scan', 10)
        self.camera_publisher = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        self.imu_publisher = self.create_publisher(Imu, '/imu/data', 10)

        # Timer for sensor simulation
        self.timer = self.create_timer(0.1, self.publish_sensor_data)  # 10Hz

        # Initialize simulators
        self.lidar_sim = LiDARSimulator()
        self.camera_sim = CameraSimulator()
        self.imu_sim = IMUSimulator()

    def publish_sensor_data(self):
        """
        Publish simulated sensor data
        """
        # Simulate sensor readings
        lidar_msg = self.lidar_sim.simulate_scan()
        camera_msg = self.camera_sim.simulate_image()
        imu_msg = self.imu_sim.simulate_imu()

        # Publish messages
        self.lidar_publisher.publish(lidar_msg)
        self.camera_publisher.publish(camera_msg)
        self.imu_publisher.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)
    sensor_simulator = SensorSimulatorNode()

    try:
        rclpy.spin(sensor_simulator)
    except KeyboardInterrupt:
        pass
    finally:
        sensor_simulator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Practical Exercise

Create a complete sensor simulation node that publishes:

1. LiDAR data with realistic noise characteristics
2. Depth camera data with distance-dependent noise
3. IMU data with bias and noise models
4. All messages properly formatted for ROS 2

## Summary

In this section, we covered:

- LiDAR sensor simulation with noise modeling
- Depth camera simulation with realistic characteristics
- IMU sensor simulation with bias and noise
- Sensor fusion approaches in simulation
- ROS 2 message integration for sensor data

Realistic sensor simulation is essential for developing robust robotics algorithms that can handle the noise and limitations of real-world sensors.