# Deployment Guide

This guide walks you through deploying SmartOps AI with:
- **Backend**: Render (Free tier)
- **Frontend**: Vercel (Free tier)

## Prerequisites

1. GitHub account (you already have the code pushed)
2. Render account (sign up at https://render.com)
3. Vercel account (sign up at https://vercel.com)
4. Google Gemini API key (from https://makersuite.google.com/app/apikey)

---

## Part 1: Deploy Backend to Render

### Step 1: Connect GitHub to Render

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select repository: **Incident_Intelligent_Platform**

### Step 2: Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `smartops-ai-backend` (or your preferred name)
- **Region**: Choose closest to you (e.g., Oregon)
- **Branch**: `main`
- **Root Directory**: `Project/backend`
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **Free** plan

### Step 3: Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.9` |
| `GEMINI_API_KEY` | `your_gemini_api_key_here` |
| `GEMINI_MODEL` | `gemini-flash-latest` |
| `API_HOST` | `0.0.0.0` |
| `API_PORT` | `8002` |
| `DEBUG` | `False` |
| `DATABASE_URL` | `sqlite:///./smartops_ai.db` |
| `CORS_ORIGINS` | `*` |

**Important:** Replace `your_gemini_api_key_here` with your actual Gemini API key!

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment to complete
3. Once deployed, you'll get a URL like: `https://smartops-ai-backend.onrender.com`
4. Test it by visiting: `https://smartops-ai-backend.onrender.com/docs`

**Note:** First request may take 30-60 seconds as Render cold-starts the free tier service.

### Step 5: Test Backend

```bash
curl https://your-backend-url.onrender.com/api/pdf/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "PDF Generator",
  "available": true
}
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Connect GitHub to Vercel

1. Go to https://vercel.com and sign in
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: **Incident_Intelligent_Platform**

### Step 2: Configure Project

**Build Settings:**
- **Framework Preset**: `Vite`
- **Root Directory**: `Project/frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install --legacy-peer-deps`

### Step 3: Add Environment Variable

Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `VITE_API_URL` | `https://your-backend-url.onrender.com` |

**Replace** `your-backend-url.onrender.com` with your actual Render backend URL from Part 1.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build and deployment
3. You'll get a URL like: `https://smartops-ai.vercel.app`

### Step 5: Test Frontend

1. Visit your Vercel URL
2. Login with: `operator@smartops.ai` / `password123`
3. Navigate to Investigation page
4. Try creating an investigation

---

## Part 3: Update CORS Settings (If Needed)

If you get CORS errors, update the backend environment variable:

1. Go to Render Dashboard → Your Web Service
2. Go to **Environment** tab
3. Update `CORS_ORIGINS` to include your Vercel domain:
   ```
   https://smartops-ai.vercel.app,https://*.vercel.app
   ```
4. Click **"Save Changes"**
5. Service will automatically redeploy

---

## Part 4: Custom Domain (Optional)

### For Vercel (Frontend)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update backend CORS if needed

### For Render (Backend)

1. Upgrade to paid plan (required for custom domains)
2. Go to Settings → Custom Domain
3. Add your domain and configure DNS

---

## Monitoring & Maintenance

### Render Dashboard

Monitor your backend:
- **Logs**: View real-time application logs
- **Metrics**: CPU, memory usage
- **Events**: Deployment history

### Vercel Dashboard

Monitor your frontend:
- **Deployments**: Build history and status
- **Analytics**: Page views, performance
- **Logs**: Function logs and errors

### Health Checks

Set up uptime monitoring (free services):
- UptimeRobot: https://uptimerobot.com
- Better Uptime: https://betteruptime.com

Monitor URLs:
- Backend: `https://your-backend.onrender.com/api/pdf/health`
- Frontend: `https://your-frontend.vercel.app`

---

## Troubleshooting

### Backend Issues

**Problem**: "Application failed to respond"
- **Solution**: Check Render logs, verify GEMINI_API_KEY is set correctly

**Problem**: "Module not found"
- **Solution**: Verify `requirements.txt` includes all dependencies

**Problem**: Database errors
- **Solution**: SQLite file will be recreated on each deploy (use PostgreSQL for persistence)

### Frontend Issues

**Problem**: "Network Error" when calling API
- **Solution**: Verify `VITE_API_URL` is set correctly in Vercel environment variables

**Problem**: Build fails
- **Solution**: Ensure `npm install --legacy-peer-deps` is used in install command

**Problem**: 404 on refresh
- **Solution**: Vercel.json already configured for SPA routing

### CORS Issues

**Problem**: "CORS policy blocked"
- **Solution**: Update `CORS_ORIGINS` in Render to include your Vercel domain

---

## Cost Breakdown

### Free Tier Limits

**Render Free Tier:**
- 750 hours/month (enough for 1 service running 24/7)
- Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 512 MB RAM, shared CPU

**Vercel Free Tier:**
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Global CDN
- Instant deploys

### Upgrade Considerations

Consider upgrading when:
- Backend needs to stay always-on (Render: $7/month)
- Need custom domains (Render: $7/month, Vercel: Free)
- Need more resources (Render: $7-$25/month)
- Need PostgreSQL database (Render: $7/month)

---

## Production Recommendations

1. **Database**: Switch from SQLite to PostgreSQL
   - Add PostgreSQL database in Render
   - Update `DATABASE_URL` environment variable

2. **Environment Variables**: Use separate production values
   - Different Gemini API key (with quota management)
   - Specific CORS origins (not wildcard)

3. **Monitoring**: Set up alerts
   - Uptime monitoring for both services
   - Error tracking (Sentry, LogRocket)

4. **Backups**: Regular database backups
   - Render PostgreSQL has automatic backups
   - Export knowledge base periodically

5. **Rate Limiting**: Implement API rate limiting
   - Protect against abuse
   - Manage Gemini API quota

---

## Quick Reference

### Render Dashboard
https://dashboard.render.com

### Vercel Dashboard
https://vercel.com/dashboard

### Your Deployed URLs
- **Backend**: https://[your-service].onrender.com
- **Frontend**: https://[your-project].vercel.app
- **API Docs**: https://[your-service].onrender.com/docs

### Support
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- GitHub Issues: https://github.com/Vaish5002/Incident_Intelligent_Platform/issues

---

## Next Steps

After successful deployment:

1. Test all features in production
2. Share your deployed URL with team
3. Monitor logs for any issues
4. Set up uptime monitoring
5. Consider upgrading for better performance

Congratulations! Your SmartOps AI is now live!
