# Quick Start Guide - 15 Minutes to Deployment

## What You're Building
A cloud-hosted billing tracker that your whole team can access at a nice URL like `https://billing.aredgegroup.com`

## Total Time: ~15 minutes
## Total Cost: $0-5/month

---

## Step 1: Get the Code on GitHub (5 minutes)

1. **Download your billing-tracker folder** (you should have this already)

2. **Go to GitHub:**
   - Visit https://github.com/new
   - Repository name: `billing-tracker`
   - Keep it Private
   - Don't check any boxes
   - Click "Create repository"

3. **Upload your code:**
   
   **Option A - If you have Git installed:**
   ```bash
   cd /path/to/billing-tracker
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/billing-tracker.git
   git push -u origin main
   ```

   **Option B - If you don't have Git:**
   - In GitHub, click "uploading an existing file"
   - Drag and drop ALL folders/files from billing-tracker
   - Click "Commit changes"

---

## Step 2: Deploy to Railway (5 minutes)

1. **Sign up for Railway:**
   - Go to https://railway.app
   - Click "Login with GitHub"
   - Authorize Railway

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose "billing-tracker"
   - Railway detects Python and starts deploying

3. **Add database:**
   - In your project, click "+ New"
   - Select "Database"
   - Choose "PostgreSQL"
   - It automatically connects to your app

4. **Wait for deployment:**
   - Watch the logs scroll
   - Should complete in 2-3 minutes
   - You'll see "✓ Deployed successfully"

5. **Get your URL:**
   - Click on your web service (not database)
   - Go to "Settings" tab
   - Find "Networking" section
   - Click "Generate Domain"
   - Copy the URL (looks like: `billing-tracker-production.up.railway.app`)

---

## Step 3: Test It (2 minutes)

1. **Open the URL** Railway gave you
2. **You should see:** Your billing tracker with default groups
3. **Test:** Try editing a billing record and saving it
4. **Refresh:** The changes should still be there

✅ **Success!** Your app is live.

---

## Step 4: Custom Domain - OPTIONAL (5 minutes)

If you want `billing.aredgegroup.com` instead of the Railway URL:

### In Railway:
1. Go to your service → Settings → Networking
2. Click "Custom Domain"
3. Enter: `billing.aredgegroup.com`
4. Railway shows you a CNAME value (copy it)

### In Your DNS (Cloudflare, Namecheap, etc.):
1. Add CNAME record:
   - Type: `CNAME`
   - Name: `billing`
   - Value: [paste what Railway showed]
   - TTL: `Auto` or `3600`
2. Save

### Wait 10-30 minutes for DNS to propagate

### Test:
- Visit `https://billing.aredgegroup.com`
- Should work!

---

## 🎉 You're Done!

**Your app is now:**
- ✅ Live 24/7 on the internet
- ✅ Accessible by your whole team
- ✅ Saving data to a real database
- ✅ Automatically backed up by Railway
- ✅ SSL secured (HTTPS)

**Share the URL with your team and start using it!**

---

## What's Next?

### Customize Your Data:
1. Click "Settings" in the app
2. Edit the groups and facilities
3. Add your real billing schedules
4. All changes save automatically

### Monitor Usage:
- Railway Dashboard shows your usage
- Free tier: $5/month credit
- Typical usage: $3-5/month
- If you exceed free tier, Railway will email you

### Make Updates:
1. Edit your code locally
2. Push to GitHub
3. Railway automatically redeploys
4. Takes 2-3 minutes

---

## Troubleshooting

### "Application Error"
- Check Railway logs: Click Deployments → View Logs
- Most common: DATABASE_URL not set (should be automatic)

### App is slow
- Free tier sleeps after 15 min inactivity
- First load after sleep: ~30 seconds
- After that: fast

### Can't connect to database
- Make sure PostgreSQL service is running in Railway
- Restart your service: Settings → Restart

### Custom domain not working
- DNS can take up to 48 hours (usually 10-30 min)
- Check CNAME record is correct
- Make sure there's no conflicting A record

---

## Need Help?

- Railway Discord: https://discord.gg/railway
- Railway Docs: https://docs.railway.app
- Railway usually responds in <1 hour

---

## Cost Breakdown

### Free Tier:
- $5/month in credits (free!)
- Usually enough for small teams

### If You Exceed Free Tier:
- $5/month minimum (gets $5 in credits)
- Backend: ~$3/month
- Database: ~$2/month
- Total: ~$5/month

**No surprise charges - Railway will email before billing**

---

**That's it! Enjoy your cloud-hosted billing tracker! 🚀**
