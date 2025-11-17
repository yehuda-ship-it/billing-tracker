# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Team Members                         │
│  👤 Yehuda    👤 Team Member 2    👤 Team Member 3          │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Railway.app Cloud Platform                      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         billing.aredgegroup.com                      │   │
│  │         (or Railway default URL)                     │   │
│  │         [SSL Certificate Included]                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                   │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Frontend (billing_tracker.html)                     │   │
│  │  • React Application                                 │   │
│  │  • Served by Flask                                   │   │
│  │  • Runs in user's browser                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                   │
│                           │ API Calls                         │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Backend API (app.py)                                │   │
│  │  • Python Flask Server                               │   │
│  │  • RESTful API                                       │   │
│  │  • Handles all business logic                        │   │
│  │  • Runs on Gunicorn (production server)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                   │
│                           │ SQL Queries                       │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PostgreSQL Database                                 │   │
│  │  • facility_groups                                   │   │
│  │  • facilities                                        │   │
│  │  • billing_records                                   │   │
│  │  • custom_dates                                      │   │
│  │  • settings                                          │   │
│  │  [Automatic Backups Included]                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Examples

### Example 1: Loading the App

```
User opens: billing.aredgegroup.com
    │
    ▼
Railway serves: billing_tracker.html
    │
    ▼
Browser loads React app
    │
    ▼
React makes API calls:
    • GET /api/facility-groups
    • GET /api/billing-records
    • GET /api/settings
    │
    ▼
Flask API queries PostgreSQL
    │
    ▼
Database returns data
    │
    ▼
Flask sends JSON to browser
    │
    ▼
React displays billing tracker
```

### Example 2: Saving a Billing Record

```
User edits "Paid Amount" → clicks Save
    │
    ▼
React calls: POST /api/billing-records
    │
    ▼
Flask receives JSON data
    │
    ▼
database.py validates and saves
    │
    ▼
PostgreSQL writes to billing_records table
    │
    ▼
PostgreSQL confirms write
    │
    ▼
Flask returns: { "success": true }
    │
    ▼
React shows success, updates UI
```

### Example 3: Adding a New Facility

```
User clicks "Add Facility" in Settings
    │
    ▼
React calls: POST /api/facilities
    │
    ▼
Flask receives: { "name": "New Facility", "groupId": 1 }
    │
    ▼
database.py inserts into facilities table
    │
    ▼
PostgreSQL returns new facility ID
    │
    ▼
Flask returns: { "id": 5, "success": true }
    │
    ▼
React adds facility to local state
    │
    ▼
User sees new facility immediately
```

---

## API Endpoints

### Facility Groups
```
GET    /api/facility-groups         → List all groups
POST   /api/facility-groups         → Create new group
PUT    /api/facility-groups/:id     → Update group
DELETE /api/facility-groups/:id     → Delete group
```

### Facilities
```
GET    /api/facilities              → List all facilities
POST   /api/facilities              → Create new facility
DELETE /api/facilities/:id          → Delete facility
```

### Billing Records
```
GET    /api/billing-records         → List all records
POST   /api/billing-records         → Create/update record
```

### Custom Dates
```
GET    /api/custom-dates/:groupId   → Get custom dates for group
POST   /api/custom-dates            → Save custom dates
```

### Settings
```
GET    /api/settings                → Get all settings
POST   /api/settings                → Save settings
```

### Health Check
```
GET    /api/health                  → Check if API is running
```

---

## Technology Stack

### Frontend
- **Framework:** React 18
- **Styling:** Tailwind CSS
- **State Management:** React Hooks (useState, useEffect)
- **HTTP Client:** Fetch API

### Backend
- **Language:** Python 3.11
- **Framework:** Flask 3.0
- **WSGI Server:** Gunicorn 21.2
- **Database Driver:** psycopg2 2.9

### Database
- **Type:** PostgreSQL 15
- **Hosting:** Railway (managed)
- **Backups:** Automatic (Railway handles)

