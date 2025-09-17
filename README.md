# 🐾 Pet Finder

A modern Django web application for finding adoptable pets from PetFinder.com. This application scrapes pet data and provides a beautiful, user-friendly interface for browsing and filtering pets available for adoption.

## ✨ Features

- **🔍 Advanced Search**: Search pets by location, animal type, and distance
- **🎨 Modern UI**: Beautiful, responsive design with Bootstrap 5
- **📊 Statistics Dashboard**: Comprehensive analytics and charts
- **🔧 Data Management**: Export data as CSV, clear database
- **📱 Mobile Friendly**: Fully responsive design
- **⚡ Fast Performance**: Optimized queries and caching
- **🛡️ Secure**: Input validation, CSRF protection, and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pet-finder
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000`

## 📖 Usage

### Searching for Pets

1. **Enter search criteria**:
   - City (e.g., "Seattle")
   - State/Province (e.g., "WA")
   - Animal type (dogs, cats, etc.)
   - Search radius in miles

2. **Click "Find Pets"** to start scraping

3. **Browse results** using the modern card-based interface

4. **Filter results** by breed, gender, size, or age

### Managing Data

- **Clear All**: Remove all pets from the database
- **Download CSV**: Export all pet data as a CSV file
- **Statistics**: View comprehensive analytics and charts

## 🏗️ Project Structure

```
pet-finder/
├── scraper/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── website/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic (class-based views)
│   ├── forms.py           # Django forms
│   ├── services.py        # Business logic layer
│   ├── admin.py           # Admin interface
│   └── templates/         # HTML templates
│       ├── homepage.html  # Main page
│       └── pet_stats.html # Statistics page
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and customize:

```bash
cp env.example .env
```

Key settings:
- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Enable/disable debug mode
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database

By default, the application uses SQLite for development. For production, configure a PostgreSQL database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'petfinder_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-django

# Run tests
pytest

# Run with coverage
coverage run -m pytest
coverage report
```

## 🚀 Deployment

### Production Settings

1. **Set environment variables**:
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export DEBUG=False
   export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
   ```

2. **Install production dependencies**:
   ```bash
   pip install gunicorn whitenoise
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Run with Gunicorn**:
   ```bash
   gunicorn scraper.wsgi:application
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "scraper.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📊 API Documentation

The application provides several endpoints:

- `GET /` - Homepage with search form and pet listings
- `POST /` - Process search form and scrape pets
- `POST /clear/` - Clear all pets from database
- `GET /download/` - Download pets data as CSV
- `GET /stats/` - View statistics dashboard
- `GET /admin/` - Django admin interface

## 🛠️ Development

### Code Quality

The project uses several tools for code quality:

```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Type checking (if using mypy)
mypy .
```

### Adding New Features

1. **Create models** in `website/models.py`
2. **Add forms** in `website/forms.py`
3. **Implement business logic** in `website/services.py`
4. **Create views** in `website/views.py`
5. **Update templates** in `website/templates/`
6. **Add URL patterns** in `scraper/urls.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [PetFinder.com](https://www.petfinder.com/) for providing the pet data API
- [Django](https://djangoproject.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components
- [Chart.js](https://www.chartjs.org/) for the statistics charts

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔄 Changelog

### Version 2.0.0 (Current)
- ✨ Complete redesign with modern UI
- 🏗️ Refactored to use class-based views
- 📊 Added comprehensive statistics dashboard
- 🔧 Improved error handling and validation
- 📱 Enhanced mobile responsiveness
- 🛡️ Better security and input validation
- ⚡ Performance optimizations

### Version 1.0.0
- 🎉 Initial release
- 🔍 Basic pet searching functionality
- 📄 Simple table-based interface
- 💾 CSV export feature

---

Made with ❤️ for pet lovers everywhere! 🐾
