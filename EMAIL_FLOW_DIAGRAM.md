# Email Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BKR FOUNDATION EMAIL SYSTEM                           │
└─────────────────────────────────────────────────────────────────────────┘

USER FORMS                    API ENDPOINTS              EMAIL RECIPIENTS
═══════════                   ═════════════              ════════════════

┌──────────────┐              ┌──────────────┐          ┌─────────────────┐
│ File         │              │   POST       │          │ bkrfoundation.  │
│ Complaint    │─────────────>│ /api/email/  │─────────>│ helpdesk@       │
│ Form         │              │ complaint    │          │ gmail.com       │
└──────────────┘              └──────────────┘          └─────────────────┘
complaints.html               Subject: "File Complaint - [subject]"
Required: name, phone,        
area, category, subject,      
message                       

┌──────────────┐              ┌──────────────┐          ┌─────────────────┐
│ Volunteer    │              │   POST       │          │ bkrfoundation@  │
│ Registration │─────────────>│ /api/email/  │─────────>│ gmail.com       │
│ Form         │              │ volunteer    │          │                 │
└──────────────┘              └──────────────┘          └─────────────────┘
index.html#volunteer          Subject: "Volunteer Registration - [name]"
Required: name, phone,
email, area

┌──────────────┐              ┌──────────────┐          ┌─────────────────┐
│ Get in Touch │              │   POST       │          │ bkrfoundation@  │
│ (Contact)    │─────────────>│ /api/email/  │─────────>│ gmail.com       │
│ Form         │              │ contact      │          │                 │
└──────────────┘              └──────────────┘          └─────────────────┘
index.html#contact            Subject: "Casual Message - [subject]"
Required: name, email,
subject, message

┌──────────────┐              ┌──────────────┐          ┌─────────────────┐
│ Share Your   │              │   POST       │          │ bkrfoundation@  │
│ Feedback     │─────────────>│ /api/email/  │─────────>│ gmail.com       │
│ Form         │              │ feedback     │          │                 │
└──────────────┘              └──────────────┘          └─────────────────┘
feedback.html                 Subject: "Share Your Feedback - [category]"
Required: rating,
category


═══════════════════════════════════════════════════════════════════════════

                         BACKEND EMAIL SERVICE
                         ════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                        email_service.py                                  │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ EmailService Class                                                  │ │
│  │                                                                      │ │
│  │ Configuration from .env:                                            │ │
│  │ • SMTP_SERVER = smtp.gmail.com                                      │ │
│  │ • SMTP_PORT = 587 (TLS)                                             │ │
│  │ • SMTP_USERNAME = bkrfoundation@gmail.com                           │ │
│  │ • SMTP_PASSWORD = [App Password]                                    │ │
│  │ • EMAIL_FROM = bkrfoundation@gmail.com                              │ │
│  │ • EMAIL_TO_HELPDESK = bkrfoundation.helpdesk@gmail.com              │ │
│  │                                                                      │ │
│  │ Methods:                                                             │ │
│  │ ├─ send_complaint_email(data)  → Beautiful HTML email               │ │
│  │ ├─ send_volunteer_email(data)  → Beautiful HTML email               │ │
│  │ ├─ send_contact_email(data)    → Beautiful HTML email               │ │
│  │ └─ send_feedback_email(data)   → Beautiful HTML email               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘

                                  ▼
                                  
                         ┌─────────────────┐
                         │   SMTP Server   │
                         │ smtp.gmail.com  │
                         │     Port 587    │
                         │   (TLS/STARTTLS)│
                         └─────────────────┘
                                  ▼
                                  
                         ┌─────────────────┐
                         │  Gmail delivers │
                         │  email to       │
                         │  recipient      │
                         └─────────────────┘


═══════════════════════════════════════════════════════════════════════════

                            EMAIL FEATURES
                            ══════════════

✨ Beautiful HTML Templates
   • Responsive design
   • BKR Foundation branding
   • Gradient headers
   • Professional layout
   • Clear field organization

📧 Smart Routing
   • Complaints go to helpdesk
   • Other forms go to main email
   • Customizable recipients

🔒 Secure
   • TLS encryption
   • App Password authentication
   • Environment variables
   • No hardcoded credentials

⚡ Features
   • Loading states
   • Success/Error messages
   • Form validation
   • Local storage backup
   • Async/await

🎯 User Experience
   • Instant feedback
   • Clear error messages
   • Professional emails
   • Fast delivery


═══════════════════════════════════════════════════════════════════════════

                         SAMPLE EMAIL OUTPUT
                         ═══════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│ From: BKR Foundation <bkrfoundation@gmail.com>                           │
│ To: bkrfoundation.helpdesk@gmail.com                                     │
│ Subject: File Complaint - Road Repair Needed                             │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────────────┐   │
│ │          🚨 New Complaint Filed                                    │   │
│ │        From BKR Foundation Website                                │   │
│ │                                                                    │   │
│ ├───────────────────────────────────────────────────────────────────┤   │
│ │                                                                    │   │
│ │ 📋 Subject: Road Repair Needed                                    │   │
│ │ 👤 Name: Ranjit Kumar                                             │   │
│ │ 📞 Phone: +91 9876543210                                          │   │
│ │ 📧 Email: ranjit@example.com                                      │   │
│ │ 📍 Area: Quthbullapur                                             │   │
│ │ 🏷️ Category: Infrastructure                                       │   │
│ │ 💬 Details: The road near my house has potholes...               │   │
│ │ 🕒 Submitted: January 17, 2026 at 10:30 AM                       │   │
│ │                                                                    │   │
│ ├───────────────────────────────────────────────────────────────────┤   │
│ │     This is an automated message from BKR Foundation Website      │   │
│ │              Please respond within 48 hours                       │   │
│ └───────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

                            TESTING FLOW
                            ════════════

1. User fills form on website
        ↓
2. JavaScript validates data
        ↓
3. Async POST request to API endpoint
        ↓
4. Backend validates required fields
        ↓
5. EmailService creates HTML email
        ↓
6. Connect to Gmail SMTP server
        ↓
7. Authenticate with App Password
        ↓
8. Send email via TLS
        ↓
9. Return success/error to frontend
        ↓
10. Show notification to user
        ↓
11. Reset form on success


═══════════════════════════════════════════════════════════════════════════
```
