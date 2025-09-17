# 🚀 Manual Deployment Guide - Render.com

If automatic deployment fails, please follow these steps for manual deployment:

## Step 1: Create Render.com Account

1. Visit [render.com](https://render.com)
2. Sign in with your GitHub account
3. Connect your GitHub account

## Step 2: Create Database

1. In the Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Set database name: `pet-finder-db`
3. Select **"Free"** plan
4. Click **"Create Database"**
5. Wait for database creation to complete
6. Note down the database connection information

## Step 3: Create Web Service

1. In the Render dashboard, click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Choose your `pet-finder` repository
4. Click **"Connect"**

## Step 4: Configure Deployment Settings

### Basic Settings:
- **Name**: `pet-finder`
- **Environment**: `Python 3`
- **Region**: Choose the region closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty

### Build & Deploy Settings:
- **Build Command**: 
  ```bash
  pip install --upgrade pip && pip install -r requirements-prod.txt && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```bash
  python manage.py migrate && gunicorn scraper.wsgi:application
  ```

### Environment Variables:
Click **"Advanced"** → **"Add Environment Variable"**, add the following variables:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Click "Generate" to create a new key |
| `ALLOWED_HOSTS` | Leave empty (automatically includes Render domains) |
| `DATABASE_URL` | Copy connection string from the database created in Step 2 |

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (approximately 5-10 minutes)
3. Check deployment logs to ensure no errors

## Step 6: Test Deployment

1. After deployment is complete, you will receive a URL (e.g., `https://pet-finder.onrender.com`)
2. Visit the URL to test if the website works properly
3. Test the search functionality
4. Confirm that static files (CSS, JS, images) load correctly

## Troubleshooting Common Issues

### Issue 1: Deployment Failed
- Check if Build Command is correct
- Confirm all environment variables are set
- View deployment logs for error information

### Issue 2: Website Unreachable
- Check `ALLOWED_HOSTS` environment variable
- Confirm URL is correct

### Issue 3: Database Connection Error
- Check `DATABASE_URL` environment variable
- Confirm database service is running

### Issue 4: Static Files Not Loading
- Confirm `whitenoise` is properly configured
- Check if `collectstatic` command executed successfully

## Automatic Redeployment

After successful deployment, every time you push code to the `main` branch on GitHub, Render will automatically:
1. Detect code changes
2. Rebuild the application
3. Redeploy

## Monitoring and Maintenance

1. **View Logs**: Check real-time logs in the Render dashboard
2. **Monitor Performance**: Check CPU and memory usage
3. **Backup Data**: Regularly backup PostgreSQL database

## Free Tier Limitations

- Application sleeps after 15 minutes of inactivity
- Restart takes 30 seconds
- Monthly usage limits
- Database storage limits

## Upgrade Options

If you need better performance, consider upgrading to a paid plan:
- Faster startup time
- More resources
- Better support