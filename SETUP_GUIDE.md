# Script to Film Platform - Complete Setup Guide

## Overview

This guide will walk you through setting up the complete Script to Film platform, including both the backend API and frontend web interface.

## What You'll Build

A complete AI-powered filmmaking assistant that:
1. Generates scripts from simple prompts
2. Analyzes scripts into structured scenes
3. Creates text-to-video prompts for each scene
4. Allows easy export for use with video generation services

## Architecture

```
┌─────────────────┐
│  React Frontend │  ← User Interface (Port 3000)
│   (TypeScript)  │
└────────┬────────┘
         │
         │ REST API
         │
┌────────▼────────┐
│  FastAPI Backend│  ← Python API (Port 8000)
│   + AI Services │
└─────────────────┘
```

## Step 1: Backend Setup

### 1.1 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### 1.2 Install Dependencies

```bash
# From the project root
cd /Users/alanballesterossandoval/script-to-film-platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# For now, you can use placeholder values for API keys
nano .env  # or use your preferred editor
```

Minimum required configuration:
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# For MVP, these can be placeholder values
OPENAI_API_KEY=sk-placeholder
ANTHROPIC_API_KEY=sk-placeholder
SECRET_KEY=your-secret-key-here

# Database (optional for now)
DATABASE_URL=sqlite:///./test.db
REDIS_URL=redis://localhost:6379/0
```

### 1.4 Start the Backend

```bash
# From the project root with venv activated
python -m uvicorn script_to_film.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test the API:**
- Open http://localhost:8000/docs in your browser
- You should see the interactive API documentation

## Step 2: Frontend Setup

### 2.1 Prerequisites

- Node.js 18+ (check with `node --version`)
- npm (comes with Node.js)

### 2.2 Install Dependencies

Open a **new terminal window** (keep the backend running):

```bash
# Navigate to frontend directory
cd /Users/alanballesterossandoval/script-to-film-platform/frontend

# Install dependencies
npm install
```

### 2.3 Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# The default configuration should work:
# VITE_API_URL=http://localhost:8000/api/v1
```

### 2.4 Start the Frontend

```bash
# From the frontend directory
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Open the application:**
- Navigate to http://localhost:3000 in your browser

## Step 3: Using the Platform

### 3.1 Generate Your First Script

1. Open http://localhost:3000
2. In the "Script Idea / Prompt" field, enter something like:
   ```
   A touching story about a programmer who discovers an old friend
   at a coffee shop and they reminisce about their college days
   ```
3. Optionally set:
   - Genre: "Drama"
   - Tone: "Nostalgic"
   - Duration: 90 seconds
4. Click "Generate Script"
5. Wait 2-3 seconds for the AI to generate your script

### 3.2 Review and Analyze

1. Review the generated script in the display
2. Click "Copy" to copy the script to clipboard
3. Click "Download" to save it as a text file
4. Click "Analyze & Generate Scene Prompts" to continue

### 3.3 View Scene Breakdown

You'll see each scene broken down with:
- Scene number and location
- Time of day (with icons)
- Action description
- Character dialogue
- Estimated duration

### 3.4 Get Text-to-Video Prompts

1. Click "Continue to Video Prompts"
2. View optimized prompts for each scene
3. Click "Copy Prompt" on any scene to copy it
4. Click "Edit" to refine a prompt
5. Click "Export All" to download all prompts

### 3.5 Create Your Video

Use the prompts with any text-to-video service:

**RunwayML Gen-2:**
1. Go to https://runwayml.com
2. Select Gen-2
3. Paste each scene prompt
4. Generate videos for each scene

**Pika Labs:**
1. Join Pika Discord
2. Use `/create` command
3. Paste your prompts

**Stable Video Diffusion:**
1. Use the Stability AI API
2. Send prompts programmatically

## Step 4: Development Workflow

### 4.1 Making Changes

**Backend Changes:**
- Edit files in `src/script_to_film/`
- The server will auto-reload (with `--reload` flag)
- Check http://localhost:8000/docs for API changes

**Frontend Changes:**
- Edit files in `frontend/src/`
- Vite will hot-reload automatically
- See changes instantly in the browser

### 4.2 Project Structure

```
Backend:
- src/script_to_film/api/routes.py      # API endpoints
- src/script_to_film/services/          # Business logic
- src/script_to_film/models/            # Data models

Frontend:
- frontend/src/components/              # React components
- frontend/src/services/api.ts          # API integration
- frontend/src/types/                   # TypeScript types
```

### 4.3 Common Tasks

**Add a new API endpoint:**
1. Edit `src/script_to_film/api/routes.py`
2. Add your endpoint function
3. Test at http://localhost:8000/docs

**Add a new UI component:**
1. Create file in `frontend/src/components/`
2. Import and use in `App.tsx`
3. View changes at http://localhost:3000

## Step 5: Integrating Real AI Services

### 5.1 OpenAI Integration (Script Generation)

1. Get an API key from https://platform.openai.com
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-your-real-key-here
   ```
3. Update `src/script_to_film/services/ai_service.py`:
   ```python
   import openai

   async def generate_script(self, prompt: str, ...):
       response = await openai.ChatCompletion.acreate(
           model="gpt-4",
           messages=[
               {"role": "system", "content": "You are a screenwriter..."},
               {"role": "user", "content": prompt}
           ]
       )
       return response.choices[0].message.content
   ```

### 5.2 Anthropic Claude Integration (Alternative)

```python
import anthropic

async def generate_script(self, prompt: str, ...):
    client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
    message = await client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

## Troubleshooting

### Backend won't start

**Error: "No module named 'script_to_film'"**
- Make sure you're in the project root
- Activate the virtual environment
- Run `pip install -e .`

**Error: "Address already in use"**
- Another process is using port 8000
- Kill it: `lsof -ti:8000 | xargs kill -9`
- Or use a different port: `--port 8001`

### Frontend won't start

**Error: "Cannot find module"**
- Run `npm install` again
- Delete `node_modules` and `package-lock.json`, then reinstall

**Error: "CORS error"**
- Make sure backend is running
- Check that `VITE_API_URL` in `.env` is correct
- Backend should allow CORS (already configured)

### API calls failing

**Check:**
1. Backend is running (http://localhost:8000/health)
2. Frontend `.env` has correct API URL
3. Browser console for error messages
4. Backend terminal for error logs

## Next Steps

### Production Deployment

1. **Database**: Set up PostgreSQL for production
2. **Authentication**: Add user accounts and JWT tokens
3. **Storage**: Configure S3 for storing generated content
4. **AI Services**: Add real API keys for OpenAI/Anthropic
5. **Video Processing**: Integrate with video generation APIs
6. **Hosting**: Deploy backend to Railway/Render, frontend to Vercel

### Feature Enhancements

- [ ] User authentication and project management
- [ ] Save and load scripts from database
- [ ] Real-time progress updates with WebSockets
- [ ] Video preview and editing
- [ ] Multiple visual styles (realistic, animated, etc.)
- [ ] Audio generation for dialogue
- [ ] Music generation for scenes
- [ ] Automated video composition

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Vite Docs**: https://vitejs.dev
- **OpenAI API**: https://platform.openai.com/docs
- **Anthropic API**: https://docs.anthropic.com

## Support

For issues and questions:
1. Check the logs in both terminal windows
2. Review the API documentation at http://localhost:8000/docs
3. Open an issue on GitHub (when repository is created)

---

**Congratulations!** You now have a fully functional Script to Film platform. Start creating amazing short films with AI! 🎬
