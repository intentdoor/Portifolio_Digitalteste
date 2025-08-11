# Digital Portfolio

## Overview

This is a Flask-based digital portfolio web application that allows the owner to showcase projects and achievements while providing visitor interaction features. The system consists of two main areas: an administrative backend for content management and a public frontend for displaying portfolio content. Users can register, authenticate, like projects, and comment on published work, while the admin can manage all content through a comprehensive dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask with Blueprint Architecture**: The application uses Flask as the web framework with a modular blueprint structure separating authentication (`auth_bp`), admin (`admin_bp`), and public (`public_bp`) routes. This promotes code organization and maintainability.
- **In-Memory Data Store**: Currently uses a Python dictionary-based data store for MVP functionality, making it easy to prototype and test. The data store is initialized with default admin credentials and sample projects.
- **Session-Based Authentication**: Implements simple session-based authentication with password hashing using Werkzeug's security utilities.

### Frontend Architecture
- **Server-Side Rendered Templates**: Uses Jinja2 templating with a base template system for consistent UI components across all pages.
- **Bootstrap Dark Theme**: Leverages Bootstrap 5 with a dark theme for responsive design and modern aesthetics.
- **Progressive Enhancement**: JavaScript functionality is layered on top of functional HTML forms, ensuring the application works without JavaScript.

### Data Models
The application manages four core data entities:
- **Users**: Stores user credentials, profile information, and admin status
- **Projects**: Contains project details, status (published/draft), tags, likes count, and media links
- **Achievements**: Tracks accomplishments and milestones with dates and descriptions  
- **Comments**: Manages user comments on projects with timestamps and user associations
- **About Info**: Stores customizable portfolio owner information including skills and contact details

### File Upload System
- **Werkzeug Secure Filename**: Implements secure file upload handling with filename sanitization
- **Size Limitations**: Enforces 16MB maximum file size for uploads
- **Upload Directory Management**: Automatically creates and manages upload directories

### Security Features
- **Admin Authentication Decorator**: Custom decorator ensures admin-only access to management functions
- **Password Hashing**: Uses Werkzeug's generate_password_hash for secure password storage
- **Session Management**: Implements proper session handling with configurable secret keys
- **Input Validation**: Form validation on both client and server sides

### Email Notification System
- **SMTP Integration**: Configurable SMTP settings for sending comment notifications to admin users
- **Environment-Based Configuration**: Uses environment variables for SMTP credentials and server settings

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework for Python
- **Werkzeug**: WSGI utility library providing security utilities and file upload handling

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN with dark theme support
- **Font Awesome 6**: Icon library for UI components
- **Custom CSS/JS**: Local static files for portfolio-specific styling and functionality

### Email Services
- **SMTP Server**: Configurable email service (defaults to Gmail SMTP) for comment notifications
- **Environment Variables**: SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD for email configuration

### Deployment Infrastructure
- **ProxyFix Middleware**: Handles reverse proxy headers for proper deployment behind load balancers or reverse proxies
- **Environment Configuration**: Uses environment variables for secret keys and external service credentials

### Future Database Migration
The current in-memory data store is designed for easy migration to a persistent database solution like PostgreSQL with minimal code changes required in the data access layer.