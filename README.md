# Physical AI & Humanoid Robotics Educational Platform

A comprehensive educational platform for learning about Physical AI and Humanoid Robotics, combining both frontend educational content and backend APIs.

## Overview

This project provides a complete educational experience on Physical AI and Humanoid Robotics, covering topics from ROS 2 and simulation environments to AI-robot interaction and vision-language-action systems.

## Project Structure

This project follows a microservices architecture with separate frontend and backend components:

### Frontend (`/frontend/website`)
- Built with Docusaurus v3
- Educational content in Markdown/MDX format
- Interactive components for learning
- Responsive design
- Deployed to GitHub Pages

### Backend (`/backend`)
- RESTful API built with Express.js
- Provides course content APIs
- Search functionality
- Modular architecture supporting all course modules

## Features

- **Module 1**: The Robotic Nervous System (ROS 2) - Nodes, Topics, Services, rclpy, URDF
- **Module 2**: The Digital Twin (Gazebo & Unity) - Simulation, Physics, Sensors
- **Module 3**: The AI-Robot Brain (NVIDIA Isaac™) - Isaac Sim, VSLAM, Nav2
- **Module 4**: Vision-Language-Action (VLA) - Voice commands, LLMs, Capstone Project

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Running the Frontend

1. Navigate to the frontend website directory:
```bash
cd frontend/website
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run start
```

### Running the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

## Development

### Frontend Development
- Content is written in Markdown/MDX format in the `docs/` directory
- Custom components are in the `src/components/` directory
- Styling is handled in `src/css/custom.css`

### Backend Development
- API endpoints are defined in `index.js`
- Environment variables are configured in `.env`
- API documentation is available at the root endpoint

## Deployment

### Frontend Deployment
The frontend is configured for GitHub Pages deployment:
```bash
cd frontend/website
npm run deploy
```

### Backend Deployment
The backend can be deployed to any Node.js hosting service (Heroku, AWS, etc.)

## Technologies Used

### Frontend
- Docusaurus v3
- React
- TypeScript
- MDX
- Mermaid
- ESLint/Prettier

### Backend
- Express.js
- Node.js
- CORS
- Dotenv

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.