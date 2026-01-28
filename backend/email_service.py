"""
Email Service for sending emails via SMTP
Handles all email functionality for the BKR website
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from datetime import datetime


class EmailService:
    """Service class to handle email sending via SMTP"""
    
    def __init__(self):
        """Initialize email service with SMTP configuration from environment variables"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_to_helpdesk = os.getenv('EMAIL_TO_HELPDESK')
        
        if not all([self.smtp_username, self.smtp_password, self.email_from]):
            raise ValueError('Email configuration incomplete. Check environment variables.')
    
    def _create_html_email(self, subject, body_html):
        """Create a MIME email message with HTML content"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr(('BKR Foundation', self.email_from))
        
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        
        return msg
    
    def _send_email(self, to_email, msg):
        """Send email via SMTP"""
        try:
            msg['To'] = to_email
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.smtp_username, self.smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True, "Email sent successfully"
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check email credentials."
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_complaint_email(self, data):
        """
        Send complaint email to helpdesk
        
        Args:
            data (dict): Complaint form data containing name, phone, email, area, category, subject, message, address
        
        Returns:
            tuple: (success: bool, message: str)
        """
        subject = f"File Complaint - {data.get('subject', 'No Subject')}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #0a1628 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #ff6b35; }}
                .label {{ font-weight: bold; color: #1e3a5f; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 New Complaint Filed</h1>
                    <p>From BKR Foundation Website</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">📋 Subject:</div>
                        <div class="value">{data.get('subject', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">👤 Name:</div>
                        <div class="value">{data.get('name', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📞 Phone:</div>
                        <div class="value">{data.get('phone', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value">{data.get('email', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📍 Area:</div>
                        <div class="value">{data.get('area', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">🏷️ Category:</div>
                        <div class="value">{data.get('category', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">💬 Complaint Details:</div>
                        <div class="value">{data.get('message', 'N/A')}</div>
                    </div>
                    {f'''<div class="field">
                        <div class="label">🏠 Address:</div>
                        <div class="value">{data.get('address', 'N/A')}</div>
                    </div>''' if data.get('address') else ''}
                    <div class="field">
                        <div class="label">🕒 Submitted:</div>
                        <div class="value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated message from BKR Foundation Website</p>
                    <p>Please respond within 48 hours</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        return self._send_email(self.email_to_helpdesk, msg)
    
    def send_volunteer_email(self, data):
        """
        Send volunteer registration email
        
        Args:
            data (dict): Volunteer form data containing name, phone, email, area, message
        
        Returns:
            tuple: (success: bool, message: str)
        """
        subject = f"Volunteer Registration - {data.get('name', 'New Volunteer')}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ff6b35 0%, #ff9933 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #1e3a5f; }}
                .label {{ font-weight: bold; color: #ff6b35; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤝 New Volunteer Registration</h1>
                    <p>Someone wants to join the movement!</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">👤 Name:</div>
                        <div class="value">{data.get('name', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📞 Phone:</div>
                        <div class="value">{data.get('phone', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value">{data.get('email', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📍 Area:</div>
                        <div class="value">{data.get('area', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">💬 Why they want to volunteer:</div>
                        <div class="value">{data.get('message', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">🕒 Registered:</div>
                        <div class="value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated message from BKR Foundation Website</p>
                    <p>Welcome them to the movement!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        return self._send_email(self.email_from, msg)
    
    def send_contact_email(self, data):
        """
        Send contact/get-in-touch email (casual message)
        
        Args:
            data (dict): Contact form data containing name, email, subject, message
        
        Returns:
            tuple: (success: bool, message: str)
        """
        subject = f"Casual Message - {data.get('subject', 'Get in Touch')}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #0a1628 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #ff6b35; }}
                .label {{ font-weight: bold; color: #1e3a5f; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💌 New Message</h1>
                    <p>Someone wants to get in touch</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">📋 Subject:</div>
                        <div class="value">{data.get('subject', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">👤 Name:</div>
                        <div class="value">{data.get('name', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value">{data.get('email', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">💬 Message:</div>
                        <div class="value">{data.get('message', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">🕒 Sent:</div>
                        <div class="value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated message from BKR Foundation Website</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        return self._send_email(self.email_from, msg)
    
    def send_feedback_email(self, data):
        """
        Send feedback email
        
        Args:
            data (dict): Feedback form data containing rating, category, name, phone, email, area, feedback
        
        Returns:
            tuple: (success: bool, message: str)
        """
        subject = f"Share Your Feedback - {data.get('category', 'General Feedback')}"
        
        # Create star rating display
        rating = int(data.get('rating', 0))
        stars = '⭐' * rating + '☆' * (5 - rating)
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ff6b35 0%, #ff9933 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #1e3a5f; }}
                .label {{ font-weight: bold; color: #ff6b35; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .rating {{ font-size: 24px; text-align: center; padding: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⭐ New Feedback Received</h1>
                    <p>Someone shared their experience</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">⭐ Rating:</div>
                        <div class="rating">{stars} ({rating}/5)</div>
                    </div>
                    <div class="field">
                        <div class="label">🏷️ Category:</div>
                        <div class="value">{data.get('category', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">👤 Name:</div>
                        <div class="value">{data.get('name', 'Anonymous')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📞 Phone:</div>
                        <div class="value">{data.get('phone', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value">{data.get('email', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📍 Area:</div>
                        <div class="value">{data.get('area', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">💬 Feedback:</div>
                        <div class="value">{data.get('feedback', 'N/A')}</div>
                    </div>
                    {f'''<div class="field">
                        <div class="label">💡 Suggestions:</div>
                        <div class="value">{data.get('suggestions', 'None')}</div>
                    </div>''' if data.get('suggestions') else ''}
                    <div class="field">
                        <div class="label">🕒 Submitted:</div>
                        <div class="value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated message from BKR Foundation Website</p>
                    <p>Thank them for their feedback!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        return self._send_email(self.email_from, msg)
    
    def send_skills_registration_confirmation(self, to_email, name, registration_data):
        """
        Send skills for youth registration confirmation email to applicant
        
        Args:
            to_email (str): Applicant's email address
            name (str): Applicant's name
            registration_data (dict): Full registration data
        
        Returns:
            tuple: (success: bool, message: str)
        """
        subject = "Skills for Youth Program - Registration Confirmed"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .welcome {{ background: white; padding: 20px; border-radius: 6px; margin-bottom: 20px; text-align: center; }}
                .details {{ background: white; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
                .field {{ margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #e9ecef; }}
                .label {{ font-weight: bold; color: #667eea; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .info-box {{ background: #e7f3ff; padding: 20px; border-radius: 6px; border-left: 4px solid #667eea; margin: 20px 0; }}
                .highlight {{ color: #667eea; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Welcome to Skills for Youth!</h1>
                    <p>B Kishore Reddy Foundation</p>
                </div>
                <div class="content">
                    <div class="welcome">
                        <h2 style="color: #1e3a5f; margin-bottom: 15px;">Thank You for Registering, {name}!</h2>
                        <p style="color: #6c757d; font-size: 16px;">Your registration has been successfully received.</p>
                    </div>
                    
                    <div class="details">
                        <h3 style="color: #1e3a5f; margin-bottom: 20px;">📋 Registration Details</h3>
                        <div class="field">
                            <div class="label">Name:</div>
                            <div class="value">{registration_data.get('name')}</div>
                        </div>
                        <div class="field">
                            <div class="label">Email:</div>
                            <div class="value">{registration_data.get('email')}</div>
                        </div>
                        <div class="field">
                            <div class="label">Phone:</div>
                            <div class="value">{registration_data.get('phone')}</div>
                        </div>
                        <div class="field">
                            <div class="label">Location:</div>
                            <div class="value">{registration_data.get('location')}, {registration_data.get('city')}</div>
                        </div>
                        <div class="field" style="border-bottom: none;">
                            <div class="label">Education:</div>
                            <div class="value">{registration_data.get('education')}</div>
                        </div>
                    </div>
                    
                    <div class="info-box">
                        <h4 style="color: #1e3a5f; margin-top: 0;">📚 What's Next?</h4>
                        <p>✓ Your registration is being reviewed by our team</p>
                        <p>✓ Program dates will be announced soon</p>
                        <p>✓ You will receive course schedule via email</p>
                        <p>✓ Our faculty has <span class="highlight">10+ years of experience</span></p>
                    </div>
                    
                    <div class="info-box" style="background: #fff3cd; border-left-color: #ffc107;">
                        <h4 style="color: #856404; margin-top: 0;">💡 Program Highlights</h4>
                        <p>• Expert training in Aptitude & Reasoning</p>
                        <p>• Comprehensive study materials provided</p>
                        <p>• Mock tests and performance analysis</p>
                        <p>• Career guidance and counseling</p>
                        <p>• Job placement assistance</p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="color: #6c757d;">Questions? Contact us:</p>
                        <p style="color: #1e3a5f; font-weight: bold;">📧 {self.email_from}</p>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>B Kishore Reddy Foundation</strong></p>
                    <p>Empowering Youth • Building Futures</p>
                    <p style="margin-top: 15px;">This is an automated confirmation email</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        success, message = self._send_email(to_email, msg)
        
        # Also send notification to admin
        if success:
            self._send_skills_registration_notification(registration_data)
        
        return success, message
    
    def _send_skills_registration_notification(self, data):
        """Send internal notification about new skills registration"""
        subject = f"New Skills Registration - {data.get('name')}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #667eea; }}
                .label {{ font-weight: bold; color: #667eea; margin-bottom: 5px; }}
                .value {{ color: #495057; }}
                .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 New Skills for Youth Registration</h1>
                    <p>From BKR Foundation Website</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">👤 Name:</div>
                        <div class="value">{data.get('name')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📞 Phone:</div>
                        <div class="value">{data.get('phone')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value">{data.get('email')}</div>
                    </div>
                    <div class="field">
                        <div class="label">📅 Date of Birth:</div>
                        <div class="value">{data.get('dob')}</div>
                    </div>
                    <div class="field">
                        <div class="label">🎓 Education:</div>
                        <div class="value">{data.get('education')}</div>
                    </div>
                    {f'''<div class="field">
                        <div class="label">🏫 Institution:</div>
                        <div class="value">{data.get('institution')}</div>
                    </div>''' if data.get('institution') else ''}
                    <div class="field">
                        <div class="label">📍 Location:</div>
                        <div class="value">{data.get('location')}, {data.get('city')}</div>
                    </div>
                    {f'''<div class="field">
                        <div class="label">💭 Motivation:</div>
                        <div class="value">{data.get('motivation')}</div>
                    </div>''' if data.get('motivation') else ''}
                    <div class="field">
                        <div class="label">🕒 Submitted:</div>
                        <div class="value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated message from BKR Foundation Website</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = self._create_html_email(subject, body_html)
        return self._send_email(self.email_to_helpdesk, msg)
