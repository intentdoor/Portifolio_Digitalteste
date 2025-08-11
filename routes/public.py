from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from models.data_store import data_store
from utils.email_utils import send_comment_notification
import uuid

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    # Get published projects, sorted by likes and recent first
    published_projects = [p for p in data_store['projects'] if p['status'] == 'published']
    published_projects = sorted(published_projects, key=lambda x: (x['likes'], x['created_at']), reverse=True)
    
    return render_template('index.html', projects=published_projects[:6])

@public_bp.route('/projects')
def projects():
    published_projects = [p for p in data_store['projects'] if p['status'] == 'published']
    return render_template('index.html', projects=published_projects, show_all=True)

@public_bp.route('/project/<project_id>')
def project_detail(project_id):
    project = None
    for p in data_store['projects']:
        if p['id'] == project_id and p['status'] == 'published':
            project = p
            break
    
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('public.index'))
    
    # Get comments for this project
    comments = [c for c in data_store['comments'] if c['project_id'] == project_id]
    comments = sorted(comments, key=lambda x: x['created_at'], reverse=True)
    
    return render_template('project_detail.html', project=project, comments=comments)

@public_bp.route('/project/<project_id>/like', methods=['POST'])
def like_project(project_id):
    if not session.get('user_id'):
        return jsonify({'error': 'Login required'}), 401
    
    project = None
    for p in data_store['projects']:
        if p['id'] == project_id:
            project = p
            break
    
    if project:
        project['likes'] = project.get('likes', 0) + 1
        return jsonify({'likes': project['likes']})
    
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
    comment_id = str(uuid.uuid4())
    new_comment = {
        'id': comment_id,
        'project_id': project_id,
        'user_id': session['user_id'],
        'user_name': user_name,
        'text': comment_text,
        'created_at': '2025-08-11T00:00:00Z'  # In production, use datetime.now()
    }
    
    data_store['comments'].append(new_comment)
    
    # Send notification to admin
    try:
        send_comment_notification(project_id, user_name, comment_text)
    except Exception as e:
        print(f"Failed to send notification: {e}")
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('public.project_detail', project_id=project_id))

@public_bp.route('/about')
def about():
    return render_template('about.html', about=data_store['about_info'], 
                         achievements=data_store['achievements'])

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Store contact message
        contact_id = str(uuid.uuid4())
        contact_message = {
            'id': contact_id,
            'name': name,
            'email': email,
            'message': message,
            'created_at': '2025-08-11T00:00:00Z'
        }
        
        if 'contact_messages' not in data_store:
            data_store['contact_messages'] = []
        data_store['contact_messages'].append(contact_message)
        
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    
    return render_template('about.html', about=data_store['about_info'], show_contact=True)

@public_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
