# NVC AI Facilitator - Deployment Guide

## Quick Deploy to Railway

### Option 1: One-Click Deploy (Easiest)
1. **Fork this repository** to your GitHub account
2. **Go to [Railway.app](https://railway.com)**
3. **Sign up/Login** with your GitHub account
4. **Click "New Project"** → **"Deploy from GitHub repo"**
5. **Select your forked repo**
6. **Add Environment Variable**: `OPENAI_API_KEY` with your OpenAI API key
7. **Deploy!** - Railway will automatically detect the Python app and deploy

### Option 2: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add OpenAI API key
railway variables set OPENAI_API_KEY=your-api-key-here

# Deploy
railway up
```

## Alternative: Deploy to Render

1. **Fork this repository** to your GitHub account
2. **Go to [Render.com](https://render.com)**
3. **Create New** → **Web Service**
4. **Connect your GitHub repo**
5. **Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   - `OPENAI_API_KEY`: your-api-key-here
7. **Deploy**

## Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key (required for AI responses)
- `PORT`: Automatically set by hosting platform

## Testing Your Deployment

1. **Backend API**: Visit `https://your-app-url.railway.app/health`
2. **Web Interface**: Visit `https://your-app-url.railway.app/test`
3. **API Docs**: Visit `https://your-app-url.railway.app/api/v1/docs`

## Local Development

```bash
# Start backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app/main.py

# Test UI
open test_ui.html in browser or visit http://localhost:19000/test
```

## Architecture

- **Backend**: Python FastAPI serving API and static UI
- **Frontend**: Single HTML file with embedded CSS/JavaScript
- **Database**: None required (stateless conversation)
- **AI**: OpenAI GPT-4o-mini via API

## Cost Estimate

- **Railway Free Tier**: $5 credit (covers ~1-2 months light usage)
- **OpenAI API**: ~$0.01 per conversation (GPT-4o-mini pricing)
- **Total**: Very low cost for testing and demos