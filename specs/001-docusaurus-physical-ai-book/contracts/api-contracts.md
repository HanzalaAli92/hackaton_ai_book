# API Contracts: Physical AI & Humanoid Robotics Book

## Content API

### Get Course Modules
- **Endpoint**: `GET /api/modules`
- **Description**: Retrieve all course modules with basic information
- **Response**:
  ```json
  {
    "modules": [
      {
        "id": "module-1",
        "title": "The Robotic Nervous System (ROS 2)",
        "description": "Introduction to ROS 2 Nodes/Topics/Services, bridging Python agents with rclpy, URDF for humanoids",
        "order": 1,
        "pageCount": 4,
        "duration": "2 weeks"
      }
    ]
  }
  ```

### Get Module Pages
- **Endpoint**: `GET /api/modules/{moduleId}/pages`
- **Description**: Retrieve all pages within a specific module
- **Parameters**:
  - `moduleId`: string (the module identifier)
- **Response**:
  ```json
  {
    "pages": [
      {
        "id": "ros2-nodes-topics",
        "title": "ROS 2 Nodes, Topics, and Services",
        "module": "module-1",
        "order": 1,
        "type": "content",
        "path": "/module-1/ros2-nodes-topics"
      }
    ]
  }
  ```

### Get Page Content
- **Endpoint**: `GET /api/pages/{pageId}`
- **Description**: Retrieve specific page content and metadata
- **Parameters**:
  - `pageId`: string (the page identifier)
- **Response**:
  ```json
  {
    "id": "ros2-nodes-topics",
    "title": "ROS 2 Nodes, Topics, and Services",
    "content": "Markdown content with embedded components...",
    "module": "module-1",
    "learningObjectives": [
      "Understand ROS 2 node architecture",
      "Learn to create topics and services",
      "Implement basic communication patterns"
    ],
    "relatedPages": [
      "rclpy-bridge",
      "urdf-humanoids"
    ]
  }
  }
  ```

## Search API

### Search Content
- **Endpoint**: `GET /api/search`
- **Description**: Search across all course content
- **Parameters**:
  - `query`: string (search term)
  - `limit`: number (optional, default 10)
- **Response**:
  ```json
  {
    "results": [
      {
        "id": "search-result-id",
        "title": "Page Title",
        "path": "/path/to/page",
        "preview": "Content preview with highlighted matches...",
        "relevance": 0.95
      }
    ]
  }
  }
  ```