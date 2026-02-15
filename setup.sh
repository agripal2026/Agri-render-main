#!/bin/bash

# AgriPal Render Deployment Setup Script
# This script helps you prepare your project for Render deployment

echo "🌱 AgriPal - Render Deployment Setup"
echo "===================================="
echo ""

# Check if model file exists
if [ ! -f "plant_diseases_model.h5" ]; then
    echo "⚠️  WARNING: Model file not found!"
    echo "   Please add 'plant_diseases_model.h5' to this directory"
    echo "   Your app will not work without this file."
    echo ""
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
else
    echo "✅ Git already initialized"
    echo ""
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
.venv
.DS_Store
*.log
EOF
    echo "✅ .gitignore created"
    echo ""
fi

echo "📋 Current Status:"
echo "=================="
echo ""

# Check required files
files=("main.py" "requirements.txt" "Procfile" "runtime.txt")
all_present=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING!"
        all_present=false
    fi
done

# Check directories
if [ -d "templates" ]; then
    echo "✅ templates/"
else
    echo "❌ templates/ - MISSING!"
    all_present=false
fi

if [ -d "static" ]; then
    echo "✅ static/"
else
    echo "❌ static/ - MISSING!"
    all_present=false
fi

# Check model file
if [ -f "plant_diseases_model.h5" ]; then
    echo "✅ plant_diseases_model.h5"
else
    echo "⚠️  plant_diseases_model.h5 - MISSING (REQUIRED!)"
    all_present=false
fi

echo ""
echo "📊 File Sizes:"
echo "=============="
if [ -f "plant_diseases_model.h5" ]; then
    size=$(du -h "plant_diseases_model.h5" | cut -f1)
    echo "   Model file: $size"
    echo "   Note: Files >100MB may need Git LFS"
fi

echo ""
echo "🚀 Next Steps:"
echo "=============="
echo ""

if [ "$all_present" = false ]; then
    echo "❌ Some required files are missing!"
    echo "   Please check the list above and add missing files."
    echo ""
    exit 1
fi

echo "1. Add your changes to git:"
echo "   git add ."
echo ""
echo "2. Commit your changes:"
echo "   git commit -m 'Prepare for Render deployment'"
echo ""
echo "3. Create a GitHub repository and add remote:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/agripal.git"
echo ""
echo "4. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "5. Deploy on Render:"
echo "   - Go to https://dashboard.render.com"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repo"
echo "   - Configure and deploy!"
echo ""
echo "✅ Your project is ready for deployment!"
echo ""
echo "📚 For detailed instructions, see:"
echo "   - README.md (complete guide)"
echo "   - DEPLOY.md (quick start)"
echo "   - CHECKLIST.md (step-by-step checklist)"
echo ""
