from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from models.models import db, User, Project, Achievement, Comment, AboutInfo
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
        'total_projects': Project.query.count(),
        'published_projects': Project.query.filter_by(status='published').count(),
        'total_achievements': Achievement.query.count(),
        'total_users': User.query.filter_by(is_admin=False).count(),
        'total_comments': Comment.query.count(),
        'total_likes': db.session.query(db.func.sum(Project.likes)).scalar() or 0
    }
    
    # Get recent activities
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, 
                         recent_projects=recent_projects, recent_comments=recent_comments)

@admin_bp.route('/projects')
@admin_required
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects)

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
        new_project = Project(
            title=title,
            description=description,
            tags=[tag.strip() for tag in tags],
            status=status,
            link=link,
            image=image_filename,
            likes=0
        )
        
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects, editing=True)

@admin_bp.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    project = Project.query.get(project_id)
    
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin.projects'))
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.tags = [tag.strip() for tag in request.form['tags'].split(',') if tag.strip()]
        project.status = request.form['status']
        project.link = request.form.get('link', '')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                image_filename = f"{uuid.uuid4()}_{filename}"
                file.save(os.path.join('uploads', image_filename))
                project.image = image_filename
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects, 
                         editing=True, edit_project=project)

@admin_bp.route('/projects/<project_id>/delete', methods=['POST'])
@admin_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        # Associated comments will be deleted automatically due to cascade
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    else:
        flash('Project not found', 'error')
    return redirect(url_for('admin.projects'))

@admin_bp.route('/achievements')
@admin_required
def achievements():
    all_achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('admin/achievements.html', achievements=all_achievements)

@admin_bp.route('/achievements/new', methods=['GET', 'POST'])
@admin_required
def new_achievement():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        
        # Create new achievement
        from datetime import datetime
        achievement_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_achievement = Achievement(
            title=title,
            description=description,
            date=achievement_date
        )
        
        db.session.add(new_achievement)
        db.session.commit()
        flash('Achievement created successfully!', 'success')
        return redirect(url_for('admin.achievements'))
    
    all_achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('admin/achievements.html', achievements=all_achievements, editing=True)

@admin_bp.route('/achievements/<achievement_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    
    if not achievement:
        flash('Achievement not found', 'error')
        return redirect(url_for('admin.achievements'))
    
    if request.method == 'POST':
        achievement.title = request.form['title']
        achievement.description = request.form['description']
        date_str = request.form['date']
        
        from datetime import datetime
        achievement.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Achievement updated successfully!', 'success')
        return redirect(url_for('admin.achievements'))
    
    all_achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('admin/achievements.html', achievements=all_achievements, 
                         editing=True, edit_achievement=achievement)

@admin_bp.route('/achievements/<achievement_id>/delete', methods=['POST'])
@admin_required
def delete_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    if achievement:
        db.session.delete(achievement)
        db.session.commit()
        flash('Achievement deleted successfully!', 'success')
    else:
        flash('Achievement not found', 'error')
    return redirect(url_for('admin.achievements'))

@admin_bp.route('/profile')
@admin_required
def profile():
    # Get admin user
    admin_user = User.query.get(session['user_id'])
    about_info = AboutInfo.query.first()
    
    return render_template('admin/profile.html', user=admin_user, 
                         about_info=about_info)

@admin_bp.route('/profile/update', methods=['POST'])
@admin_required
def update_profile():
    # Update admin user info
    admin_user = User.query.get(session['user_id'])
    if admin_user:
        admin_user.name = request.form['name']
        admin_user.email = request.form['email']
        session['user_name'] = admin_user.name
    
    # Update about info
    about_info = AboutInfo.query.first()
    if about_info:
        about_info.title = request.form['about_title']
        about_info.description = request.form['about_description']
        about_info.skills = [skill.strip() for skill in request.form['skills'].split(',') if skill.strip()]
        about_info.contact_email = request.form['contact_email']
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('admin.profile'))
