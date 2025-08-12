import uuid
from werkzeug.security import generate_password_hash

# In-memory data store for MVP
data_store = {
    'users': [],
    'projects': [],
    'achievements': [],
    'comments': [],
    'about_info': {
        'title': 'Bem-vindo ao Meu Portfólio',
        'description': 'Sou um desenvolvedor apaixonado criando experiências digitais incríveis.',
        'skills': ['Desenvolvimento Web', 'UI/UX Design', 'Gerenciamento de Projetos'],
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
            'name': 'Usuário Admin',
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
                'title': 'Plataforma E-Commerce',
                'description': 'Uma solução completa de e-commerce construída com tecnologias web modernas. Inclui autenticação de usuários, carrinho de compras, integração de pagamentos e painel administrativo.',
                'tags': ['Desenvolvimento Web', 'Full Stack', 'E-commerce'],
                'status': 'published',
                'link': 'https://github.com/example/ecommerce',
                'image': None,
                'likes': 15,
                'created_at': '2025-08-01T00:00:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Gerenciador de Tarefas Mobile',
                'description': 'Uma aplicação responsiva de gerenciamento de tarefas com funcionalidade de arrastar e soltar, atualizações em tempo real e recursos colaborativos.',
                'tags': ['Desenvolvimento Mobile', 'React', 'UI/UX'],
                'status': 'published',
                'link': 'https://github.com/example/taskmanager',
                'image': None,
                'likes': 8,
                'created_at': '2025-07-15T00:00:00Z'
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Dashboard de Visualização de Dados',
                'description': 'Um painel interativo para visualizar conjuntos de dados complexos com gráficos personalizáveis, filtros e atualizações de dados em tempo real.',
                'tags': ['Visualização de Dados', 'Dashboard', 'Analytics'],
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
                'title': 'Desenvolvedor Web Certificado',
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
