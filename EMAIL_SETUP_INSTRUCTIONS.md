# 📧 Email Setup Instructions

## Quick Start Guide

### Step 1: Configure Gmail App Password

**IMPORTANT:** You MUST set up a Gmail App Password before emails will work!

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** (left sidebar)
3. Under "How you sign in to Google", enable **2-Step Verification**
4. Once 2-Step is enabled, go back to Security
5. Click on **App passwords** (under 2-Step Verification)
6. Select app: **Mail**
7. Select device: **Other** (name it "BKR Website")
8. Click **Generate**
9. Copy the 16-character password (example: `abcd efgh ijkl mnop`)

### Step 2: Update the .env File

Open `backend/.env` and update the SMTP password with your App Password:

```env
SMTP_PASSWORD=abcd efgh ijkl mnop
```

**Note:** Remove spaces from the app password or keep them - both work!

### Step 3: Test the Email Service

Run the test script to verify everything is working:

```bash
cd backend
python test_email.py
```

This will send 4 test emails (one for each form type).

### Step 4: Start the Server

```bash
cd backend
python app.py
```

The server will start at http://localhost:5000

### Step 5: Test the Forms

Open your browser and test each form:
- **File Complaint:** http://localhost:5000/pages/complaint.html
- **Share Feedback:** http://localhost:5000/pages/feedback.html  
- **Volunteer:** http://localhost:5000/#volunteer
- **Get in Touch:** http://localhost:5000/#contact

### Step 6: Check Your Email

Check these inboxes for test emails:
- **bkrfoundation.helpdesk@gmail.com** - for complaints
- **bkrfoundation@gmail.com** - for volunteer, contact, feedback

---

## Email Routing Summary

| Form | Recipient | Subject Prefix |
|------|-----------|---------------|
| File Complaint | bkrfoundation.helpdesk@gmail.com | "File Complaint - ..." |
| Volunteer Registration | bkrfoundation@gmail.com | "Volunteer Registration - ..." |
| Get in Touch (Contact) | bkrfoundation@gmail.com | "Casual Message - ..." |
| Share Your Feedback | bkrfoundation@gmail.com | "Share Your Feedback - ..." |

---

## Troubleshooting

### Emails Not Sending?

**Check 1: App Password**
- Make sure you're using an App Password, not your regular Gmail password
- The password should be 16 characters
- Remove any spaces if you copied them

**Check 2: Gmail Settings**
- 2-Step Verification must be enabled
- "Less secure app access" is NOT needed if using App Password

**Check 3: .env File**
- Make sure the file is named exactly `.env` (not `.env.txt`)
- Check there are no typos in the credentials
- Restart the server after changing .env

**Check 4: Internet Connection**
- Make sure you have internet access
- Try pinging smtp.gmail.com

**Check 5: Firewall**
- Port 587 must not be blocked
- Check your antivirus/firewall settings

### Error: "Authentication failed"
- Your App Password is incorrect
- Generate a new App Password and update .env

### Error: "Connection refused"
- Check your internet connection
- Make sure port 587 is not blocked

### Error: "Module not found"
- Make sure you're running from the backend directory
- Install dependencies: `pip install -r requirements.txt`

### Forms Submit but No Email?
- Check the browser console for errors
- Look at the server terminal for error messages
- Verify the API endpoints are responding (check Network tab in DevTools)

---

## For Production Deployment

When deploying to Easypanel, Railway, or other platforms:

### 1. Set Environment Variables
Don't use the .env file in production. Set these as environment variables:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=bkrfoundation@gmail.com
SMTP_PASSWORD=your-app-password-here
EMAIL_FROM=bkrfoundation@gmail.com
EMAIL_TO_HELPDESK=bkrfoundation.helpdesk@gmail.com
```

### 2. Consider Using a Dedicated Email Service
For production, consider using:
- **SendGrid** - 100 emails/day free
- **Mailgun** - 5,000 emails/month free
- **Amazon SES** - Very cheap, pay per email
- **Postmark** - Excellent deliverability

These services have better deliverability than Gmail and provide:
- Email tracking
- Bounce handling  
- Analytics
- Higher sending limits
- Better reliability

### 3. Add Rate Limiting
Prevent spam by limiting form submissions:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/email/complaint', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 complaints per hour per IP
def send_complaint():
    ...
```

### 4. Add CAPTCHA
Prevent bots from submitting forms:
- Google reCAPTCHA
- hCaptcha
- Cloudflare Turnstile

---

## Security Best Practices

✅ **DO:**
- Use App Passwords instead of regular passwords
- Keep .env file in .gitignore
- Use environment variables in production
- Add rate limiting to prevent spam
- Add CAPTCHA to forms
- Monitor email delivery
- Set up email notifications for errors

❌ **DON'T:**
- Commit .env file to Git
- Use "Less secure app access"
- Share your App Password
- Store passwords in code
- Allow unlimited form submissions
- Ignore failed email notifications

---

## Email Template Customization

To customize email templates, edit `backend/email_service.py`:

Each form type has its own method:
- `send_complaint_email()` - Complaint emails
- `send_volunteer_email()` - Volunteer registration
- `send_contact_email()` - Get in touch messages
- `send_feedback_email()` - Feedback submissions

You can customize:
- HTML styling (colors, fonts, layout)
- Email content (text, formatting)
- Subject lines
- Recipient addresses

---

## Testing Checklist

Before going live, test:

- [ ] All 4 forms submit successfully
- [ ] Emails arrive in correct inboxes
- [ ] Email formatting looks good
- [ ] All form fields appear in emails
- [ ] Success messages show correctly
- [ ] Error messages work when offline
- [ ] Loading states work
- [ ] Forms reset after submission
- [ ] CAPTCHA works (if added)
- [ ] Rate limiting works (if added)

---

## Need Help?

If you're still having issues:

1. Check the server logs for detailed error messages
2. Run `python test_email.py` to test SMTP directly
3. Review the EMAIL_IMPLEMENTATION_GUIDE.md
4. Check Gmail's sent folder to see if emails were sent
5. Make sure both email addresses exist and can receive mail

---

**Last Updated:** January 17, 2026
