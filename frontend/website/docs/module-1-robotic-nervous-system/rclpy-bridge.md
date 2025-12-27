---
sidebar_position: 3
title: Bridging Python Agents with rclpy
---

# Bridging Python Agents with rclpy

In this section, we'll explore how to bridge Python agents with ROS 2 using rclpy, the Python client library for ROS 2. This allows Python-based AI agents to communicate with the robotic system.

## Learning Objectives

By the end of this section, you will be able to:

- Use rclpy to create ROS 2 nodes in Python
- Bridge Python AI agents with ROS 2 communication
- Implement Python-based controllers for robotic systems
- Integrate Python-based machine learning models with ROS 2

## Introduction to rclpy

rclpy is the Python client library for ROS 2. It provides a Python API for ROS 2 concepts such as nodes, publishers, subscribers, services, and parameters.

### Installing rclpy

rclpy is typically installed as part of a ROS 2 installation. You can install ROS 2 with Python support following the official ROS 2 installation guide.

### Basic rclpy Node Structure

```python
import rclpy
from rclpy.node import Node

class PythonAgentNode(Node):
    def __init__(self):
        super().__init__('python_agent_node')
        self.get_logger().info('Python Agent Node initialized')

def main(args=None):
    rclpy.init(args=args)
    python_agent_node = PythonAgentNode()

    try:
        rclpy.spin(python_agent_node)
    except KeyboardInterrupt:
        pass
    finally:
        python_agent_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Creating Publishers and Subscribers with rclpy

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class AgentPublisher(Node):
    def __init__(self):
        super().__init__('agent_publisher')
        self.publisher_ = self.create_publisher(String, 'agent_commands', 10)
        self.timer = self.create_timer(1.0, self.publish_command)

    def publish_command(self):
        msg = String()
        msg.data = f'Command from Python agent at {time.time()}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    agent_publisher = AgentPublisher()

    try:
        rclpy.spin(agent_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        agent_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AgentSubscriber(Node):
    def __init__(self):
        super().__init__('agent_subscriber')
        self.subscription = self.create_subscription(
            String,
            'robot_feedback',
            self.feedback_callback,
            10)
        self.subscription  # prevent unused variable warning

    def feedback_callback(self, msg):
        self.get_logger().info(f'Received feedback: {msg.data}')
        # Process the feedback in the Python agent
        self.process_feedback(msg.data)

    def process_feedback(self, feedback):
        # Implement Python-based processing logic
        self.get_logger().info(f'Processing feedback: {feedback}')

def main(args=None):
    rclpy.init(args=args)
    agent_subscriber = AgentSubscriber()

    try:
        rclpy.spin(agent_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        agent_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Integrating AI Agents with ROS 2

### Example: Python-based Decision Making Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
from geometry_msgs.msg import Twist
import numpy as np

class AIAgentNode(Node):
    def __init__(self):
        super().__init__('ai_agent_node')

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscribers
        self.sensor_subscriber = self.create_subscription(
            Float64MultiArray,
            'sensor_data',
            self.sensor_callback,
            10)

        # Timer for decision making
        self.timer = self.create_timer(0.1, self.make_decision)

        # Internal state
        self.sensor_data = None
        self.get_logger().info('AI Agent Node initialized')

    def sensor_callback(self, msg):
        self.sensor_data = np.array(msg.data)
        self.get_logger().info(f'Received sensor data: {self.sensor_data}')

    def make_decision(self):
        if self.sensor_data is not None:
            # Simple AI decision making
            cmd_vel = Twist()

            # Example: Move forward if clear path, turn if obstacle detected
            if self.sensor_data[0] > 1.0:  # If no obstacle ahead
                cmd_vel.linear.x = 0.5
                cmd_vel.angular.z = 0.0
            else:  # If obstacle detected
                cmd_vel.linear.x = 0.0
                cmd_vel.angular.z = 0.5  # Turn right

            self.cmd_vel_publisher.publish(cmd_vel)
            self.get_logger().info(f'Published command: linear={cmd_vel.linear.x}, angular={cmd_vel.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    ai_agent_node = AIAgentNode()

    try:
        rclpy.spin(ai_agent_node)
    except KeyboardInterrupt:
        pass
    finally:
        ai_agent_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Practical Exercise

Create a Python-based agent that receives sensor data from a simulated robot and makes decisions about navigation based on that data.

## Summary

In this section, we learned how to bridge Python agents with ROS 2 using rclpy:

- Basic rclpy node structure and patterns
- Creating publishers and subscribers in Python
- Integrating AI agents with robotic systems
- Implementing decision-making logic in Python that interacts with ROS 2

This bridge enables the integration of sophisticated Python-based AI algorithms with robotic systems, forming the foundation for intelligent robotic behavior.