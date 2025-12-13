#!/bin/bash
# Quick Deployment Script for BKR Website

echo "=========================================="
echo "BKR Website - Deployment Preparation"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already exists"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📝 Uncommitted changes detected"
    read -p "Commit message: " commit_msg
    
    if [ -z "$commit_msg" ]; then
        commit_msg="Update for deployment"
    fi
    
    git add .
    git commit -m "$commit_msg"
    echo "✓ Changes committed"
else
    echo "✓ No uncommitted changes"
fi

# Check for remote
if ! git remote | grep -q "origin"; then
    echo ""
    echo "🔗 No remote repository found"
    read -p "Enter GitHub repository URL: " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✓ Remote added"
    fi
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✓ Successfully pushed to GitHub!"
    echo ""
    echo "=========================================="
    echo "Next Steps:"
    echo "=========================================="
    echo "1. Go to your Hostinger EasyPanel"
    echo "2. Create new Python app for backend"
    echo "3. Connect to your GitHub repository"
    echo "4. Set environment variables (see DEPLOYMENT_GUIDE.md)"
    echo "5. Deploy backend"
    echo "6. Update js/api-service.js with backend URL"
    echo "7. Upload frontend files to public_html"
    echo ""
    echo "📖 Full guide: DEPLOYMENT_GUIDE.md"
    echo "=========================================="
else
    echo "❌ Push failed. Check your credentials and try again."
fi
