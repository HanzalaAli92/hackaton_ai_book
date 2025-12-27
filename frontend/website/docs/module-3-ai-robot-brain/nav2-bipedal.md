---
sidebar_position: 4
title: Nav2 for Bipedal Movement
---

# Nav2 for Bipedal Movement

In this section, we'll explore the Navigation Stack 2 (Nav2) and how it can be adapted for bipedal robot navigation. We'll learn about the architecture of Nav2, how to configure it for legged robots, and how to implement custom behaviors for bipedal locomotion.

## Learning Objectives

By the end of this section, you will be able to:

- Understand the architecture of the Navigation Stack 2 (Nav2)
- Configure Nav2 for bipedal robot navigation
- Implement custom controllers for bipedal locomotion
- Adapt navigation behaviors for legged robots
- Integrate Nav2 with whole-body controllers for bipedal movement

## Introduction to Nav2

Navigation Stack 2 (Nav2) is the latest navigation framework for ROS 2, designed to provide reliable navigation for mobile robots. While originally designed for wheeled robots, Nav2 can be adapted for bipedal robots with appropriate modifications.

### Nav2 Architecture

Nav2 consists of several key components:

1. **Navigation System**: Coordinates the navigation process
2. **Global Planner**: Plans a path from start to goal
3. **Local Planner**: Creates commands to follow the path
4. **Controller**: Translates commands to robot-specific actions
5. **Recovery Behaviors**: Handles navigation failures
6. **Costmap**: Represents obstacles and free space

## Nav2 Components for Bipedal Robots

### Global Planner Adaptation

For bipedal robots, the global planner needs to consider:

- **Step constraints**: Maximum step length and height
- **Terrain traversability**: Rough terrain navigation
- **Stability regions**: Maintaining balance during navigation

```python
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from builtin_interfaces.msg import Time
import numpy as np

class BipedalGlobalPlanner(Node):
    def __init__(self):
        super().__init__('bipedal_global_planner')

        # Create publishers and subscribers
        self.path_pub = self.create_publisher(Path, '/global_plan', 10)
        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        # Bipedal-specific parameters
        self.max_step_length = 0.3  # meters
        self.max_step_height = 0.1  # meters
        self.min_step_width = 0.1   # meters

    def plan_path(self, start_pose, goal_pose):
        """
        Plan a path considering bipedal constraints
        """
        # Create path message
        path_msg = Path()
        path_msg.header.frame_id = 'map'
        path_msg.header.stamp = self.get_clock().now().to_msg()

        # Simple straight-line path (in practice, use A* or Dijkstra)
        # But ensure steps are within bipedal constraints
        path_points = self.generate_bipedal_path(start_pose, goal_pose)

        for point in path_points:
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = 'map'
            pose_stamped.pose.position.x = point[0]
            pose_stamped.pose.position.y = point[1]
            pose_stamped.pose.position.z = 0.0
            pose_stamped.pose.orientation.w = 1.0

            path_msg.poses.append(pose_stamped)

        return path_msg

    def generate_bipedal_path(self, start_pose, goal_pose):
        """
        Generate path considering bipedal step constraints
        """
        # Calculate straight-line path
        dx = goal_pose.position.x - start_pose.position.x
        dy = goal_pose.position.y - start_pose.position.y
        distance = np.sqrt(dx**2 + dy**2)

        # Calculate number of steps needed based on max step length
        num_steps = int(np.ceil(distance / self.max_step_length))

        path_points = []
        for i in range(num_steps + 1):
            t = i / num_steps if num_steps > 0 else 0
            x = start_pose.position.x + t * dx
            y = start_pose.position.y + t * dy
            path_points.append([x, y])

        return path_points

    def goal_callback(self, goal_msg):
        """
        Handle new goal pose
        """
        # Get current robot pose (from TF or localization)
        current_pose = self.get_current_pose()

        # Plan path
        path_msg = self.plan_path(current_pose, goal_msg.pose)

        # Publish path
        self.path_pub.publish(path_msg)
```

### Local Planner for Bipedal Navigation

The local planner needs to consider bipedal-specific dynamics:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Path, Odometry
from tf2_ros import TransformListener, Buffer
import numpy as np

