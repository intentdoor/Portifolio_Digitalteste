import uuid
from werkzeug.security import generate_password_hash

# In-memory data store for MVP
data_store = {
    'users': [],
    'projects': [],
    'achievements': [],
    'comments': [],
    'about_info': {
        'title': 'Welcome to My Portfolio',
        'description': 'I am a passionate developer creating amazing digital experiences.',
        'skills': ['Web Development', 'UI/UX Design', 'Project Management'],
        'contact_email': 'contact@portfolio.com'
    }
}

def init_data_store():
    """Initialize data store with default admin user"""
    if not data_store['users']:
        # Create default admin user
        admin_id = str(uuid.uuid4())
        admin_user = {
            'id': admin_id,
            'name': 'Admin User',
            'email': 'admin@portfolio.com',
            'password_hash': generate_password_hash('admin123'),  # Change this in production
            'is_admin': True,
            'profile_image': None
        }
        data_store['users'].append(admin_user)
        
        # Add some sample projects (remove in production)
        sample_projects = [
            {
                'id': str(uuid.uuid4()),
                'title': 'E-Commerce Platform',
                'description': 'A full-stack e-commerce solution built with modern web technologies. Features include user authentication, shopping cart, payment integration, and admin dashboard.',
                'tags': ['Web Development', 'Full Stack', 'E-commerce'],
                'status': 'published',
                'link': 'https://github.com/example/ecommerce',
                'image': None,
                'likes': 15,
                'created_at': '2025-08-01T00:00:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Mobile Task Manager',
                'description': 'A responsive task management application with drag-and-drop functionality, real-time updates, and collaborative features.',
                'tags': ['Mobile Development', 'React', 'UI/UX'],
                'status': 'published',
                'link': 'https://github.com/example/taskmanager',
                'image': None,
                'likes': 8,
                'created_at': '2025-07-15T00:00:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Data Visualization Dashboard',
                'description': 'An interactive dashboard for visualizing complex datasets with customizable charts, filters, and real-time data updates.',
                'tags': ['Data Visualization', 'Dashboard', 'Analytics'],
                'status': 'draft',
                'link': '',
                'image': None,
                'likes': 3,
                'created_at': '2025-08-10T00:00:00Z'
            }
        ]
        data_store['projects'].extend(sample_projects)
        
        # Add sample achievements
        sample_achievements = [
            {
                'id': str(uuid.uuid4()),
                'title': 'Certified Web Developer',
                'description': 'Completed advanced web development certification with distinction.',
                'date': '2025-06-01'
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Best Project Award',
                'description': 'Won the "Best Innovation" award at the annual tech conference.',
                'date': '2025-05-15'
            }
        ]
        data_store['achievements'].extend(sample_achievements)

def get_user_by_id(user_id):
    """Get user by ID"""
    for user in data_store['users']:
        if user['id'] == user_id:
            return user
    return None

def get_project_by_id(project_id):
    """Get project by ID"""
    for project in data_store['projects']:
        if project['id'] == project_id:
            return project
    return None
