# Script to Film - Frontend

Modern React-based UI for the Script to Film platform.

## Features

- **Script Generation**: AI-powered script creation from simple prompts
- **Scene Analysis**: Automatic breakdown of scripts into individual scenes
- **Video Prompts**: Generate text-to-video prompts for each scene
- **Copy & Export**: Easy copying and exporting of prompts for video generation services

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Icons
- Axios

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

## Usage

### 1. Generate Script
- Enter your script idea in the prompt field
- Optionally specify genre, tone, and target duration
- Click "Generate Script" to create a screenplay

### 2. Review Script
- Review the generated script
- Copy or download if needed
- Click "Analyze & Generate Scene Prompts"

### 3. Scene Breakdown
- View the parsed scenes with locations, timing, and dialogue
- Each scene shows duration and other metadata

### 4. Video Prompts
- Copy individual prompts for each scene
- Edit prompts to refine them
- Export all prompts at once
- Use with services like:
  - RunwayML Gen-2
  - Pika Labs
  - Stable Video Diffusion
  - Any text-to-video service

## Project Structure

```
frontend/
├── src/
│   ├── components/        # React components
│   │   ├── Header.tsx
│   │   ├── ScriptGenerator.tsx
│   │   ├── ScriptDisplay.tsx
│   │   ├── SceneBreakdown.tsx
│   │   └── VideoPrompts.tsx
│   ├── services/          # API services
│   │   └── api.ts
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   ├── styles/            # Global styles
│   │   └── index.css
│   ├── App.tsx            # Main app component
│   └── main.tsx           # Entry point
├── public/                # Static assets
└── index.html             # HTML template
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Integration with Backend

The frontend expects the backend API to be running at `http://localhost:8000` by default. You can change this in the `.env` file:

```
VITE_API_URL=http://your-api-url/api/v1
```

## Contributing

Contributions are welcome! Please follow the existing code style and add tests for new features.

## License

MIT
