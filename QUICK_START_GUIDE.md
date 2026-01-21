# Quick Start Guide - News & Chat Control

## 🚀 Getting Started

### Step 1: Start the Backend Server

Make sure your PostgreSQL database is running and the backend server is started:

```bash
cd backend
python app.py
```

The server should start on `http://localhost:5000`

---

## 📰 Managing News Articles

### Add Your First News Article

1. **Open Admin Panel**
   - Navigate to: `http://localhost:5000/admin/pages/news.html`
   - Login with your admin credentials

2. **Click "Add News Article" Button**

3. **Fill in the Form**
   ```
   Title: Free Medical Camp at Quthbullapur
   Category: Event
   Date: 2026-01-25
   Summary: BKR Foundation organizing free health checkup camp for all residents
   Content: [Full details about the event...]
   ```

4. **Add a Photo (Choose One)**
   - **Upload File**: Click "Upload Image" → Select image from computer
   - **Use URL**: Paste image URL like: `https://example.com/camp-photo.jpg`
   - **Use Local**: Use existing images: `images/IMG-20240511-WA0053.jpg`

5. **Set Status**
   - ✅ Published (shows on homepage immediately)
   - ⬜ Draft (saved but hidden)

6. **Click "Publish Article"**

7. **View on Homepage**
   - Open `http://localhost:5000/`
   - Scroll to "News & Updates" section
   - Your article should appear!

### Edit Existing News

1. Go to News management page
2. Find your article in the table
3. Click the ✏️ (edit) icon
4. Modify any field
5. Click "Update Article"

### Delete News

1. Click the 🗑️ (trash) icon next to any article
2. Confirm deletion
3. Article removed from database and homepage

---

## 🤖 Control Chat Page Visibility

### Hide the Chat Page

1. **Open Settings**
   - Navigate to: `http://localhost:5000/admin/pages/settings.html`

2. **Find "Enable AI Chat Page" Toggle**
   - It's in the "General Settings" section
   - Toggle it to OFF position

3. **Click "Save Settings" Button**

4. **Verify**
   - Open homepage: `http://localhost:5000/`
   - The AI chatbot button should be HIDDEN from navigation

### Show the Chat Page

1. Go to Settings page
2. Toggle "Enable AI Chat Page" to ON
3. Click "Save Settings"
4. Refresh homepage - AI button appears in navigation!

---

## 🎯 Common Scenarios

### Scenario 1: Add News with Uploaded Photo

```javascript
// Admin does this through UI:
1. Click "Add News Article"
2. Fill: Title = "New Initiative Announced"
3. Fill: Category = "Announcement"
4. Fill: Date = today
5. Fill: Summary = "Brief description..."
6. Fill: Content = "Full details..."
7. Click "Upload Image" → Choose file
8. Wait for upload (image URL auto-fills)
9. Click "Publish Article"
```

### Scenario 2: Temporarily Disable Chat

```javascript
// For maintenance or other reasons:
1. Go to Settings
2. Turn OFF "Enable AI Chat Page"
3. Save Settings
// Chat page link now hidden from all users
```

### Scenario 3: Update Old News Article

```javascript
1. Go to News management
2. Find the old article
3. Click edit icon
4. Change date to today
5. Update content
6. Click "Update Article"
// Updated news appears on homepage
```

---

## 🔧 Troubleshooting

### News Not Appearing on Homepage

**Check:**
1. Is article status "published"? (not draft)
2. Is backend server running?
3. Check browser console for errors
4. Try refreshing the page

**Fix:**
```javascript
// Open browser console (F12) and run:
fetch('/api/news')
  .then(r => r.json())
  .then(d => console.log(d))
// Should show your news articles
```

### Chat Page Still Visible After Disabling

**Check:**
1. Did you click "Save Settings"?
2. Did you refresh the homepage?
3. Clear browser cache

**Fix:**
```javascript
// Check settings in browser console:
fetch('/api/settings/chat_page_enabled')
  .then(r => r.json())
  .then(d => console.log(d))
// Should show { chat_page_enabled: "false" }
```

### Image Not Displaying

**Options:**
1. **Use existing images** from your images folder
2. **Use external URL** (must be publicly accessible)
3. **Upload file** (needs upload endpoint implementation)

**Example URLs that work:**
```
images/IMG-20240511-WA0053.jpg
images/IMG-20240511-WA0047.jpg
images/IMG-20240511-WA0037.jpg
https://via.placeholder.com/600x400
```

---

## 📊 API Testing with Browser Console

### Get All News
```javascript
fetch('/api/news')
  .then(r => r.json())
  .then(d => console.log(d));
```

### Get Settings
```javascript
fetch('/api/settings')
  .then(r => r.json())
  .then(d => console.log(d));
```

### Create News (Requires API Key)
```javascript
fetch('/api/news', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'bkr-secret-key-2024'
  },
  body: JSON.stringify({
    title: 'Test News',
    category: 'announcement',
    date: '2026-01-20',
    summary: 'Test summary',
    content: 'Test content',
    image_url: 'images/IMG-20240511-WA0053.jpg',
    status: 'published'
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### Update Setting (Requires API Key)
```javascript
fetch('/api/settings', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'bkr-secret-key-2024'
  },
  body: JSON.stringify({
    chat_page_enabled: 'false'
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

---

## ✅ Testing Checklist

Run through this checklist to verify everything works:

### News Management
- [ ] Add news article with title and content
- [ ] Add news with image URL
- [ ] View news on homepage
- [ ] Edit news article
- [ ] Delete news article
- [ ] Create draft article (should not appear on homepage)
- [ ] Publish draft article (should appear on homepage)

### Chat Page Control
- [ ] Disable chat page in settings
- [ ] Verify chat button disappears from homepage
- [ ] Enable chat page in settings
- [ ] Verify chat button reappears
- [ ] Refresh page - settings persist

---

## 🎓 Tips & Best Practices

### News Management
1. **Use descriptive titles** - Make them SEO-friendly
2. **Keep summaries short** - 1-2 sentences max
3. **Optimize images** - Compress before upload
4. **Use categories consistently** - Helps with organization
5. **Update old news** - Keep content fresh

### Images
1. **Recommended size**: 600x400 pixels
2. **Max file size**: 5MB
3. **Supported formats**: JPG, PNG, GIF, WebP
4. **Use compression** - Tools like TinyPNG

### Settings
1. **Test before saving** - Preview changes
2. **Document changes** - Note why settings changed
3. **Communicate** - Tell team about visibility changes

---

## 📞 Need Help?

If you encounter issues:

1. **Check the documentation**: `NEWS_AND_CHAT_CONTROL_IMPLEMENTATION.md`
2. **View browser console**: Press F12 → Console tab
3. **Check server logs**: Terminal running backend server
4. **Verify database**: Ensure PostgreSQL is running

---

## 🎉 You're All Set!

Both features are now ready to use. Start by adding your first news article and experimenting with the chat page toggle!

**Happy managing! 📰🤖**
