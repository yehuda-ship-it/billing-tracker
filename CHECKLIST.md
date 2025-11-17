# Deployment Checklist

Use this checklist to deploy your billing tracker to Railway.app

---

## Pre-Deployment

- [ ] I have all files from the `billing-tracker` folder
- [ ] I have a GitHub account
- [ ] I have a Railway account (or will sign up with GitHub)
- [ ] I have 15-20 minutes available
- [ ] (Optional) I have access to DNS settings for custom domain

---

## Step 1: GitHub Setup (5 minutes)

- [ ] Created new repository on GitHub named "billing-tracker"
- [ ] Uploaded/pushed all files to GitHub
- [ ] Verified all files are there (check frontend/, backend/, etc.)
- [ ] Repository is set to Private (recommended)

---

## Step 2: Railway Deployment (5 minutes)

- [ ] Signed up for Railway.app (used GitHub login)
- [ ] Created new project in Railway
- [ ] Selected "Deploy from GitHub repo"
- [ ] Chose "billing-tracker" repository
- [ ] Railway started deploying
- [ ] Added PostgreSQL database (clicked "+ New" → Database → PostgreSQL)
- [ ] Database automatically linked to app
- [ ] Deployment completed successfully (saw green checkmark)
- [ ] Generated domain in Settings → Networking
- [ ] Copied the URL

---

## Step 3: Testing (5 minutes)

- [ ] Opened the Railway URL in browser
- [ ] Saw billing tracker load successfully
- [ ] Saw default groups (Alabama Facilities, Weekly Facilities)
- [ ] Clicked on a group, saw facilities
- [ ] Edited a billing record
- [ ] Clicked save
- [ ] Refreshed the page
- [ ] Change was still there (data persisted!)
- [ ] Opened Settings
- [ ] Made a change (e.g., renamed a group)
- [ ] Refreshed
- [ ] Setting change persisted

---

## Step 4: Custom Domain (Optional - 10 minutes)

- [ ] Decided on subdomain (e.g., billing.aredgegroup.com)
- [ ] In Railway: Settings → Networking → Custom Domain
- [ ] Entered my custom domain
- [ ] Railway showed me CNAME value
- [ ] Copied CNAME value
- [ ] Logged into DNS provider (Cloudflare, Namecheap, etc.)
- [ ] Added CNAME record:
  - Type: CNAME
  - Name: billing (or whatever I chose)
  - Value: (pasted Railway's value)
  - TTL: Auto or 3600
- [ ] Saved DNS record
- [ ] Waited 10-30 minutes
- [ ] Tested custom domain - it works!

---

## Step 5: Team Rollout (10 minutes)

- [ ] Shared URL with team
- [ ] Confirmed team members can access
- [ ] Opened Settings in app
- [ ] Deleted default groups
- [ ] Created real facility groups
- [ ] Added real facilities
- [ ] Set up correct billing schedules
- [ ] Added month-end tracker URL (if applicable)
- [ ] Verified all changes saved
- [ ] Team tested making edits
- [ ] Confirmed multi-user works

---

## Post-Deployment

- [ ] Bookmarked Railway dashboard
- [ ] Set calendar reminder to check costs weekly
- [ ] Documented the URL for team
- [ ] (Optional) Added to company wiki/docs
- [ ] (Optional) Set up uptime monitoring

---

## Troubleshooting (If Needed)

If something didn't work:

### App Won't Load
- [ ] Checked Railway deployment logs
- [ ] Looked for Python errors
- [ ] Verified DATABASE_URL environment variable exists
- [ ] Tried restarting service in Railway

### Database Issues
- [ ] Checked PostgreSQL service is running
- [ ] Verified it's linked to web service
- [ ] Restarted web service

### Custom Domain Issues
- [ ] Double-checked CNAME record is correct
- [ ] Waited longer (can take up to 48 hours)
- [ ] Checked for conflicting DNS records
- [ ] Tested with Railway URL to confirm app works

---

## Success Criteria

✅ **You're successful when:**
- App loads at your URL
- Multiple team members can access simultaneously
- Changes save and persist
- Settings can be modified
- Billing records can be edited
- Groups and facilities can be managed
- Everything "just works"

---

## Next Actions

After successful deployment:

### Immediate
- [ ] Train team on features
- [ ] Add real billing data
- [ ] Test all functionality
- [ ] Document any issues

### This Week
- [ ] Monitor Railway dashboard
- [ ] Check credit usage
- [ ] Verify automatic backups working
- [ ] Gather team feedback

### This Month
- [ ] Review costs
- [ ] Consider paid tier if needed
- [ ] Plan any feature additions
- [ ] Document any custom workflows

---

## Support Resources

### If I Get Stuck:
1. Check QUICKSTART.md
2. Check README.md troubleshooting section
3. Check Railway Discord: https://discord.gg/railway
4. Check Railway docs: https://docs.railway.app

### Railway Support:
- Discord (fastest): https://discord.gg/railway
- Email: help@railway.app
- Response time: Usually <1 hour

---

## Cost Tracking

### Current Plan:
- [ ] Using free tier ($5/month credit)
- [ ] Using paid tier ($5/month + $5 credit)
- [ ] Using paid tier ($20/month + $20 credit)

### Expected Monthly Cost:
- Backend: ~$3/month
- Database: ~$2/month
- Total: ~$5/month

### Actual Cost This Month:
- Check Railway dashboard weekly
- Document here: $_____/month

---

## Backup Verification

- [ ] Confirmed Railway automatic backups enabled
- [ ] Checked backup settings in dashboard
- [ ] Tested database export (optional)
- [ ] Code is safe in GitHub
- [ ] Documented recovery process

---

## Update Process

When I need to make changes:

- [ ] Edit files locally
- [ ] (Optional) Test locally
- [ ] Commit changes: `git commit -am "Description"`
- [ ] Push to GitHub: `git push`
- [ ] Wait 2-3 minutes for Railway to deploy
- [ ] Check Railway deployment logs
- [ ] Test changes at my URL
- [ ] Verify everything works

---

## Performance Monitoring

- [ ] Bookmarked Railway metrics dashboard
- [ ] Checking CPU/memory usage: Normal/High
- [ ] Checking response times: Fast/Slow
- [ ] Any errors in logs: Yes/No
- [ ] App performance: Good/Needs attention

---

## Team Feedback

Track team feedback on the app:

**Positive:**
- 
- 
- 

**Issues:**
- 
- 
- 

**Feature Requests:**
- 
- 
- 

---

## Future Enhancements

Ideas for later:

- [ ] Email notifications
- [ ] Export to Excel
- [ ] User authentication
- [ ] Mobile app
- [ ] Integrations
- [ ] Other: _______________

---

**Date Deployed:** _______________
**Deployed By:** _______________
**Current URL:** _______________
**Status:** ⬜ In Progress  ⬜ Complete  ⬜ Issue

---

**Notes:**
