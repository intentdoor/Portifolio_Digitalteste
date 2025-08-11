# Spider Portfolio - Digital Portfolio Web Application

A Flask-based interactive digital portfolio with a dark spider theme, featuring both administrative and public areas for showcasing projects and achievements.

## Features

- **Spider-themed Dark Design**: Gothic aesthetic with red/black color scheme and cool animations
- **Admin Dashboard**: Complete content management system for projects, achievements, and user interactions
- **User Authentication**: Registration, login, and session management
- **Project Showcase**: Display projects with images, tags, likes, and comments
- **File Upload System**: Secure image uploads for project portfolios
- **Email Notifications**: SMTP integration for comment notifications
- **Responsive Design**: Bootstrap-based responsive layout with dark theme

## Theme Features

- Dark background with spider web patterns
- Glowing red text effects and animations
- Spider icons throughout the interface
- Cool hover effects with red glowing shadows
- Gothic, dark aesthetic with spider motifs

## Technology Stack

- **Backend**: Flask with Blueprint architecture
- **Frontend**: Bootstrap 5 Dark Theme, Font Awesome icons
- **Authentication**: Session-based with password hashing
- **Storage**: In-memory data store (easily migrated to database)
- **Deployment**: Gunicorn WSGI server

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd spider-portfolio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export SESSION_SECRET=your-secret-key-here
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
```

4. Run the application:
```bash
python main.py
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login
2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set SESSION_SECRET=your-secret-key
heroku config:set SMTP_SERVER=smtp.gmail.com
heroku config:set SMTP_PORT=587
heroku config:set SMTP_USERNAME=your-email@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password
```

4. Deploy:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Local Development

Run with debug mode:
```bash
export FLASK_ENV=development
python main.py
```

## Default Admin Access

- **Username**: admin
- **Password**: admin123

**Important**: Change these credentials after first login!

## Project Structure

```
spider-portfolio/
├── app.py              # Flask app initialization
├── main.py             # Application entry point
├── routes/             # Blueprint route handlers
│   ├── auth.py         # Authentication routes
│   ├── admin.py        # Admin dashboard routes
│   └── public.py       # Public portfolio routes
├── models/             # Data models and storage
│   └── data_store.py   # In-memory data store
├── templates/          # Jinja2 templates
├── static/             # CSS, JS, and asset files
├── uploads/            # User uploaded files
└── utils/              # Utility functions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please create an issue in the GitHub repository.