### Hosting
- **Platform:** Railway.app
- **SSL:** Automatic (Let's Encrypt)
- **CDN:** Included
- **Region:** US (default, can change)

---

## Security Features

### Transport Security
- ✅ All connections use HTTPS
- ✅ SSL certificate auto-renewed
- ✅ TLS 1.3 supported

### Database Security
- ✅ Not publicly accessible
- ✅ Only backend can connect
- ✅ Encrypted connections
- ✅ Railway manages credentials

### Application Security
- ✅ CORS configured properly
- ✅ SQL injection prevented (parameterized queries)
- ✅ Input validation on backend
- ✅ Error messages sanitized

---

## Scalability

### Current Setup (Small Team)
- **Users:** 1-10 simultaneous
- **Requests:** ~100-500 per day
- **Database Size:** <100 MB
- **Cost:** $0-5/month

### If You Need to Scale
- **10-50 users:** Upgrade to $20/month Railway plan
- **50-200 users:** Consider dedicated database
- **200+ users:** Contact Railway for enterprise

### What Scales Automatically
- ✅ Database connections (pooling)
- ✅ Request handling (Gunicorn workers)
- ✅ SSL termination
- ✅ Database backups

### What Doesn't Scale (Yet)
- ⚠️ Single server instance
- ⚠️ No load balancing (not needed for small team)
- ⚠️ No caching (add Redis if needed)

---

## Monitoring & Logs

### Available in Railway Dashboard

**Metrics:**
- CPU usage
- Memory usage
- Request count
- Response times
- Database connections

**Logs:**
- Application logs (Flask)
- Database logs (PostgreSQL)
- Deployment logs
- Error logs

**Alerts:**
- Deployment failures
- High resource usage
- Downtime alerts

---

## Backup & Recovery

### Automatic Backups
- **Frequency:** Daily (Railway handles)
- **Retention:** 7 days (free tier)
- **Location:** Railway's infrastructure
- **Recovery:** Via Railway dashboard

### Manual Backups
- **Database:** Export via Railway dashboard
- **Code:** Git repository (GitHub)
- **Settings:** Stored in database

### Disaster Recovery
1. Code is in GitHub (always safe)
2. Database has automatic backups
3. Can redeploy from scratch in minutes
4. Restore database from backup if needed

---

## Development Workflow

### Local Development (Optional)
```bash
# 1. Clone repo
git clone https://github.com/yourusername/billing-tracker.git

# 2. Install dependencies
cd billing-tracker/backend
pip install -r requirements.txt

# 3. Set environment variable
export DATABASE_URL="postgresql://localhost/billing_tracker"

# 4. Run locally
python app.py

# 5. Open browser
# http://localhost:5000
```

### Making Changes
```bash
# 1. Edit files
# 2. Test locally (optional)
# 3. Commit
git add .
git commit -m "Your changes"

# 4. Push
git push

# 5. Railway auto-deploys
# (wait 2-3 minutes)

# 6. Test at your URL
```

---

## Cost Optimization Tips

### Stay in Free Tier
- Use Railway's $5/month free credit
- Monitor usage weekly
- Typical small team: $3-5/month

### If You Need More
- $20/month plan gives $20 in credits
- Good for 10-20 users
- Includes better support

### What Uses Credits
- **Backend:** ~$0.10/day (~$3/month)
- **Database:** ~$0.07/day (~$2/month)
- **Total:** ~$5/month for small team

### What's Free
- SSL certificates
- Domain hosting
- Deployment
- Git integration
- Basic monitoring

---

## Future Enhancements (Ideas)

### Easy Additions
- Email notifications for unpaid bills
- Export to Excel/CSV
- User authentication (login required)
- Audit log (who changed what)

### Medium Additions
- Multiple organizations support
- Role-based permissions
- API tokens for integrations
- Mobile responsive improvements

### Advanced Additions
- Integrate with accounting software
- Automated billing reminders
- Analytics dashboard
- Mobile app

---

## Comparison: This vs Alternatives

### vs Shared Drive + CSV
| Feature | This Solution | CSV Solution |
|---------|--------------|--------------|
| Multi-user | ✅ Perfect | ⚠️ File locking issues |
| Always available | ✅ 24/7 | ⚠️ Depends on computer |
| Professional URL | ✅ Custom domain | ❌ No URL |
| Automatic backups | ✅ Yes | ⚠️ Manual |
| Cost | $0-5/month | $0 |

### vs Google Sheets
| Feature | This Solution | Google Sheets |
|---------|--------------|---------------|
| Custom UI | ✅ Perfect | ❌ Spreadsheet only |
| Performance | ✅ Fast | ⚠️ Slower with formulas |
| Automation | ✅ Full control | ⚠️ Limited |
| Professional | ✅ Very | ⚠️ Less so |
| Cost | $0-5/month | $0 |

### vs AWS
| Feature | This Solution | AWS |
|---------|--------------|-----|
| Setup time | 15 minutes | 2-4 hours |
| Cost | $0-5/month | $15-40/month |
| Maintenance | Low | High |
| Complexity | Low | High |
| Features | Same | Same |

---

**This architecture is production-ready and will serve your team well!**