class BipedalLocalPlanner(Node):
    def __init__(self):
        super().__init__('bipedal_local_planner')

        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.path_sub = self.create_subscription(
            Path,
            '/global_plan',
            self.path_callback,
            10
        )
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Bipedal-specific parameters
        self.step_frequency = 1.0  # steps per second
        self.max_step_speed = 0.5  # m/s
        self.lookahead_distance = 0.5  # meters
        self.path_tolerance = 0.1  # meters

        # Path following variables
        self.current_path = None
        self.current_pose = None
        self.current_path_index = 0

        # Timer for control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)

    def path_callback(self, path_msg):
        """
        Receive global path
        """
        self.current_path = path_msg
        self.current_path_index = 0

    def odom_callback(self, odom_msg):
        """
        Receive odometry
        """
        self.current_pose = odom_msg.pose.pose

    def control_loop(self):
        """
        Main control loop for following path
        """
        if self.current_path is None or self.current_pose is None:
            return

        # Find next waypoint
        target_pose = self.get_next_waypoint()
        if target_pose is None:
            # Reached goal
            self.stop_robot()
            return

        # Calculate velocity command for bipedal movement
        cmd_vel = self.calculate_bipedal_command(target_pose)

        # Publish command
        self.cmd_vel_pub.publish(cmd_vel)

    def get_next_waypoint(self):
        """
        Find next waypoint on path
        """
        if self.current_path is None or self.current_path_index >= len(self.current_path.poses):
            return None

        # Find the closest point on path
        min_dist = float('inf')
        closest_idx = self.current_path_index

        for i in range(self.current_path_index, len(self.current_path.poses)):
            pose = self.current_path.poses[i]
            dist = self.calculate_distance(self.current_pose, pose.pose)

            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        # Look ahead to find target point
        target_idx = closest_idx
        for i in range(closest_idx, len(self.current_path.poses)):
            pose = self.current_path.poses[i]
            dist = self.calculate_distance(self.current_path.poses[closest_idx].pose, pose.pose)

            if dist >= self.lookahead_distance:
                target_idx = i
                break

        self.current_path_index = closest_idx
        return self.current_path.poses[target_idx].pose

    def calculate_bipedal_command(self, target_pose):
        """
        Calculate velocity command for bipedal robot
        """
        cmd_vel = Twist()

        if self.current_pose is None:
            return cmd_vel

        # Calculate direction to target
        dx = target_pose.position.x - self.current_pose.position.x
        dy = target_pose.position.y - self.current_pose.position.y
        distance = np.sqrt(dx**2 + dy**2)

        # Calculate angle to target
        target_angle = np.arctan2(dy, dx)

        # Get robot's current orientation
        robot_yaw = self.quaternion_to_yaw(self.current_pose.orientation)

        # Calculate angle difference
        angle_diff = target_angle - robot_yaw
        angle_diff = np.arctan2(np.sin(angle_diff), np.cos(angle_diff))  # Normalize to [-pi, pi]

        # Set linear velocity based on distance and constraints
        if distance > self.path_tolerance:
            cmd_vel.linear.x = min(self.max_step_speed, distance * 0.5)
        else:
            cmd_vel.linear.x = 0.0

        # Set angular velocity to turn toward target
        cmd_vel.angular.z = angle_diff * 0.5  # Proportional controller

        return cmd_vel

    def calculate_distance(self, pose1, pose2):
        """
        Calculate Euclidean distance between two poses
        """
        dx = pose2.position.x - pose1.position.x
        dy = pose2.position.y - pose1.position.y
        return np.sqrt(dx**2 + dy**2)

    def quaternion_to_yaw(self, quat):
        """
        Convert quaternion to yaw angle
        """
        siny_cosp = 2 * (quat.w * quat.z + quat.x * quat.y)
        cosy_cosp = 1 - 2 * (quat.y * quat.y + quat.z * quat.z)
        return np.arctan2(siny_cosp, cosy_cosp)

    def stop_robot(self):
        """
        Stop the robot
        """
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd_vel)
```

## Costmap Configuration for Bipedal Robots

The costmap needs to be configured for bipedal-specific navigation:

```yaml
# bipedal_costmap_params.yaml
local_costmap:
  global_frame: odom
  robot_base_frame: base_link
  update_frequency: 5.0
  publish_frequency: 2.0
  static_map: false
  rolling_window: true
  width: 6.0
  height: 6.0
  resolution: 0.05  # 5cm resolution for detailed footstep planning
  plugins:
    - {name: obstacles, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation, type: "nav2_costmap_2d::InflationLayer"}

  # Bipedal-specific obstacle layer configuration
  obstacles:
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0  # Bipedal robots can step over low obstacles
      obstacle_range: 3.0
      raytrace_range: 4.0
      clearing: true
      marking: true

  # Inflation layer for bipedal safety
  inflation:
    inflation_radius: 0.4  # Larger than wheeled robots for stability
    cost_scaling_factor: 3.0

global_costmap:
  global_frame: map
  robot_base_frame: base_link
  update_frequency: 1.0
  static_map: true
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacle_layer, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation, type: "nav2_costmap_2d::InflationLayer"}

  # Bipedal-specific configurations
  static_layer:
    map_topic: /map
    transform_tolerance: 0.5

  obstacle_layer:
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0
      obstacle_range: 3.0
      raytrace_range: 4.0
      clearing: true
      marking: true

  inflation:
    inflation_radius: 0.5  # Account for bipedal base support area
    cost_scaling_factor: 2.5
```

## Bipedal-Specific Controllers

For bipedal locomotion, special controllers are needed:

### Footstep Planner

```python
import numpy as np
from geometry_msgs.msg import Point

