from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.data_store import data_store
import uuid
import smtplib
from email.mime.text import MIMEText
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Find user by email
        user = None
        for u in data_store['users']:
            if u['email'] == email:
                user = u
                break
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['is_admin'] = user.get('is_admin', False)
            flash('Login realizado com sucesso!', 'success')
            
            # Redirect admin users to admin dashboard
            if session.get('is_admin'):
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('public.index'))
        else:
            flash('Email ou senha inválidos', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return render_template('auth/register.html')
        
        # Check if email already exists
        for user in data_store['users']:
            if user['email'] == email:
                flash('Email já está cadastrado', 'error')
                return render_template('auth/register.html')
        
        # Create new user
        user_id = str(uuid.uuid4())
        new_user = {
            'id': user_id,
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'is_admin': False,
            'profile_image': None
        }
        
        data_store['users'].append(new_user)
        flash('Cadastro realizado com sucesso! Por favor, faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('public.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Find user by email
        user = None
        for u in data_store['users']:
            if u['email'] == email:
                user = u
                break
        
        if user:
            # Generate reset token (in production, this should be more secure)
            reset_token = str(uuid.uuid4())
            user['reset_token'] = reset_token
            
            # Send email (simplified for demo)
            try:
                send_password_reset_email(user['email'], user['name'], reset_token)
                flash('Password reset instructions have been sent to your email', 'success')
            except Exception as e:
                flash('Error sending email. Please try again later.', 'error')
                print(f"Email error: {e}")
        else:
            flash('If that email exists in our system, you will receive reset instructions', 'info')
    
    return render_template('auth/forgot_password.html')

def send_password_reset_email(email, name, reset_token):
    """Send password reset email"""
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured")
        return
    
    subject = "Password Reset Request"
    body = f"""
    Hi {name},
    
    You requested a password reset for your portfolio account.
    
    Reset Token: {reset_token}
    
    If you didn't request this reset, please ignore this email.
    
    Best regards,
    Portfolio Team
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = email
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
