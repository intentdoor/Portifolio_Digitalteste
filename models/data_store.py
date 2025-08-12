from datetime import date


def init_database_data():
    """Initialize database with default data if empty"""
    from models.models import db, User, Project, Achievement, AboutInfo
    
    # Check if admin user exists
    admin_user = User.query.filter_by(email='admin@portfolio.com').first()
    
    if not admin_user:
        # Create default admin user
        admin_user = User(
            name='Usuário Admin',
            email='admin@portfolio.com',
            is_admin=True
        )
        admin_user.set_password('admin123')  # Change this in production
        db.session.add(admin_user)
        
        # Add about info
        about_info = AboutInfo(
            title='Bem-vindo ao Meu Portfólio',
            description='Sou um desenvolvedor apaixonado criando experiências digitais incríveis.',
            skills=['Desenvolvimento Web', 'UI/UX Design', 'Gerenciamento de Projetos'],
            contact_email='contact@portfolio.com'
        )
        db.session.add(about_info)
        
        # Add sample projects
        sample_projects = [
            Project(
                title='Plataforma E-Commerce',
                description='Uma solução completa de e-commerce construída com tecnologias web modernas. Inclui autenticação de usuários, carrinho de compras, integração de pagamentos e painel administrativo.',
                tags=['Desenvolvimento Web', 'Full Stack', 'E-commerce'],
                status='published',
                link='https://github.com/example/ecommerce',
                likes=15
            ),
            Project(
                title='Gerenciador de Tarefas Mobile',
                description='Uma aplicação responsiva de gerenciamento de tarefas com funcionalidade de arrastar e soltar, atualizações em tempo real e recursos colaborativos.',
                tags=['Desenvolvimento Mobile', 'React', 'UI/UX'],
                status='published',
                link='https://github.com/example/taskmanager',
                likes=8
            ),
            Project(
                title='Dashboard de Visualização de Dados',
                description='Um painel interativo para visualizar conjuntos de dados complexos com gráficos personalizáveis, filtros e atualizações de dados em tempo real.',
                tags=['Visualização de Dados', 'Dashboard', 'Analytics'],
                status='draft',
                likes=3
            )
        ]
        
        for project in sample_projects:
            db.session.add(project)
        
        # Add sample achievements
        sample_achievements = [
            Achievement(
                title='Desenvolvedor Web Certificado',
                description='Completed advanced web development certification with distinction.',
                date=date(2025, 6, 1)
            ),
            Achievement(
                title='Best Project Award',
                description='Won the "Best Innovation" award at the annual tech conference.',
                date=date(2025, 5, 15)
            )
        ]
        
        for achievement in sample_achievements:
            db.session.add(achievement)
        
        db.session.commit()


# Legacy compatibility functions for gradual migration
def get_user_by_id(user_id):
    """Get user by ID - now uses database"""
    from models.models import User
    return User.query.get(user_id)

def get_project_by_id(project_id):
    """Get project by ID - now uses database"""
    from models.models import Project
    return Project.query.get(project_id)
