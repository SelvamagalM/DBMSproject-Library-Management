# Vercel Deployment Guide for Library Management System

## Prerequisites
1. **GitHub account** - Vercel integrates with GitHub
2. **Vercel account** - Sign up at https://vercel.com
3. **Git repository** - Your code should be in a GitHub repository

## Important Note: Database Limitation
⚠️ **SQLite on Vercel is ephemeral** - The `library.db` file will be reset on every deployment since Vercel doesn't persist files between deployments. For production, consider migrating to PostgreSQL or Firebase.

## Deployment Steps

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Setup for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel
- Go to https://vercel.com/dashboard
- Click "Add New..." → "Project"
- Select "Import Git Repository"
- Choose your GitHub repository
- Click "Import"

### 3. Configure Vercel Settings
**Root Directory:** `library_web` (or leave blank if that's your project root)

**Build Command:** (leave default)

**Install Command:** (leave default)

**Environment Variables:** (optional)
```
PYTHON_VERSION=3.11
```

### 4. Deploy
- Click "Deploy"
- Wait for build to complete
- Your app will be available at: `https://your-project-name.vercel.app`

## Accessing Your App
Once deployed:
- Go to your Vercel deployment URL
- Login with:
  - Admin: `admin` / `admin123`
  - Members: Use registered email / `member123`

## Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Make sure `vercel.json` is in the root
- Verify `api/index.py` exists

### Database Issues
- SQLite data is lost on each deployment
- To keep data persistent, migrate to a cloud database:
  - PostgreSQL (Supabase, Railway)
  - Firebase Realtime Database
  - MongoDB (MongoDB Atlas)

### Cold Starts
- First request to Vercel app may be slow (this is normal)
- Subsequent requests are faster

## Local Development
Still works as before:
```bash
python library_web/app.py
```

Or with ngrok tunnel:
```bash
python library_web/run_with_tunnel.py
```

## Next Steps for Production
1. Move data to cloud database
2. Use environment variables for secrets
3. Enable HTTPS (automatic on Vercel)
4. Set up CI/CD for automatic deploys
