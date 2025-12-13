# BKR Backend API

Flask-based REST API for the BKR Politician Website with SQLite database.

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update the API key:

```powershell
cp .env.example .env
```

Edit `.env` and change the API_KEY:
```
API_KEY=your-secret-api-key-change-this
```

### 3. Initialize Database

Create sample data:
```powershell
python migrate_data.py --sample
```

Or migrate from localStorage backup:
```powershell
python migrate_data.py path/to/backup.json
```

### 4. Start the Server

```powershell
python app.py
```

Server will start at: `http://localhost:5000`

## 📡 API Endpoints

### Public Endpoints (No API Key Required)

- `GET /api/health` - Health check
- `GET /api/health-camps` - Get all health camps
- `GET /api/health-camps?status=upcoming` - Filter by status
- `GET /api/health-camps/<id>` - Get single camp
- `POST /api/complaints` - Submit complaint
- `POST /api/feedback` - Submit feedback
- `GET /api/news` - Get published news
- `GET /api/news?status=published` - Filter news

### Protected Endpoints (Require API Key)

**Header Required:** `X-API-Key: your-api-key`

#### Health Camps
- `POST /api/health-camps` - Create new camp
- `PUT /api/health-camps/<id>` - Update camp
- `DELETE /api/health-camps/<id>` - Delete camp

#### Complaints
- `GET /api/complaints` - Get all complaints
- `PATCH /api/complaints/<id>/status` - Update status

#### Feedback
- `GET /api/feedback` - Get all feedback

#### News
- `POST /api/news` - Create news article
- `PUT /api/news/<id>` - Update article
- `DELETE /api/news/<id>` - Delete article

#### Dashboard
- `GET /api/dashboard/stats` - Get statistics

## 📝 Request Examples

### Create Health Camp
```bash
curl -X POST http://localhost:5000/api/health-camps \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "title": "Free Eye Check-up Camp",
    "date": "2025-12-20",
    "time": "9:00 AM - 5:00 PM",
    "location": "Community Hall, Quthbullapur",
    "services": "Eye Screening, Free Spectacles",
    "description": "Free eye check-up for all",
    "contact": "+91-9XXXXXX363",
    "status": "upcoming"
  }'
```

### Get Health Camps
```bash
curl http://localhost:5000/api/health-camps
```

### Submit Complaint (Public)
```bash
curl -X POST http://localhost:5000/api/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "9876543210",
    "email": "john@example.com",
    "area": "Quthbullapur",
    "category": "Infrastructure",
    "subject": "Road Repair Needed",
    "message": "The main road needs urgent repair",
    "date": "2025-12-12"
  }'
```

## 🗄️ Database Schema

### health_camps
- id, title, date, time, location, services, description, contact, status, created_at, updated_at

### complaints
- id, name, phone, email, area, category, subject, message, address, status, date, created_at, updated_at

### feedback
- id, name, phone, email, area, rating (1-5), category, message, suggestions, date, created_at

### news
- id, title, category, summary, content, status, date, created_at, updated_at

## 🔒 Security

- API key authentication for admin operations
- CORS configured for localhost:8080
- Environment variables for sensitive data
- Input validation on all endpoints

## 🧪 Testing

Test the API health:
```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "success": true,
  "message": "BKR API Server is running",
  "version": "1.0.0"
}
```

## 📦 Project Structure

```
backend/
├── app.py              # Flask application & routes
├── database.py         # Database operations
├── models.py           # Database schema
├── migrate_data.py     # Data migration tool
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🚨 Troubleshooting

**Port 5000 already in use:**
```powershell
# Windows: Find and kill the process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

**Module not found:**
```powershell
pip install -r requirements.txt
```

**Database errors:**
```powershell
# Delete and recreate database
rm bkr_database.db
python migrate_data.py --sample
```

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
