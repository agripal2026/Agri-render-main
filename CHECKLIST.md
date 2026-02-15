# 📋 Deployment Checklist for AgriPal

Use this checklist to ensure everything is ready before deploying:

## Pre-Deployment Checklist

### Required Files
- [ ] `main.py` - Flask application ✅ (included)
- [ ] `requirements.txt` - Python dependencies ✅ (included)
- [ ] `Procfile` - Render configuration ✅ (included)
- [ ] `runtime.txt` - Python version ✅ (included)
- [ ] `plant_diseases_model.h5` - **YOU MUST ADD THIS** ⚠️

### HTML Templates
- [ ] `templates/index.html` ✅ (included)
- [ ] `templates/result.html` ✅ (included)

### Static Files
- [ ] `static/images/imgs1.jpg` (optional)
- [ ] `static/images/imgs2.jpg` (optional)
- [ ] `static/uploads/` folder created ✅ (auto-created)

### GitHub Setup
- [ ] Created GitHub repository
- [ ] Added all files to git
- [ ] Pushed to GitHub
- [ ] Repository is public or connected to Render

### Render Setup
- [ ] Created Render account
- [ ] Connected GitHub account to Render
- [ ] Created new Web Service
- [ ] Configured build settings
- [ ] Started deployment

## Post-Deployment Checklist

### Testing
- [ ] App deployed successfully (no build errors)
- [ ] Home page loads correctly
- [ ] Image upload form works
- [ ] Can upload and analyze plant images
- [ ] Disease detection results display properly
- [ ] Chatbot responds to questions
- [ ] Google Translate widget works
- [ ] Responsive design works on mobile

### Monitoring
- [ ] Check Render logs for errors
- [ ] Monitor app performance
- [ ] Test with different image types
- [ ] Verify all 38 disease classes work

## Common Issues & Solutions

### ❌ Build Fails
**Solution**: 
- Verify all files are committed
- Check `requirements.txt` for typos
- Ensure model file exists

### ❌ App Crashes
**Solution**:
- Check Render logs for error messages
- Verify model file path is correct
- Check Python version compatibility

### ❌ Slow First Load
**Explanation**: 
- Free tier spins down after 15 min
- This is normal behavior
- Consider paid tier for always-on service

### ❌ Images Don't Display
**Solution**:
- Add images to `static/images/`
- Or remove image references from HTML
- Check file paths in templates

## Environment Variables (Optional)

If you need environment variables, add these in Render dashboard:

```
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216  # 16MB file upload limit
```

## Render Free Tier Limits

- ✅ 750 hours/month
- ✅ Auto-sleep after 15 min inactivity
- ✅ 512MB RAM
- ✅ Free SSL certificate
- ⚠️ Slower cold starts

## Ready to Deploy?

If all required items are checked ✅, you're ready to deploy!

Follow the steps in DEPLOY.md or README.md for detailed instructions.

---

**Good luck with your deployment! 🚀🌱**
