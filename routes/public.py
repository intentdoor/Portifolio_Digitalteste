from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from models.models import db, User, Project, Achievement, Comment, AboutInfo
from utils.email_utils import send_comment_notification, send_contact_notification
import uuid

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    # Get published projects, sorted by likes and recent first
    published_projects = Project.query.filter_by(status='published').order_by(Project.likes.desc(), Project.created_at.desc()).limit(6).all()
    
    return render_template('index.html', projects=published_projects)

@public_bp.route('/projects')
def projects():
    published_projects = Project.query.filter_by(status='published').order_by(Project.likes.desc(), Project.created_at.desc()).all()
    return render_template('index.html', projects=published_projects, show_all=True)

@public_bp.route('/project/<project_id>')
def project_detail(project_id):
    project = Project.query.filter_by(id=project_id, status='published').first()
    
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('public.index'))
    
    # Get comments for this project
    comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at.desc()).all()
    
    return render_template('project_detail.html', project=project, comments=comments)

@public_bp.route('/project/<project_id>/like', methods=['POST'])
def like_project(project_id):
    if not session.get('user_id'):
        return jsonify({'error': 'Login required'}), 401
    
    project = Project.query.get(project_id)
    
    if project:
        project.likes = project.likes + 1
        db.session.commit()
        return jsonify({'likes': project.likes})
    
    return jsonify({'error': 'Project not found'}), 404

@public_bp.route('/project/<project_id>/comment', methods=['POST'])
def add_comment(project_id):
    if not session.get('user_id'):
        flash('Please login to comment', 'error')
        return redirect(url_for('auth.login'))
    
    comment_text = request.form.get('comment')
    if not comment_text:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('public.project_detail', project_id=project_id))
    
    # Get user name
    user_name = session.get('user_name', 'Anonymous')
    
    # Create new comment
    new_comment = Comment(
        content=comment_text,
        project_id=project_id,
        user_id=session['user_id']
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    # Send notification to admin
    try:
        send_comment_notification(project_id, user_name, comment_text)
    except Exception as e:
        print(f"Failed to send notification: {e}")
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('public.project_detail', project_id=project_id))

@public_bp.route('/about')
def about():
    about_info = AboutInfo.query.first()
    achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('about.html', about=about_info, achievements=achievements)

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Send email notification
        try:
            send_contact_notification(name, email, message)
            flash('Mensagem enviada com sucesso! Obrigado pelo contato.', 'success')
        except Exception as e:
            flash('Erro ao enviar mensagem. Tente novamente mais tarde.', 'error')
        
        return redirect(url_for('public.contact'))
    
    about_info = AboutInfo.query.first()
    return render_template('about.html', about=about_info, show_contact=True)

@public_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
