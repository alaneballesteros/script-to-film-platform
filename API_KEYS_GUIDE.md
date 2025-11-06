# API Keys Setup Guide

This guide shows you how to get all the API keys needed to run the Script to Film Platform locally.

## Overview

You need API keys for:
- **OpenAI** (GPT for script generation) - Required for AI features
- **Anthropic** (Claude AI - alternative) - Optional, but recommended
- **Runway** (Video generation) - Optional for video features

## Cost Overview

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **OpenAI** | $5 free credits (new accounts) | Pay as you go (~$0.002/request) |
| **Anthropic** | Limited free trial | Pay as you go (~$0.003/request) |
| **Runway** | Limited free credits | Pay per video generation |

**For Development:** The free tiers are usually sufficient!

---

## 1. OpenAI API Key (GPT for Script Generation)

### Step 1: Create Account

1. Go to: https://platform.openai.com/signup
2. Sign up with email or Google/Microsoft account
3. Verify your email

### Step 2: Get API Key

1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "Script to Film Development"
4. Click "Create secret key"
5. **IMPORTANT:** Copy the key immediately (starts with `sk-`)
   - You won't be able to see it again!
   - Example: `sk-proj-abc123...`

### Step 3: Add Credits (If Needed)

New accounts get $5 free credits. If expired:

1. Go to: https://platform.openai.com/account/billing/overview
2. Click "Add payment method"
3. Add credit card
4. Add $5-10 for development

### Usage & Cost

- **Script generation:** ~$0.002 per script (~500 scripts for $1)
- **Free tier:** Usually lasts weeks for development
- **Monitor usage:** https://platform.openai.com/account/usage

---

## 2. Anthropic API Key (Claude AI - Alternative)

### Step 1: Create Account

1. Go to: https://console.anthropic.com
2. Click "Sign Up"
3. Sign up with email or Google
4. Verify your email

### Step 2: Get API Key

1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Name it: "Script to Film Development"
4. Click "Create Key"
5. **Copy the key** (starts with `sk-ant-`)
   - Example: `sk-ant-api03-abc123...`

### Step 3: Add Credits

1. Go to: https://console.anthropic.com/settings/billing
2. Click "Add credits"
3. Add $5-10 for development

### Usage & Cost

- **Claude Sonnet:** ~$0.003 per request
- **Good for:** AI script generation, scene analysis
- **Monitor:** https://console.anthropic.com/settings/usage

---

## 3. Runway API Key (Video Generation - Optional)

**Note:** Runway is optional. You can develop without it and add later.

### Step 1: Create Account

1. Go to: https://runwayml.com
2. Click "Sign Up"
3. Create account with email

### Step 2: Get API Key

1. Log in to Runway
2. Go to: Settings → API
3. Or direct link: https://app.runwayml.com/settings/api
4. Click "Generate API Key"
5. **Copy the key**
   - Example: `key_abc123...`

### Step 3: Add Credits

1. Go to billing settings
2. Purchase credits
3. Video generation uses credits per second

### Usage & Cost

- **Gen-2 Video:** ~$0.05 per second of video
- **4-second clip:** ~$0.20
- **For development:** You can skip this initially

---

## 4. Setup Your Local Environment

### Step 1: Copy Environment Template

```bash
# In your project directory
cd script-to-film-platform
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in your text editor:

```bash
# Use nano, vim, or VS Code
nano .env
# or
code .env
```

### Step 3: Add Your API Keys

Replace the placeholder values:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=development
DEBUG=true

# Database (SQLite for local development)
DATABASE_URL=sqlite:///./script_to_film.db

# AI Services - ADD YOUR KEYS HERE
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_OPENAI_KEY_HERE
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_ANTHROPIC_KEY_HERE
RUNWAY_API_KEY=key_YOUR_ACTUAL_RUNWAY_KEY_HERE

# Security (for local dev, this is fine)
SECRET_KEY=dev-secret-key-12345-change-in-production

# Application Settings (defaults are fine)
MAX_SCRIPT_LENGTH=10000
MAX_VIDEO_DURATION=300
OUTPUT_VIDEO_FORMAT=mp4
OUTPUT_VIDEO_RESOLUTION=1920x1080
OUTPUT_VIDEO_FPS=30
```

### Step 4: Save and Verify

```bash
# Save the file (Ctrl+O in nano, Cmd+S in VS Code)
# Exit (Ctrl+X in nano)

# Verify it exists
cat .env | grep API_KEY
# Should show your keys (don't share this output!)
```

---

## 5. Testing Your Setup

