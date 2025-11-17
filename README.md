# Billing Tracker - Railway Deployment Guide

A multi-user billing tracker application with PostgreSQL database, deployed on Railway.app.

## 🚀 Features

- ✅ Multi-user support with PostgreSQL database
- ✅ Multiple billing frequencies (weekly, bi-weekly, bi-monthly, monthly, custom)
- ✅ Facility groups management
- ✅ Billing records tracking
- ✅ Custom billing schedules
- ✅ Month-end tracker integration
- ✅ Automatic data persistence

## 📋 Prerequisites

- Git installed on your computer
- GitHub account (free)
- Railway account (free) - Sign up at https://railway.app

## 🎯 Deployment Steps

### Step 1: Prepare Your Code

1. **Create a GitHub repository:**
   ```bash
   # Navigate to the billing-tracker folder
   cd billing-tracker
   
   # Initialize git
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - Billing Tracker"
   ```

2. **Push to GitHub:**
   - Go to https://github.com/new
   - Create a new repository (name it "billing-tracker")
   - Don't initialize with README (we already have files)
   - Copy the commands GitHub shows and run them:
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/billing-tracker.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Go to Railway.app:**
   - Visit https://railway.app
   - Click "Login" → Sign in with GitHub
   - Authorize Railway to access your GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your "billing-tracker" repository
   - Railway will auto-detect it's a Python app

3. **Add PostgreSQL Database:**
   - In your project, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically create a PostgreSQL database
   - It will auto-link it to your app (DATABASE_URL env var)

4. **Configure Environment:**
   - Your app should automatically deploy
   - Wait 2-3 minutes for deployment to complete

5. **Generate Domain:**
   - Click on your service (not the database)
   - Go to "Settings" tab
   - Scroll to "Networking"
   - Click "Generate Domain"
   - You'll get a URL like: `https://billing-tracker-production.up.railway.app`

### Step 3: Test Your App

1. **Open the URL** Railway generated
2. You should see your Billing Tracker loading
3. The default groups and facilities should appear
4. Try editing a billing record - it should save to the database

### Step 4: Custom Domain (Optional)

If you want to use your company domain (e.g., `billing.aredgegroup.com`):

1. **In Railway:**
   - Go to your service → Settings → Networking
   - Click "Custom Domain"
   - Enter: `billing.aredgegroup.com`
   - Railway will show you DNS records to add

2. **In Your DNS Provider (Cloudflare, Namecheap, etc.):**
   - Add a CNAME record:
   ```
   Type: CNAME
   Name: billing
   Value: [the value Railway showed you]
   TTL: Auto
   ```

3. **Wait 5-30 minutes** for DNS to propagate
4. **Access your app** at https://billing.aredgegroup.com

## 💰 Pricing

### Railway Pricing:
- **Free Tier:** $5/month in credits (should be enough for small team)
- **Paid:** $5/month gets you $5 in credits
- Typical usage for small team: $3-8/month

### What Uses Credits:
- Backend service: ~$3-5/month
- PostgreSQL database: ~$2-3/month
- Total: ~$5-8/month

## 🔧 Making Changes

### To Update Your App:

1. **Make changes locally** to your code
2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. **Railway auto-deploys** - wait 2-3 minutes
4. **Refresh your browser** to see changes

## 📊 Database Access

### View Your Database:

1. In Railway, click on your PostgreSQL service
2. Go to "Data" tab
3. You can view/edit tables directly

### Tables Created:
- `facility_groups` - Your billing groups
- `facilities` - Facilities in each group
- `billing_records` - All billing records
- `custom_dates` - Custom billing dates
- `settings` - App settings (month-end URL, etc.)

## 🐛 Troubleshooting

### App Won't Load:
1. Check Railway logs: Service → Deployments → Click latest → View Logs
2. Look for error messages
3. Make sure DATABASE_URL is set (should be automatic)

### Database Connection Error:
1. Make sure PostgreSQL service is running
2. Check that DATABASE_URL environment variable exists
3. Restart the service: Service → Settings → Restart

### Changes Not Showing:
1. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
2. Check deployment status in Railway
3. View logs for errors

## 📞 Support

### Railway Support:
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

### Common Issues:

**"Failed to load facility groups"**
- Database isn't connected
- Check Railway logs
- Verify PostgreSQL service is running

**"Application Error"**
- Check deployment logs in Railway
- Make sure all files were pushed to GitHub
- Verify requirements.txt has all dependencies

**Slow Loading**
- Free tier may sleep after inactivity
- First request after sleep takes ~30 seconds
- Subsequent requests are fast

## 🔐 Security Notes

- Railway handles SSL automatically (HTTPS)
- Database is not publicly accessible
- Only your backend can access the database
- All connections are encrypted

## 📈 Monitoring

In Railway dashboard you can see:
- CPU usage
- Memory usage
- Database size
- Request count
- Deployment history

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] App deployed successfully
- [ ] Can access app via Railway URL
- [ ] Can view and edit billing records
- [ ] Settings save properly
- [ ] (Optional) Custom domain configured

## 💡 Next Steps

Once deployed successfully:

1. **Add Your Real Data:**
   - Go to Settings
   - Update facility groups
   - Add your facilities
   - Configure billing schedules

2. **Share with Team:**
   - Send them the URL
   - Everyone can access immediately
   - No installation needed

3. **Monitor Usage:**
   - Check Railway dashboard weekly
   - Watch credit usage
   - Upgrade if needed

---

**Need Help?** Check Railway docs or reach out to support!
