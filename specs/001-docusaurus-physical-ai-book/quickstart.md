# Quickstart: Physical AI & Humanoid Robotics Book

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- GitHub account for deployment

## Setup Instructions

1. **Clone or create the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run start
   # or
   yarn start
   ```
   This will start a local development server at http://localhost:3000

4. **Create your first content page**
   - Add a new `.md` or `.mdx` file in the `docs/` directory
   - Use frontmatter to define metadata:
     ```markdown
     ---
     title: Your Page Title
     description: Brief description of the page content
     ---
     ```

5. **Build for production**
   ```bash
   npm run build
   # or
   yarn build
   ```

6. **Deploy to GitHub Pages**
   ```bash
   npm run deploy
   # or
   yarn deploy
   ```

## Key Features

- **Interactive Code Blocks**: Use standard Markdown code blocks with syntax highlighting
- **Mermaid Diagrams**: Add diagrams using Mermaid syntax
- **MDX Components**: Embed React components directly in your content
- **Responsive Design**: Works on mobile and desktop devices
- **Search Functionality**: Built-in search across all content
- **Version Control**: All content is tracked with Git

## Content Organization

- **Module Structure**: Content is organized in the `docs/` directory by modules
- **Navigation**: Sidebar navigation is defined in `sidebars.js`
- **Styling**: Custom CSS can be added in `src/css/custom.css`
- **Assets**: Images and other static files go in the `static/` directory

## Development Workflow

1. Create/edit content in the `docs/` directory
2. Add/update sidebar navigation in `sidebars.js`
3. Test changes with `npm run start`
4. Commit changes with descriptive commit messages
5. Push to GitHub to trigger deployment