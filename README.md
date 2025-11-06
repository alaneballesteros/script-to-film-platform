# Script to Film Platform

AI-powered platform for converting script ideas into short films through an intuitive web interface.

## Workflow

1. **Prompt to Script**: User enters a script idea, AI generates a complete screenplay
2. **Scene Analysis**: Script is automatically parsed into individual scenes
3. **Text-to-Video Prompts**: AI generates optimized prompts for each scene
4. **Video Creation**: Use prompts with any text-to-video service (RunwayML, Pika, Stable Video, etc.)

## Features

- **AI Script Generation**: Transform ideas into properly formatted screenplays
- **Automatic Scene Breakdown**: Parse scripts into structured scenes with metadata
- **Video Prompt Generation**: Create optimized text-to-video prompts for each scene
- **Modern Web UI**: Intuitive React-based interface with real-time updates
- **RESTful API**: Full backend API for integration and automation
- **Export & Copy**: Easy export and copying of scripts and prompts

## Project Structure

```
script-to-film-platform/
├── frontend/                  # React web application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API integration
│   │   ├── types/            # TypeScript types
│   │   └── styles/           # CSS and styling
│   ├── package.json
│   └── vite.config.ts
├── src/
│   └── script_to_film/       # Python backend
│       ├── api/              # API routes and endpoints
│       ├── services/         # Business logic (AI, parsing, video)
│       ├── models/           # Data models and schemas
│       ├── config/           # Configuration management
│       ├── utils/            # Utility functions
│       └── main.py           # Application entry point
├── tests/
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── data/
│   ├── scripts/              # Input scripts
│   ├── output/               # Generated content
│   └── temp/                 # Temporary files
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Prerequisites

### Backend
- Python 3.10 or higher
- PostgreSQL (optional - for production)
- Redis (optional - for task queue)

### Frontend
- Node.js 18+ and npm

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd script-to-film-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Start the backend server:
```bash
python -m uvicorn script_to_film.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# The default configuration points to http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The web application will be available at `http://localhost:3000`

### Quick Start with Make

From the root directory:
```bash
# Backend
make install   # Install Python dependencies
make run       # Start the API server

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

## Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Enter your script idea in the prompt field
3. Click "Generate Script" and wait for AI to create your screenplay
4. Review the generated script
5. Click "Analyze & Generate Scene Prompts"
6. View the scene breakdown with all metadata
7. Continue to see text-to-video prompts for each scene
8. Copy prompts and use them with your preferred text-to-video service

### Supported Text-to-Video Services

- **RunwayML Gen-2**: High-quality video generation
- **Pika Labs**: Creative AI video generation
- **Stable Video Diffusion**: Open-source video generation
- **Any text-to-video API**: Use the exported prompts

### API Endpoints

#### Scripts

- `POST /api/v1/scripts/generate` - Generate a script from a prompt using AI
- `POST /api/v1/scripts` - Create/parse an existing script
- `GET /api/v1/scripts` - List all scripts
- `GET /api/v1/scripts/{script_id}` - Get a specific script
- `POST /api/v1/scripts/{script_id}/video-prompts` - Generate video prompts for scenes

#### Videos

- `POST /api/v1/videos` - Generate a video from a script (future)
- `GET /api/v1/videos` - List all videos
- `GET /api/v1/videos/{video_id}` - Get a specific video

### Example: Generate a Script from a Prompt

```bash
curl -X POST "http://localhost:8000/api/v1/scripts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A heartwarming story about two old friends reuniting",
    "genre": "Drama",
    "tone": "Uplifting",
    "duration_preference": 90
  }'
```

### Example: Parse an Existing Script

```bash
curl -X POST "http://localhost:8000/api/v1/scripts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Short Film",
    "author": "John Doe",
    "content": "INT. COFFEE SHOP - DAY\n\nA young woman sits alone..."
  }'
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
ruff check src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Architecture

### Services

- **ScriptParser**: Parses raw script text into structured scenes
- **AIService**: Interfaces with AI models for content generation
- **VideoGenerator**: Orchestrates video creation from scripts

### Models

- **Script**: Represents a screenplay with scenes and metadata
- **Video**: Represents a generated video with status tracking
- **ScriptScene**: Individual scene within a script
- **VideoScene**: Individual scene in a video with visual/audio paths

## Configuration

Key configuration options in `.env`:

- `OPENAI_API_KEY`: OpenAI API key for GPT and DALL-E
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `AWS_*`: AWS credentials for S3 storage

## Roadmap

- [ ] Complete AI model integration (DALL-E, Stable Diffusion)
- [ ] Implement video generation pipeline
- [ ] Add text-to-speech for dialogue
- [ ] Implement background music generation
- [ ] Add user authentication and authorization
- [ ] Create web interface
- [ ] Add progress tracking for long-running tasks
- [ ] Implement caching for generated assets
- [ ] Add support for different video styles
- [ ] Create comprehensive test suite

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on the GitHub repository.