### Test Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Start backend
python -m uvicorn script_to_film.main:app --reload --port 8000

# In another terminal, test the API
curl http://localhost:8000/api/v1/
# Should return: {"message":"Script to Film API","version":"0.1.0"}
```

### Test Frontend

```bash
# In frontend directory
cd frontend
npm run dev

# Open browser
open http://localhost:3001
```

### Test AI Integration

Try generating a script in the UI to verify your API keys work!

---

## Troubleshooting

### "Invalid API key" Error

**OpenAI:**
- Make sure key starts with `sk-proj-` or `sk-`
- Check for spaces or quotes in .env file
- Verify key at: https://platform.openai.com/api-keys

**Anthropic:**
- Make sure key starts with `sk-ant-`
- Verify key at: https://console.anthropic.com/settings/keys

**Runway:**
- Make sure key starts with `key_`
- Verify key at: https://app.runwayml.com/settings/api

### "Insufficient quota" Error

You've run out of credits:
- **OpenAI:** Add credits at https://platform.openai.com/account/billing
- **Anthropic:** Add credits at https://console.anthropic.com/settings/billing

### Can't find .env file

```bash
# Make sure you're in the right directory
pwd
# Should show: /path/to/script-to-film-platform

# Create .env if missing
cp .env.example .env
```

---

## Security Best Practices

### ✅ DO:
- Keep API keys in `.env` file only
- Add `.env` to `.gitignore` (already done ✓)
- Use different keys for development and production
- Rotate keys periodically
- Monitor usage regularly

### ❌ DON'T:
- Commit `.env` to git
- Share keys in Slack/email
- Use production keys for development
- Hardcode keys in source code
- Share screenshots showing keys

---

## Key Rotation (If Compromised)

If you accidentally expose a key:

### OpenAI
1. Go to: https://platform.openai.com/api-keys
2. Click the trash icon next to compromised key
3. Create a new key
4. Update `.env` with new key

### Anthropic
1. Go to: https://console.anthropic.com/settings/keys
2. Click "Revoke" on compromised key
3. Create new key
4. Update `.env` with new key

### Runway
1. Go to: https://app.runwayml.com/settings/api
2. Revoke old key
3. Generate new key
4. Update `.env` with new key

---

## For Production Deployment

When deploying to Railway/Vercel:

**DON'T:**
- Use your personal development keys

**DO:**
1. Create separate production API keys
2. Add them as environment variables in Railway/Vercel dashboard
3. Set up billing alerts
4. Monitor usage closely

See `DEPLOYMENT_GUIDE.md` for details.

---

## Cost Optimization Tips

### 1. Use Caching
- Cache AI responses for common prompts
- Avoid regenerating same content

### 2. Monitor Usage
- Check OpenAI dashboard weekly
- Set up billing alerts
- Track which features use most credits

### 3. Development Practices
- Use mock responses for testing when possible
- Test with short scripts first
- Don't spam the API during development

### 4. Free Alternatives for Testing
- Use mock data for UI development
- Test with cached responses
- Only call real APIs when needed

---

## Minimum Requirements

### To run locally (minimum):
- ✅ **OpenAI API Key** (for script generation)
- ❌ Anthropic (optional alternative)
- ❌ Runway (optional, for video features)

### For full functionality:
- ✅ OpenAI or Anthropic (at least one)
- ✅ Runway (for video generation)

---

## Quick Reference

### Where to Get Keys

| Service | URL |
|---------|-----|
| **OpenAI** | https://platform.openai.com/api-keys |
| **Anthropic** | https://console.anthropic.com/settings/keys |
| **Runway** | https://app.runwayml.com/settings/api |

### Where Keys Go

```env
# In .env file (project root)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
RUNWAY_API_KEY=your_key_here
```

### Testing Keys Work

```bash
# Start backend
python -m uvicorn script_to_film.main:app --reload

# Try generating a script in the UI
open http://localhost:3001
```

---

## Need Help?

- **OpenAI Issues:** https://help.openai.com
- **Anthropic Issues:** https://support.anthropic.com
- **Runway Issues:** https://help.runwayml.com

---

## Summary

1. **Sign up** for OpenAI (required) and Anthropic (optional)
2. **Get API keys** from each dashboard
3. **Copy** `.env.example` to `.env`
4. **Add keys** to your `.env` file
5. **Never commit** `.env` to git
6. **Test** by running the app locally

**Estimated setup time:** 10-15 minutes
**Cost for development:** ~$5-10 should last weeks

Happy developing! 🚀
