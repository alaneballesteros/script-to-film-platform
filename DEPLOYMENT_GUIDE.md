# Deployment Guide - Script to Film Platform

This guide will help you deploy your application to a live domain so you and your friend can access it from anywhere.

## Recommended Deployment Stack

We'll use this free/low-cost stack:

| Component | Service | Why |
|-----------|---------|-----|
| **Backend** | Railway or Render | Free tier, easy Python deployment |
| **Frontend** | Vercel or Netlify | Free tier, automatic deployments from GitHub |
| **Database** | PostgreSQL on Railway/Render | Free tier included |
| **Domain** | Vercel/Netlify subdomain (free) | Or custom domain ($12/year) |

## Option 1: Recommended Setup (Easiest)

### Backend: Railway
### Frontend: Vercel

This is the **easiest and fastest** option with automatic deployments from GitHub.

---

## 🚀 Quick Start - Deploy in 15 Minutes

### A. Deploy Backend to Railway

#### 1. Sign Up for Railway

1. Go to: https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub
4. Authorize Railway

#### 2. Deploy Backend

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `alaneballesteros/script-to-film-platform`
4. Railway will detect it's a Python project

#### 3. Configure Backend

1. Click on your deployment
2. Go to "Variables" tab
3. Add these environment variables:

```env
API_HOST=0.0.0.0
API_PORT=$PORT
API_ENV=production
DEBUG=false

# Database (Railway will auto-provision PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# AI Services (use your actual keys)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
RUNWAY_API_KEY=your_runway_key

# Security
SECRET_KEY=generate-a-long-random-string-here

# Application Settings
MAX_SCRIPT_LENGTH=10000
MAX_VIDEO_DURATION=300
```

#### 4. Add PostgreSQL Database

1. In your project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically link it
4. The `DATABASE_URL` will be available as `${{Postgres.DATABASE_URL}}`

#### 5. Configure Start Command

1. Go to "Settings" tab
2. Scroll to "Deploy" section
3. Set "Custom Start Command":
   ```
   python -m uvicorn script_to_film.main:app --host 0.0.0.0 --port $PORT
   ```

#### 6. Get Your Backend URL

1. Go to "Settings" → "Networking"
2. Click "Generate Domain"
3. You'll get something like: `https://your-app.up.railway.app`
4. **Save this URL** - you'll need it for the frontend!

---

### B. Deploy Frontend to Vercel

#### 1. Sign Up for Vercel

1. Go to: https://vercel.com
2. Click "Sign Up"
3. Sign in with GitHub
4. Authorize Vercel

#### 2. Deploy Frontend

1. Click "Add New Project"
2. Import `alaneballesteros/script-to-film-platform`
3. Configure settings:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

#### 3. Add Environment Variables

Before deploying, add:

```env
VITE_API_URL=https://your-app.up.railway.app/api/v1
```

Replace `your-app.up.railway.app` with your Railway backend URL!

#### 4. Deploy

1. Click "Deploy"
2. Wait 2-3 minutes
3. You'll get a URL like: `https://script-to-film-platform.vercel.app`

#### 5. Update Backend CORS

Your backend needs to allow requests from your Vercel domain:

**Edit `src/script_to_film/main.py`:**

```python
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://script-to-film-platform.vercel.app",  # Add your Vercel URL
        "http://localhost:3001",  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push this change - Railway will auto-deploy!

---

## 🎯 Your Live Application

After deployment:

- **Frontend:** `https://script-to-film-platform.vercel.app`
- **Backend API:** `https://your-app.up.railway.app`
- **API Docs:** `https://your-app.up.railway.app/docs`

Both you and your friend can access these URLs from anywhere!

---

## 🔄 Automatic Deployments

### How It Works

Once set up, deployments are **automatic**:

1. **You or your friend** make changes locally
2. Create a Pull Request on GitHub
3. Merge to `main` branch
4. **Railway** auto-deploys backend (2-3 minutes)
5. **Vercel** auto-deploys frontend (1-2 minutes)
6. Changes are **live** automatically!

### Preview Deployments

**Vercel** creates preview URLs for every PR:
- Each PR gets its own URL
- Test changes before merging
- Example: `https://script-to-film-platform-pr123.vercel.app`

---

## Option 2: Alternative - All on Render

If you prefer one service for everything:

### Deploy to Render

1. Go to: https://render.com
2. Sign in with GitHub
3. Click "New +"

#### Deploy Backend

1. Select "Web Service"
2. Connect `script-to-film-platform` repo
3. Settings:
   - **Name:** `script-to-film-api`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && pip install -e .`
   - **Start Command:** `python -m uvicorn script_to_film.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. Add environment variables (same as Railway above)

#### Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect same repo
3. Settings:
   - **Name:** `script-to-film-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `frontend/dist`

4. Add environment variable:
   ```
   VITE_API_URL=https://script-to-film-api.onrender.com/api/v1
   ```

---

## Option 3: Docker Deployment (Advanced)

For AWS, Google Cloud, or DigitalOcean:

### Using Docker Compose

You already have `docker-compose.yml`!

```bash
# On your server
git clone https://github.com/alaneballesteros/script-to-film-platform.git
cd script-to-film-platform

# Copy and configure environment
cp .env.example .env
# Edit .env with production values

# Build and run
docker-compose up -d

# Access on port 80
```

Point your domain to the server IP!

---

## Custom Domain Setup

### Add Your Own Domain (Optional)

If you want `https://scripttofilm.com` instead of Vercel/Railway URLs:

#### 1. Buy a Domain
- **Namecheap:** ~$12/year
- **Google Domains:** ~$12/year
- **Cloudflare:** ~$10/year

#### 2. Configure on Vercel (Frontend)

1. Go to Vercel project settings
2. Click "Domains"
3. Add your domain: `scripttofilm.com`
4. Follow DNS instructions
5. Vercel provides SSL automatically!

#### 3. Configure on Railway (Backend)

1. Go to Railway project settings
2. Click "Networking" → "Custom Domain"
3. Add: `api.scripttofilm.com`
4. Update DNS records as shown

#### Final URLs:
- Frontend: `https://scripttofilm.com`
- Backend: `https://api.scripttofilm.com`

---

## Environment Variables Checklist

### Required for Production

```env
# Backend (.env on Railway/Render)
API_HOST=0.0.0.0
API_PORT=$PORT
API_ENV=production
DEBUG=false

DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
RUNWAY_API_KEY=key_...
SECRET_KEY=long-random-string

# Frontend (.env on Vercel)
VITE_API_URL=https://your-backend-url/api/v1
```

---

## Monitoring & Logs

### Railway
- Go to project → "Deployments" tab
- Click on latest deployment
- See real-time logs

### Vercel
- Go to project → "Deployments"
- Click on deployment
- View build and function logs

### Render
- Go to service dashboard
- Click "Logs" tab
- View real-time logs

---

## Troubleshooting

### Frontend can't connect to backend

**Check:**
1. `VITE_API_URL` in Vercel matches Railway URL
2. Backend CORS allows your Vercel domain
3. Backend is running (check Railway logs)

### Database connection errors

**Check:**
1. `DATABASE_URL` is set correctly
2. PostgreSQL database is running
3. Database migrations ran (if any)

### Build failures

**Backend:**
- Check `requirements.txt` has all dependencies
- Verify Python version (should be 3.9+)

**Frontend:**
- Check `package.json` has all dependencies
- Verify Node version (should be 18+)

---

## Cost Breakdown

### Free Tier (Forever)
- **Railway:** 500 hours/month free (enough for 1 app)
- **Vercel:** Unlimited deployments, 100GB bandwidth
- **Total:** $0/month

### If You Exceed Free Tier
- **Railway:** ~$5/month for hobby tier
- **Vercel:** Free tier is usually sufficient
- **Domain:** ~$12/year (optional)
- **Total:** ~$5-7/month

---

## Deployment Workflow

### Day-to-Day Process

```bash
# You make changes locally
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Create PR on GitHub
# Friend reviews and approves
# Merge to main

# Automatic deployment starts:
# - Railway rebuilds backend (2-3 min)
# - Vercel rebuilds frontend (1-2 min)
# - Both update automatically!

# Check live site
open https://script-to-film-platform.vercel.app
```

---

## Security Checklist

Before going live:

- [ ] All API keys in environment variables (not in code)
- [ ] `.env` files in `.gitignore` (already done ✓)
- [ ] `DEBUG=false` in production
- [ ] CORS configured with specific domains (not `*`)
- [ ] HTTPS enabled (Vercel/Railway do this automatically)
- [ ] Database backups enabled
- [ ] Strong `SECRET_KEY` generated

---

## Next Steps

1. **Deploy backend to Railway** (15 minutes)
2. **Deploy frontend to Vercel** (10 minutes)
3. **Test live application** (5 minutes)
4. **Invite friend** to GitHub repo
5. **Both start building!**

Every time you merge to `main`, the live site updates automatically!

---

## Quick Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Your GitHub Repo:** https://github.com/alaneballesteros/script-to-film-platform

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs

Happy deploying! 🚀
