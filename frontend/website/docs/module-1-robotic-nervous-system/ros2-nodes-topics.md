---
sidebar_position: 2
title: ROS 2 Nodes, Topics, and Services
---

# ROS 2 Nodes, Topics, and Services

In this section, we'll explore the fundamental communication mechanisms in ROS 2: nodes, topics, and services. These components form the backbone of robotic communication and enable different parts of a robot to interact with each other.

## Learning Objectives

By the end of this section, you will be able to:

- Create and run ROS 2 nodes
- Understand the publisher-subscriber pattern using topics
- Implement request-response patterns using services
- Use ROS 2 command-line tools for monitoring communication

## Nodes

A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 program. Each node contains the code for a specific task or function within the robotic system.

### Creating a Node

Here's a basic example of a ROS 2 node:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Hello from minimal node!')

def main(args=None):
    rclpy.init(args=args)
    minimal_node = MinimalNode()

    minimal_node.get_logger().info('Spinning node...')
    rclpy.spin(minimal_node)

    minimal_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Topics and Publisher-Subscriber Pattern

Topics enable asynchronous communication between nodes using a publish-subscribe model. Publishers send messages to topics, and subscribers receive messages from topics.

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.get_clock().now().nanoseconds
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Services

Services provide synchronous request-response communication between nodes. A service client sends a request to a service server, which processes the request and returns a response.

### Service Server Example

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Practical Exercise

Create a simple ROS 2 package with a publisher and subscriber that communicate about the state of a humanoid robot's joints.

## Summary

In this section, we covered the fundamental communication mechanisms in ROS 2:

- Nodes: The basic executable units of a ROS 2 program
- Topics: Asynchronous communication using publish-subscribe pattern
- Services: Synchronous communication using request-response pattern

These concepts form the foundation for building complex robotic systems that can coordinate multiple components effectively.