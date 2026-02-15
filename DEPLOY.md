# 🚀 Quick Deployment Guide for Render

## Before You Start
✅ Make sure you have your `plant_diseases_model.h5` file ready!

## Steps to Deploy:

### 1️⃣ Add Your Model File
```bash
# Copy your model file to this directory
cp /path/to/your/plant_diseases_model.h5 ./
```

### 2️⃣ Push to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy AgriPal to Render"

# Create GitHub repo and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agripal.git
git push -u origin main
```

### 3️⃣ Deploy on Render

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in these settings:
   - **Name**: `agripal`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - Click **"Create Web Service"**

### 4️⃣ Wait for Deployment
⏱️ First deployment takes 5-10 minutes

### 5️⃣ Access Your App
🎉 Your app will be live at: `https://agripal.onrender.com`

## Important Notes:

⚠️ **Free Tier Behavior**:
- App sleeps after 15 min of inactivity
- First request after sleep takes 30-60 seconds

💾 **Model File Size**:
- If your model is >100MB, you may need to:
  - Use Git LFS (Large File Storage)
  - Host model on external storage (AWS S3, Google Cloud)
  - Upgrade to paid Render plan

## Troubleshooting:

**Build Failed?**
- Check that `plant_diseases_model.h5` exists in root directory
- Review Render build logs

**App Not Starting?**
- Check Render runtime logs
- Verify Python version (3.11.7)

**Need Help?**
- Check the full README.md for detailed instructions
- Review Render documentation: https://render.com/docs

---

Good luck! 🌱
