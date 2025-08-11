from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from models.data_store import data_store
import uuid
import os
from utils.email_utils import send_comment_notification

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or not session.get('is_admin'):
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Get statistics
    stats = {
        'total_projects': len(data_store['projects']),
        'published_projects': len([p for p in data_store['projects'] if p['status'] == 'published']),
        'total_achievements': len(data_store['achievements']),
        'total_users': len([u for u in data_store['users'] if not u.get('is_admin', False)]),
        'total_comments': len(data_store['comments']),
        'total_likes': sum(p['likes'] for p in data_store['projects'])
    }
    
    # Get recent activities
    recent_projects = sorted(data_store['projects'], key=lambda x: x['created_at'], reverse=True)[:5]
    recent_comments = sorted(data_store['comments'], key=lambda x: x['created_at'], reverse=True)[:5]
    
    return render_template('admin/dashboard.html', stats=stats, 
                         recent_projects=recent_projects, recent_comments=recent_comments)

@admin_bp.route('/projects')
@admin_required
def projects():
    return render_template('admin/projects.html', projects=data_store['projects'])

@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@admin_required
def new_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags'].split(',') if request.form['tags'] else []
        status = request.form['status']
        link = request.form.get('link', '')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                image_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join('uploads', image_filename))
        
        # Create new project
        project_id = str(uuid.uuid4())
        new_project = {
            'id': project_id,
            'title': title,
            'description': description,
            'tags': [tag.strip() for tag in tags],
            'status': status,
            'link': link,
            'image': image_filename,
            'likes': 0,
            'created_at': '2025-08-11T00:00:00Z'  # In production, use datetime.now()
        }
        
        data_store['projects'].append(new_project)
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/projects.html', projects=data_store['projects'], editing=True)

@admin_bp.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    project = None
    for p in data_store['projects']:
        if p['id'] == project_id:
            project = p
            break
    
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin.projects'))
    
    if request.method == 'POST':
        project['title'] = request.form['title']
        project['description'] = request.form['description']
        project['tags'] = [tag.strip() for tag in request.form['tags'].split(',') if tag.strip()]
        project['status'] = request.form['status']
        project['link'] = request.form.get('link', '')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                image_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join('uploads', image_filename))
                project['image'] = image_filename
        
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/projects.html', projects=data_store['projects'], 
                         editing=True, edit_project=project)

@admin_bp.route('/projects/<project_id>/delete', methods=['POST'])
@admin_required
def delete_project(project_id):
    data_store['projects'] = [p for p in data_store['projects'] if p['id'] != project_id]
    # Also delete associated comments
    data_store['comments'] = [c for c in data_store['comments'] if c['project_id'] != project_id]
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

@admin_bp.route('/achievements')
@admin_required
def achievements():
    return render_template('admin/achievements.html', achievements=data_store['achievements'])

@admin_bp.route('/achievements/new', methods=['GET', 'POST'])
@admin_required
def new_achievement():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        
        # Create new achievement
        achievement_id = str(uuid.uuid4())
        new_achievement = {
            'id': achievement_id,
            'title': title,
            'description': description,
            'date': date
        }
        
        data_store['achievements'].append(new_achievement)
        flash('Achievement created successfully!', 'success')
        return redirect(url_for('admin.achievements'))
    
    return render_template('admin/achievements.html', achievements=data_store['achievements'], editing=True)

@admin_bp.route('/achievements/<achievement_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_achievement(achievement_id):
    achievement = None
    for a in data_store['achievements']:
        if a['id'] == achievement_id:
            achievement = a
            break
    
    if not achievement:
        flash('Achievement not found', 'error')
        return redirect(url_for('admin.achievements'))
    
    if request.method == 'POST':
        achievement['title'] = request.form['title']
        achievement['description'] = request.form['description']
        achievement['date'] = request.form['date']
        
        flash('Achievement updated successfully!', 'success')
        return redirect(url_for('admin.achievements'))
    
    return render_template('admin/achievements.html', achievements=data_store['achievements'], 
                         editing=True, edit_achievement=achievement)

@admin_bp.route('/achievements/<achievement_id>/delete', methods=['POST'])
@admin_required
def delete_achievement(achievement_id):
    data_store['achievements'] = [a for a in data_store['achievements'] if a['id'] != achievement_id]
    flash('Achievement deleted successfully!', 'success')
    return redirect(url_for('admin.achievements'))

@admin_bp.route('/profile')
@admin_required
def profile():
    # Get admin user
    admin_user = None
    for user in data_store['users']:
        if user['id'] == session['user_id']:
            admin_user = user
            break
    
    return render_template('admin/profile.html', user=admin_user, 
                         about_info=data_store['about_info'])

@admin_bp.route('/profile/update', methods=['POST'])
@admin_required
def update_profile():
    # Update admin user info
    for user in data_store['users']:
        if user['id'] == session['user_id']:
            user['name'] = request.form['name']
            user['email'] = request.form['email']
            session['user_name'] = user['name']
            break
    
    # Update about info
    data_store['about_info'] = {
        'title': request.form['about_title'],
        'description': request.form['about_description'],
        'skills': [skill.strip() for skill in request.form['skills'].split(',') if skill.strip()],
        'contact_email': request.form['contact_email']
    }
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('admin.profile'))
