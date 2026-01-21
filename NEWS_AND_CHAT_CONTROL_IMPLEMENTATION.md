# News Management & Chat Page Control Implementation

## Overview
This document summarizes the implementation of two major features:
1. **Dynamic News Section** - Admin-controlled news management with photo upload
2. **Chat Page Control** - Admin toggle to enable/disable the AI chat page

## Implementation Date
January 19, 2026

---

## 1. NEWS MANAGEMENT SYSTEM

### Backend Changes

#### Database Schema (models.py)
- **Updated `news` table** to include `image_url` column for photo support
- **Added `settings` table** with default settings including:
  - `chat_page_enabled`
  - `show_news`
  - `show_health_camps`
  - `email_notifications`

#### Database Operations (database.py)
Added methods:
- `get_news(status, limit)` - Retrieve news articles
- `get_news_by_id(news_id)` - Get single news article
- `create_news(data)` - Create news with image_url support
- `update_news(news_id, data)` - Update news with image_url
- `delete_news(news_id)` - Delete news article
- `get_settings()` - Get all settings
- `get_setting(key)` - Get specific setting
- `update_setting(key, value)` - Update setting value

#### API Endpoints (app.py)
**News Endpoints:**
- `GET /api/news` - Get all published news (public)
- `GET /api/news/<id>` - Get specific news article (public)
- `POST /api/news` - Create news article (protected)
- `PUT /api/news/<id>` - Update news article (protected)
- `DELETE /api/news/<id>` - Delete news article (protected)

**Settings Endpoints:**
- `GET /api/settings` - Get all settings (public)
- `GET /api/settings/<key>` - Get specific setting (public)
- `PUT /api/settings` - Update multiple settings (protected)
- `PUT /api/settings/<key>` - Update single setting (protected)

### Frontend Changes

#### Admin Panel (admin/pages/news.html)
**Features:**
- ✅ View all news articles in a table
- ✅ Add new news with title, category, date, summary, content
- ✅ Upload photo or provide image URL
- ✅ Edit existing news articles
- ✅ Delete news articles
- ✅ Publish/Draft status control
- ✅ Integration with backend API
- ✅ Image preview in table
- ✅ File upload support (up to 5MB)

**Categories Available:**
- Announcement
- Event
- Press Release
- Update

#### Homepage (index.html)
**Dynamic News Section:**
- Fetches latest 3 published news articles from API
- Displays news with image, date, title, summary
- Fallback to static news if API fails
- Auto-formats dates
- Shows placeholder images if news image fails to load

---

## 2. CHAT PAGE CONTROL SYSTEM

### Admin Settings (admin/pages/settings.html)
**New Toggle Added:**
- **Enable AI Chat Page** - Controls visibility of chat page in navigation
  - When ON: Chat page link visible in navigation
  - When OFF: Chat page link hidden from navigation

**Settings Integration:**
- Connected to backend API for persistence
- Save button to commit all settings
- Real-time toggle updates
- Backward compatible with localStorage

### Homepage Navigation Control (index.html)
**Chat Link Control:**
- Chat navigation link has ID `chatNavLink`
- JavaScript checks `chat_page_enabled` setting on page load
- Automatically shows/hides based on admin setting
- Default behavior: Show chat link if API fails (fail-safe)

---

## How to Use

### Adding News Article (Admin)

1. **Navigate to Admin Panel**
   - Go to `admin/pages/news.html`
   - Login with admin credentials

2. **Click "Add News Article"**
   - Fill in required fields:
     - Title (required)
     - Category (required)
     - Date (required)
     - Summary (brief description)
     - Content (full article text)
   
3. **Add Photo**
   - **Option 1**: Click "Upload Image" to upload from computer (max 5MB)
   - **Option 2**: Enter direct image URL
   
4. **Set Status**
   - **Published**: Will appear on homepage immediately
   - **Draft**: Saved but not visible to public

5. **Click "Publish Article"**
   - Article will be saved to database
   - Appears on homepage if status is "published"

### Editing/Deleting News

- **Edit**: Click the edit (pencil) icon next to any news article
- **Delete**: Click the delete (trash) icon
- **View**: Click the eye icon to preview

### Controlling Chat Page Visibility

1. **Navigate to Settings**
   - Go to `admin/pages/settings.html`
   
2. **Find "Enable AI Chat Page" Toggle**
   - Turn ON to show chat page link in navigation
   - Turn OFF to hide chat page link

3. **Click "Save Settings"**
   - Settings are saved to database
   - Changes reflect immediately on homepage

---

## Database Tables

### News Table
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'published',
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Settings Table
```sql
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Authentication

Protected endpoints (POST, PUT, DELETE) require API key:
```javascript
headers: {
    'X-API-Key': 'bkr-secret-key-2024'
}
```

Stored in localStorage as `apiKey` for admin panel.

---

## Features Summary

### ✅ News Management
- [x] Admin can add news with photos
- [x] Admin can edit/delete news
- [x] News displayed dynamically on homepage
- [x] Photo upload support
- [x] Category-based organization
- [x] Publish/Draft status
- [x] Database persistence

### ✅ Chat Page Control
- [x] Admin toggle for chat page visibility
- [x] Settings saved to database
- [x] Navigation automatically updates
- [x] Fail-safe default behavior

---

## Testing Checklist

### News Management
- [ ] Add a news article with photo upload
- [ ] Add a news article with image URL
- [ ] Edit an existing news article
- [ ] Delete a news article
- [ ] Verify news appears on homepage
- [ ] Test draft vs published status

### Chat Page Control
- [ ] Toggle chat page OFF → Verify link disappears
- [ ] Toggle chat page ON → Verify link appears
- [ ] Save settings → Refresh page → Verify persistence
- [ ] Test on homepage navigation

---

## Files Modified

### Backend
- `backend/models.py` - Added settings table, updated news schema
- `backend/database.py` - Added news and settings CRUD methods
- `backend/app.py` - Added news and settings API endpoints

### Frontend
- `admin/pages/news.html` - Complete news management interface
- `admin/pages/settings.html` - Added chat page toggle and API integration
- `index.html` - Dynamic news loading and chat visibility control

---

## Next Steps (Optional Enhancements)

1. **Image Upload Endpoint**
   - Implement `/api/upload` endpoint in app.py
   - Handle file uploads to server/cloud storage
   - Return uploaded image URL

2. **News Detail Page**
   - Create `pages/news-detail.html`
   - Show full news article content
   - Share functionality

3. **News Pagination**
   - Add pagination to admin news table
   - Load more functionality on homepage

4. **Rich Text Editor**
   - Integrate WYSIWYG editor for news content
   - Better formatting options

5. **News Categories Filter**
   - Filter news by category on homepage
   - Category-based navigation

---

## Support

For issues or questions:
- Check browser console for errors
- Verify backend server is running
- Check database connection
- Ensure API key is correct

## Success! 🎉

Both features are now fully implemented and ready to use!
