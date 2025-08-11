#!/bin/bash

echo "🕷️  Spider Portfolio Deployment Script"
echo "======================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "Adding files to Git..."
git add .

# Commit changes
echo "Committing changes..."
read -p "Enter commit message (default: 'Deploy Spider Portfolio'): " commit_msg
commit_msg=${commit_msg:-"Deploy Spider Portfolio"}
git commit -m "$commit_msg"

echo ""
echo "🚀 Deployment Options:"
echo "1. GitHub + Heroku"
echo "2. GitHub + Vercel"
echo "3. GitHub + Railway"
echo "4. Just push to GitHub"

read -p "Choose deployment option (1-4): " choice

case $choice in
    1)
        echo "Setting up for Heroku deployment..."
        echo "1. Create a Heroku account at https://heroku.com"
        echo "2. Install Heroku CLI"
        echo "3. Run: heroku login"
        echo "4. Run: heroku create your-spider-portfolio"
        echo "5. Set environment variables:"
        echo "   heroku config:set SESSION_SECRET=your-secret-key"
        echo "   heroku config:set SMTP_SERVER=smtp.gmail.com"
        echo "   heroku config:set SMTP_PORT=587"
        echo "   heroku config:set SMTP_USERNAME=your-email"
        echo "   heroku config:set SMTP_PASSWORD=your-password"
        echo "6. Run: git push heroku main"
        ;;
    2)
        echo "Setting up for Vercel deployment..."
        echo "1. Push to GitHub first"
        echo "2. Visit vercel.com and connect your GitHub repo"
        echo "3. Add environment variables in Vercel dashboard"
        echo "4. Deploy automatically"
        ;;
    3)
        echo "Setting up for Railway deployment..."
        echo "1. Push to GitHub first"
        echo "2. Visit railway.app and connect your GitHub repo"
        echo "3. Add environment variables in Railway dashboard"
        echo "4. Deploy automatically"
        ;;
    4)
        echo "Just pushing to GitHub..."
        ;;
esac

# Push to GitHub
if [ -n "$GITHUB_REPO" ]; then
    echo "Pushing to GitHub repository..."
    git remote add origin $GITHUB_REPO
    git push -u origin main
else
    echo ""
    echo "📋 Next Steps:"
    echo "1. Create a new repository on GitHub"
    echo "2. Copy the repository URL"
    echo "3. Run these commands:"
    echo "   git remote add origin <your-repo-url>"
    echo "   git push -u origin main"
fi

echo ""
echo "✅ Deployment preparation complete!"
echo "Your Spider Portfolio is ready for deployment! 🕷️"