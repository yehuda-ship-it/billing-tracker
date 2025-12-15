# AR Edge Group - Customer Deployment Guide

## Overview

This guide covers deploying **Billing Tracker** and **Month End Tracker** for new customers on Railway.

---

## Prerequisites

- Customer creates a Railway account at [railway.app](https://railway.app)
- You have access to their Railway account (or they share screen)

---

## Deployment Steps

### Step 1: Create New Project

1. Log into customer's Railway account
2. Click **New Project** → **Empty Project**
3. Name it (e.g., "CustomerName-Billing")

---

### Step 2: Add PostgreSQL Database

1. Click **+ New** → **Database** → **Add PostgreSQL**
2. Wait for it to provision (green checkmark)

---

### Step 3: Deploy Billing Tracker

1. Click **+ New** → **Docker Image**
2. Enter: `aredgegroup/billing-tracker:latest`
3. Click **Deploy**
4. Go to **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Click **Add Reference** → Select **PostgreSQL** |
| `SECRET_KEY` | Enter: `[customer-name]-billing-2024` |

5. Go to **Settings** tab → **Networking** → Click **Generate Domain**
6. Copy the URL (e.g., `billing-tracker-production-xxxx.up.railway.app`)

---

### Step 4: Deploy Month End Tracker

1. Click **+ New** → **Docker Image**
2. Enter: `aredgegroup/month-end-tracker:latest`
3. Click **Deploy**
4. Go to **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Click **Add Reference** → Select **PostgreSQL** |
| `SECRET_KEY` | Enter: `[customer-name]-monthend-2024` |

5. Go to **Settings** tab → **Networking** → Click **Generate Domain**
6. Copy the URL (e.g., `month-end-tracker-production-xxxx.up.railway.app`)

---

### Step 5: Link the Apps

1. Open the Month End Tracker URL
2. Go to **Settings** → **Billing Tracker Link**
3. Paste the Billing Tracker URL
4. Click **Save**

---

## Initial App Configuration

### Billing Tracker Setup

1. Open Billing Tracker URL
2. Go to **Settings** → **Groups** → Add customer's groups
3. Go to **Settings** → **Facilities** → Add facilities to each group
4. Go to **Settings** → **Statuses** → Configure billing statuses (if needed)

### Month End Tracker Setup

1. Open Month End Tracker URL
2. Go to **Settings** → **Groups** → Add same groups as Billing Tracker
3. Go to **Settings** → **Facilities** → Add facilities to each group
4. Go to **Settings** → **Task Tabs** → Create task categories:
   - AR Review
   - Cash Posting
   - Claims Submission
   - Reconciliation
   - (or customer-specific tabs)
5. Go to **Settings** → **Tasks** → Add tasks to each tab
6. Go to **Settings** → **N/A Overrides** → Mark any facility-task combos as N/A

---

## Pushing Updates to Customers

### When You Release an Update:

**Step 1:** Build and push new Docker images

```bash
cd C:\Users\YehudaTauber\billing-tracker
docker build -t aredgegroup/billing-tracker:latest .
docker push aredgegroup/billing-tracker:latest

cd C:\Users\YehudaTauber\month-end-tracker
docker build -t aredgegroup/month-end-tracker:latest .
docker push aredgegroup/month-end-tracker:latest
```

**Step 2:** For each customer:
1. Log into their Railway account
2. Click on the service (Billing Tracker or Month End Tracker)
3. Go to **Settings** tab
4. Click **Redeploy**

Or tell customer: "Go to Railway → Click on the app → Settings → Redeploy"

---

## Troubleshooting

### App won't start
- Check **Variables** tab - make sure `DATABASE_URL` is linked to PostgreSQL
- Check **Deployments** tab for error logs

### Database connection error
- Go to PostgreSQL service → **Variables** → Copy `DATABASE_URL`
- Go to app service → **Variables** → Make sure `DATABASE_URL` matches

### App shows old version after update
- Go to **Settings** → Click **Redeploy**
- Or: **Deployments** tab → Click **Redeploy** on latest

---

## Customer Information to Record

For each customer, save:

| Field | Value |
|-------|-------|
| Customer Name | |
| Railway Account Email | |
| Billing Tracker URL | |
| Month End Tracker URL | |
| Setup Date | |
| Groups | |
| Number of Facilities | |

---

## Pricing Notes

Railway charges based on usage. Typical costs:
- **PostgreSQL:** ~$5-10/month
- **Each App:** ~$5-10/month
- **Total:** ~$15-30/month per customer

Customer pays Railway directly for hosting.

---

## Support Contact

AR Edge Group
[Your contact info here]
