# BKR Politician Website

A modern, professional website for **B Kishore Reddy** - Congress MLA Candidate for Quthbullapur Constituency.

![Congress Hand](images/congresshand.png)

## 🌐 Live Website

- **Main Website**: [http://localhost:8080](http://localhost:8080) (when running locally)
- **GitHub Repository**: [https://github.com/ranjith8889999/bkr-politician-websites](https://github.com/ranjith8889999/bkr-politician-websites)

## 📋 Table of Contents

- [Features](#features)
- [Website Structure](#website-structure)
- [Admin Panel](#admin-panel)
- [Getting Started](#getting-started)
- [URLs & Pages](#urls--pages)
- [Admin Login Credentials](#admin-login-credentials)
- [Technology Stack](#technology-stack)
- [Deployment](#deployment)

## ✨ Features

### Main Website
- 🏠 **Hero Section** - Dynamic animations with Congress branding
- 👤 **About Section** - Biography, mission, and vision
- 🛤️ **Political Journey** - Timeline of political career
- 💡 **Key Initiatives** - Major projects and achievements
- 🎯 **Agendas** - Policy promises and goals
- 🖼️ **Gallery** - Photo gallery with lightbox
- 🏥 **Health Camps** - Upcoming and past health camps
- 💬 **Testimonials** - Citizen feedback and reviews
- 📰 **News & Updates** - Latest announcements
- 📝 **Complaint Form** - Submit complaints with email notification
- ⭐ **Feedback Form** - Rate and provide feedback
- 🤝 **Volunteer Registration** - Join the movement
- 📞 **Contact Section** - Multiple contact methods

### Admin Panel
- 📊 **Dashboard** - Overview with statistics
- 🏥 **Health Camps Management** - Add/edit/delete health camps
- 🖼️ **Gallery Management** - Upload and manage images
- 📰 **News Management** - Publish articles and announcements
- 📝 **Complaints Viewer** - View, filter, and manage complaints
- ⭐ **Feedback Viewer** - View and analyze citizen feedback
- ✏️ **Content Editor** - Edit all website sections
- ⚙️ **Settings** - Account, backup/restore, and data management

## 📁 Website Structure

```
bkr4/
├── index.html                      # Main landing page
├── css/
│   ├── style.css                   # Main styles (2300+ lines)
│   ├── animations.css              # Animation library (800+ lines)
│   └── admin.css                   # Admin panel styles
├── js/
│   ├── main.js                     # Website functionality
│   └── admin.js                    # Admin panel functionality
├── images/
│   ├── congresshand.png            # Congress party symbol
│   └── IMG-*.jpg                   # Photo gallery (8 images)
├── pages/
│   ├── complaint.html              # Complaint submission form
│   ├── feedback.html               # Feedback with star rating
│   └── health-camps.html           # Health camps listing
├── admin/pages/
│   ├── login.html                  # Admin login
│   ├── dashboard.html              # Admin dashboard
│   ├── health-camps.html           # Manage health camps
│   ├── gallery.html                # Manage gallery
│   ├── news.html                   # Manage news
│   ├── complaints.html             # View complaints
│   ├── feedback.html               # View feedback
│   ├── content.html                # Edit website content
│   └── settings.html               # Admin settings
└── README.md                       # This file
```

## 🔐 Admin Panel

### Access URLs

**Local Development:**
- Admin Login: `http://localhost:8080/admin/pages/login.html`
- Dashboard: `http://localhost:8080/admin/pages/dashboard.html`
- Health Camps: `http://localhost:8080/admin/pages/health-camps.html`
- Gallery: `http://localhost:8080/admin/pages/gallery.html`
- News: `http://localhost:8080/admin/pages/news.html`
- Complaints: `http://localhost:8080/admin/pages/complaints.html`
- Feedback: `http://localhost:8080/admin/pages/feedback.html`
- Content: `http://localhost:8080/admin/pages/content.html`
- Settings: `http://localhost:8080/admin/pages/settings.html`

**GitHub Pages (after deployment):**
Replace `localhost:8080` with `https://ranjith8889999.github.io/bkr-politician-websites`

### Admin Login Credentials

```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT**: Change these credentials in production by:
1. Going to Admin Panel → Settings → Account Settings
2. Enter current password: `admin123`
3. Set your new password
4. Update and save

## 🚀 Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.x (for local server) OR any HTTP server
- Text editor (VS Code, Sublime Text, etc.)

### Running Locally

**Option 1: Using Python**
```bash
cd c:\Users\Ranjit\Desktop\bkr\bkr4
python -m http.server 8080
```

**Option 2: Using Node.js (http-server)**
```bash
npm install -g http-server
cd c:\Users\Ranjit\Desktop\bkr\bkr4
http-server -p 8080
```

**Option 3: Using VS Code Live Server**
1. Install "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

Then open: `http://localhost:8080`

## 🔗 URLs & Pages

### Public Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/index.html` or `/` | Main landing page |
| Complaint Form | `/pages/complaint.html` | Submit complaints |
| Feedback Form | `/pages/feedback.html` | Submit feedback with rating |
| Health Camps | `/pages/health-camps.html` | View health camp schedule |

### Admin Pages (Protected)

| Page | URL | Description |
|------|-----|-------------|
| Admin Login | `/admin/pages/login.html` | Login to admin panel |
| Dashboard | `/admin/pages/dashboard.html` | Admin overview & stats |
| Health Camps Mgmt | `/admin/pages/health-camps.html` | Manage health camps |
| Gallery Mgmt | `/admin/pages/gallery.html` | Upload & manage images |
| News Mgmt | `/admin/pages/news.html` | Create & publish news |
| Complaints | `/admin/pages/complaints.html` | View all complaints |
| Feedback | `/admin/pages/feedback.html` | View all feedback |
| Content Editor | `/admin/pages/content.html` | Edit website content |
| Settings | `/admin/pages/settings.html` | Admin settings & backup |

## 🛠️ Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome 6.5.1** - Icon library
- **Google Fonts (Poppins)** - Typography
- **FormSubmit.co** - Form submissions to email
- **localStorage** - Client-side data persistence

### Key Features:
- ✅ Fully responsive design
- ✅ No frameworks required (vanilla JS)
- ✅ Fast loading times
- ✅ SEO optimized
- ✅ Progressive animations
- ✅ Cross-browser compatible

## 📧 Form Submissions

All forms send emails to: **ranjith888999@gmail.com**

### Forms Available:
1. **Complaint Form** - Categories: Roads, Water, Electricity, Sanitation, etc.
2. **Feedback Form** - Star rating system (1-5 stars)
3. **Volunteer Form** - Join the movement
4. **Contact Form** - General inquiries

## 📊 Admin Panel Features

### Dashboard
- Total complaints, feedback, health camps stats
- Recent complaints and feedback tables
- Quick action buttons

### Health Camps Management
- Add new health camps with date, location, services
- View upcoming and past camps
- Edit or delete camps
- Filter and search functionality

### Gallery Management
- Drag & drop image upload
- Categorize images (Events, Health Camps, Meetings, Community)
- Add captions and descriptions
- Delete images
- Filter by category

### News Management
- Create news articles with title, summary, content
- Categorize (Announcement, Event, Press Release, Update)
- Publish or save as draft
- Featured image support
- Edit or delete articles

### Complaints Management
- View all complaints with status (Pending, In Progress, Resolved)
- Filter by category, status, area
- Update complaint status
- Export to CSV
- Search functionality
- View detailed complaint information

### Feedback Management
- View all feedback with star ratings
- Average rating calculation
- Filter by rating, category
- Positive vs negative feedback stats
- Export to CSV
- Delete feedback

### Content Editor
- Edit Hero section (tagline, heading, description)
- Edit About section (bio, stats)
- Manage Political Journey timeline
- Manage Key Initiatives
- Manage Policy Agendas
- Update Contact information
- Update Social media links

### Settings
- Change admin password
- Toggle website features (health camps, news, volunteer form)
- Create data backups (download as JSON)
- Restore from backup
- Clear specific data (complaints, feedback, gallery)
- Reset all data

## 🌐 Deployment

### GitHub Pages

1. **Enable GitHub Pages:**
   - Go to repository settings: https://github.com/ranjith8889999/bkr-politician-websites/settings/pages
   - Under "Source", select "Deploy from a branch"
   - Select branch: `main`
   - Select folder: `/ (root)`
   - Click "Save"

2. **Access your site at:**
   ```
   https://ranjith8889999.github.io/bkr-politician-websites/
   ```

3. **Admin panel will be at:**
   ```
   https://ranjith8889999.github.io/bkr-politician-websites/admin/pages/login.html
   ```

### Custom Domain (Optional)

1. Purchase a domain (e.g., kishorereddy.com)
2. In GitHub repo settings → Pages → Custom domain
3. Add CNAME record in your domain provider:
   ```
   Type: CNAME
   Name: www
   Value: ranjith8889999.github.io
   ```

## 🔒 Security Notes

1. **Change default admin password immediately**
2. **Never commit sensitive credentials to GitHub**
3. **Use environment variables for production**
4. **Enable 2FA on GitHub account**
5. **Regularly backup admin data**

## 📱 Social Media Links

Update these in the code or via Admin Panel → Content → Contact:

- **Instagram**: https://instagram.com/kishorereddy8925
- **YouTube**: https://youtube.com/@BONGUNURIKISHOREREDDYOFFICIAL
- **Facebook**: (to be updated)
- **Twitter**: (to be updated)

## 🎨 Color Palette

```css
Primary Blue: #1e3a5f
Congress Orange: #ff6b35
Saffron: #ff9933
White: #ffffff
Dark Text: #0a1628
Light Background: #f5f7fa
```

## 📝 Content Updates

### To Update Website Content:

1. **Via Admin Panel (Recommended):**
   - Login at `/admin/pages/login.html`
   - Go to "Content" section
   - Edit any section (Hero, About, Journey, etc.)
   - Click "Save Changes"

2. **Via Code:**
   - Edit `index.html` for structure
   - Edit `css/style.css` for styling
   - Edit `js/main.js` for functionality

### To Add New Health Camps:

1. Login to admin panel
2. Go to "Health Camps"
3. Click "Add New Camp"
4. Fill in details (title, date, location, services)
5. Click "Add Camp"

### To Add News:

1. Login to admin panel
2. Go to "News & Updates"
3. Click "Add News Article"
4. Fill in title, category, summary, content
5. Choose "Published" or "Draft"
6. Click "Publish Article"

## 🐛 Troubleshooting

### Images not showing?
- Check if images exist in `/images/` folder
- Verify image paths in HTML
- Clear browser cache

### Admin panel not loading?
- Check if localStorage is enabled in browser
- Try incognito/private mode
- Clear browser cache and cookies

### Forms not submitting?
- Check internet connection
- Verify email in FormSubmit configuration
- Check browser console for errors

### Data not persisting?
- localStorage must be enabled
- Don't use incognito mode for admin panel
- Create regular backups from Settings page

## 📞 Support & Contact

- **Email**: ranjith888999@gmail.com
- **Phone**: +91-9XXXXXX363
- **Office**: Quthbullapur, Medchal-Malkajgiri District, Telangana

## 📄 License

Copyright © 2025 B Kishore Reddy. All rights reserved.

## 🙏 Credits

- **Design & Development**: Custom built for BKR
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)
- **Form Handling**: FormSubmit.co

---

**Last Updated**: December 10, 2025

**Version**: 1.0.0

**Developed for**: BONGUNURI KISHORE REDDY - Congress MLA Candidate, Quthbullapur Constituency
