# AgriPal - Plant Disease Detection System

A Flask-based web application for detecting plant diseases using machine learning.

## 🚀 Deployment Instructions for Render

### Prerequisites
- A GitHub account
- A Render account (free tier available at https://render.com)
- Your trained model file: `plant_diseases_model.h5`

### Step 1: Prepare Your Files

1. **IMPORTANT**: Add your `plant_diseases_model.h5` file to the root directory of this project
   - This file is NOT included in the repository due to size constraints
   - You must upload your trained model file

2. **Add placeholder images** (optional):
   - Place images in `static/images/` folder
   - Files needed: `imgs1.jpg` and `imgs2.jpg`
   - Or update `index.html` to remove image references

### Step 2: Push to GitHub

1. Create a new repository on GitHub
2. Initialize git and push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 3: Deploy to Render

1. **Log in to Render**: Go to https://render.com and sign in

2. **Create a New Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the repository you just created

3. **Configure Your Web Service**:
   - **Name**: `agripal` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Instance Type**: Free (or paid if needed)

4. **Environment Variables** (if needed):
   - Click "Advanced" 
   - Add any environment variables if required
   - Example: `FLASK_ENV=production`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - First deployment takes 5-10 minutes

### Step 4: Verify Deployment

1. Once deployed, Render provides a URL like: `https://agripal.onrender.com`
2. Visit the URL to test your application
3. Upload a plant image to verify the disease detection works

## 📁 Project Structure

```
agripal-deploy/
├── main.py                      # Flask application
├── requirements.txt             # Python dependencies
├── Procfile                     # Process file for Render
├── runtime.txt                  # Python version specification
├── plant_diseases_model.h5      # ML model (YOU NEED TO ADD THIS)
├── templates/
│   ├── index.html              # Home page
│   └── result.html             # Results page
└── static/
    ├── uploads/                # Uploaded images stored here
    └── images/                 # Static images for UI
        ├── imgs1.jpg          # (Optional - add your own)
        └── imgs2.jpg          # (Optional - add your own)
```

## ⚙️ Configuration Details

### Requirements (requirements.txt)
- Flask 3.0.0
- flask-cors 4.0.0
- Pillow 10.2.0
- numpy 1.26.3
- tensorflow 2.15.0
- gunicorn 21.2.0

### Supported Plant Diseases
The model can detect 38 different plant conditions including:
- Apple diseases (scab, black rot, cedar rust, healthy)
- Tomato diseases (bacterial spot, early/late blight, leaf mold, etc.)
- Corn diseases (gray leaf spot, rust, northern leaf blight, healthy)
- And many more...

## 🔧 Troubleshooting

### Common Issues:

1. **Build fails**: 
   - Check that `plant_diseases_model.h5` is in the root directory
   - Verify all dependencies in `requirements.txt` are correct

2. **App crashes on startup**:
   - Check Render logs for error messages
   - Ensure model file is accessible
   - Verify Python version compatibility

3. **Images not displaying**:
   - Check that image paths in HTML templates are correct
   - Verify static folder structure

4. **Predictions not working**:
   - Ensure model file is loaded correctly
   - Check that uploaded images are saved properly
   - Verify the UPLOAD_FOLDER path

## 📝 Notes

- **Free Tier Limitations**: Render's free tier spins down after inactivity. First request after inactivity may take 30-60 seconds.
- **Model Size**: If your model is very large (>100MB), consider using external storage or upgrading Render plan
- **HTTPS**: Render provides free SSL certificates automatically

## 🆘 Support

If you encounter issues:
1. Check Render deployment logs
2. Verify all files are committed to GitHub
3. Ensure model file is present and accessible
4. Check that all dependencies are compatible

## 📄 License

This project is for educational and agricultural purposes.

---

**Happy Farming! 🌱**
