# Physical AI & Humanoid Robotics - Frontend

This is the frontend Docusaurus website for the Physical AI & Humanoid Robotics educational platform.

## Overview

The frontend is built with Docusaurus v3 and provides an educational platform for learning about Physical AI and Humanoid Robotics. It includes modules on ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems.

## Features

- Educational content organized in 4 main modules:
  - The Robotic Nervous System (ROS 2)
  - The Digital Twin (Gazebo & Unity)
  - The AI-Robot Brain (NVIDIA Isaac™)
  - Vision-Language-Action (VLA)
- Interactive code blocks with syntax highlighting
- Mermaid diagrams for visualizing concepts
- Custom React components for enhanced learning
- Responsive design for desktop and mobile
- GitHub Pages deployment ready

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Navigate to the website directory
2. Install dependencies:

```bash
cd website
npm install
```

### Local Development

```bash
cd website
npm run start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
cd website
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

The site is configured for deployment to GitHub Pages. Use the following command:

```bash
cd website
npm run deploy
```

Or set up GitHub Actions workflow as defined in `.github/workflows/deploy.yml`.

## Technologies Used

- Docusaurus v3
- TypeScript
- React
- MDX
- Mermaid for diagrams
- ESLint and Prettier for code quality

## Project Structure

- `/docs`: Course content organized by modules
  - `/module-1-robotic-nervous-system`: ROS 2 content
  - `/module-2-digital-twin`: Gazebo and Unity content
  - `/module-3-ai-robot-brain`: NVIDIA Isaac content
  - `/module-4-vision-language-action`: VLA and capstone content
- `/src/components`: Custom React components
  - `/InteractiveCodeBlock`: Enhanced code blocks
  - `/MermaidDiagram`: Diagram rendering
  - `/SimulationViewer`: Simulation components
- `/src/css`: Custom CSS styling
- `/static`: Static assets like images
