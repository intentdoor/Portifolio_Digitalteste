import smtplib
import os
from email.mime.text import MIMEText
from models.data_store import get_project_by_id

def send_comment_notification(project_id, commenter_name, comment_text):
    """Send email notification to admin when new comment is posted"""
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured - comment notification not sent")
        return
    
    # Get project info
    project = get_project_by_id(project_id)
    if not project:
        return
    
    # Get admin email
    from models.models import User
    admin_user = User.query.filter_by(is_admin=True).first()
    admin_email = admin_user.email if admin_user else None
    
    if not admin_email:
        return
    
    subject = f"New Comment on '{project.title}''"
    body = f"""
    Hi Admin,
    
    A new comment has been posted on your project "{project.title}".
    
    Commenter: {commenter_name}
    Comment: {comment_text}
    
    You can view the project and all comments in your admin dashboard.
    
    Best regards,
    Portfolio System
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = admin_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"Comment notification sent to {admin_email}")
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        raise e

def send_contact_notification(name, email, message):
    """Send email notification for contact form submissions"""
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured - contact notification not sent")
        return
    
    # Get admin email
    from models.models import User
    admin_user = User.query.filter_by(is_admin=True).first()
    admin_email = admin_user.email if admin_user else None
    
    if not admin_email:
        return
    
    subject = f"New Contact Form Submission from {name}"
    body = f"""
    Hi Admin,
    
    You have received a new contact form submission:
    
    Name: {name}
    Email: {email}
    Message: {message}
    
    Please respond to them directly at their email address.
    
    Best regards,
    Portfolio System
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = admin_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"Contact notification sent to {admin_email}")
    except Exception as e:
        print(f"Failed to send contact notification: {e}")
        raise e