class FootstepPlanner:
    def __init__(self):
        self.step_length = 0.3  # meters
        self.step_width = 0.2   # meters
        self.step_height = 0.1  # meters for stepping over obstacles

    def plan_footsteps(self, path, robot_pose):
        """
        Plan footstep locations along a path
        """
        footsteps = []

        # Start with current stance foot position
        left_foot = self.calculate_initial_left_foot(robot_pose)
        right_foot = self.calculate_initial_right_foot(robot_pose)

        # Alternate steps along the path
        for i, path_point in enumerate(path):
            if i % 2 == 0:
                # Move left foot
                next_left = self.calculate_next_foot_position(left_foot, path_point, 'left')
                footsteps.append(('left', next_left))
                left_foot = next_left
            else:
                # Move right foot
                next_right = self.calculate_next_foot_position(right_foot, path_point, 'right')
                footsteps.append(('right', next_right))
                right_foot = next_right

        return footsteps

    def calculate_next_foot_position(self, current_foot, target_point, foot_type):
        """
        Calculate next foot position based on target
        """
        # Calculate direction to target
        dx = target_point.position.x - current_foot.x
        dy = target_point.position.y - current_foot.y
        distance = np.sqrt(dx**2 + dy**2)

        # Calculate next position along path
        step_distance = min(distance, self.step_length)
        next_x = current_foot.x + (dx / distance) * step_distance if distance > 0 else current_foot.x
        next_y = current_foot.y + (dy / distance) * step_distance if distance > 0 else current_foot.y

        # Apply foot offset based on foot type
        if foot_type == 'left':
            # Offset to the left relative to robot heading
            offset_x = -self.step_width / 2
            offset_y = self.step_width / 2
        else:  # right foot
            offset_x = -self.step_width / 2
            offset_y = -self.step_width / 2

        return Point(x=next_x + offset_x, y=next_y + offset_y, z=current_foot.z)
```

### Balance Controller

```python
import numpy as np

class BalanceController:
    def __init__(self):
        self.zmp_reference = np.array([0.0, 0.0])  # Zero Moment Point reference
        self.com_height = 0.8  # Center of Mass height in meters
        self.gravity = 9.81

        # PID controller parameters
        self.kp = 10.0  # Proportional gain
        self.ki = 1.0   # Integral gain
        self.kd = 2.0   # Derivative gain

        self.error_integral = np.array([0.0, 0.0])
        self.previous_error = np.array([0.0, 0.0])

    def compute_balance_control(self, current_zmp, current_com, dt):
        """
        Compute balance control commands
        """
        # Calculate error
        error = self.zmp_reference - current_zmp

        # Update integral
        self.error_integral += error * dt

        # Calculate derivative
        if dt > 0:
            error_derivative = (error - self.previous_error) / dt
        else:
            error_derivative = np.array([0.0, 0.0])

        # PID control
        control_output = (self.kp * error +
                         self.ki * self.error_integral +
                         self.kd * error_derivative)

        # Update for next iteration
        self.previous_error = error

        return control_output

    def compute_com_trajectory(self, goal_position, current_com, dt):
        """
        Compute Center of Mass trajectory for balance
        """
        # Simple trajectory generation using 3rd order polynomial
        # This ensures smooth motion while maintaining balance

        # Calculate desired CoM position based on ZMP and balance
        desired_com_x = goal_position[0] + (self.com_height / self.gravity) * self.compute_balance_control(
            np.array([current_com[0], current_com[1]]),
            current_com,
            dt
        )[0]

        desired_com_y = goal_position[1] + (self.com_height / self.gravity) * self.compute_balance_control(
            np.array([current_com[0], current_com[1]]),
            current_com,
            dt
        )[1]

        return np.array([desired_com_x, desired_com_y, self.com_height])
```

## Integration with Isaac ROS

Integrating Nav2 with Isaac ROS provides enhanced capabilities:

### Isaac ROS Navigation Components

```python
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
import time

class IsaacROSBipedalNavigator(Node):
    def __init__(self):
        super().__init__('isaac_ros_bipedal_navigator')

        # Create action client for navigation
        self.nav_to_pose_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Isaac ROS specific components
        self.setup_isaac_ros_components()

    def setup_isaac_ros_components(self):
        """
        Setup Isaac ROS specific navigation components
        """
        # This would include Isaac ROS perception and control nodes
        # for enhanced navigation capabilities
        pass

    def navigate_to_pose(self, x, y, z, ox, oy, oz, ow):
        """
        Navigate to a specific pose
        """
        # Wait for action server
        self.nav_to_pose_client.wait_for_server()

        # Create goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = z
        goal_msg.pose.pose.orientation.x = ox
        goal_msg.pose.pose.orientation.y = oy
        goal_msg.pose.pose.orientation.z = oz
        goal_msg.pose.pose.orientation.w = ow

        # Send goal
        future = self.nav_to_pose_client.send_goal_async(goal_msg)
        return future
```

## Practical Exercise

Configure Nav2 for a bipedal robot by:

1. Creating a custom costmap configuration for bipedal navigation
2. Implementing a footstep planner for legged locomotion
3. Creating a balance controller for stable walking
4. Testing the navigation system in simulation

## Summary

In this section, we covered:

- Nav2 architecture and components
- Adapting global and local planners for bipedal robots
- Configuring costmaps for legged navigation
- Implementing footstep planners and balance controllers
- Integrating with Isaac ROS for enhanced capabilities

Nav2 provides a robust foundation for bipedal robot navigation when properly configured for the unique challenges of legged locomotion.