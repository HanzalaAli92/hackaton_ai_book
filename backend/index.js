const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Basic route
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to the Physical AI & Humanoid Robotics Backend API',
    version: '1.0.0',
    endpoints: {
      'GET /api/modules': 'Get all course modules',
      'GET /api/modules/:id': 'Get specific module',
      'GET /api/pages': 'Get all pages',
      'GET /api/pages/:id': 'Get specific page',
      'GET /api/search': 'Search across course content'
    }
  });
});

// API routes placeholder
app.get('/api/modules', (req, res) => {
  res.json([
    {
      id: 'module-1',
      title: 'The Robotic Nervous System (ROS 2)',
      description: 'Introduction to ROS 2 Nodes/Topics/Services, bridging Python agents with rclpy, URDF for humanoids',
      order: 1,
      pageCount: 4,
      duration: '2 weeks'
    }
  ]);
});

app.get('/api/modules/:id', (req, res) => {
  const moduleId = req.params.id;
  res.json({
    id: moduleId,
    title: 'Module Details',
    content: 'This is where module-specific content would be returned',
    pages: []
  });
});

app.get('/api/pages', (req, res) => {
  res.json([
    {
      id: 'page-1',
      title: 'Introduction to ROS 2',
      moduleId: 'module-1',
      order: 1,
      type: 'content',
      path: '/module-1/ros2-intro'
    }
  ]);
});

app.get('/api/pages/:id', (req, res) => {
  const pageId = req.params.id;
  res.json({
    id: pageId,
    title: 'Page Details',
    content: 'This is where specific page content would be returned',
    module: 'module-1'
  });
});

app.get('/api/search', (req, res) => {
  const { query, limit = 10 } = req.query;
  res.json({
    query: query || '',
    limit: parseInt(limit),
    results: []
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(PORT, () => {
  console.log(`Physical AI & Humanoid Robotics Backend server is running on port ${PORT}`);
  console.log(`API documentation available at http://localhost:${PORT}/`);
});