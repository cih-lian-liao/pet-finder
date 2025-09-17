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

## 🚀 Future Development

### 🌐 Multi-Site Integration
- **Expanded Data Sources**: Integrate more pet adoption platforms including AdoptAPet.com, Petco Love Lost, PetSmart Charities, etc.
- **Local Shelters**: Direct integration with municipal animal shelters and rescue organizations
- **Unified Search**: Users can search for pets from all sources on a single platform
- **Smart Deduplication**: Automatically identify and merge duplicate pet information from different platforms

### 🤖 Smart Matching System
- **AI Recommendations**: Intelligent pet matching based on user preferences and lifestyle
- **Personalized Suggestions**: Recommend suitable pets based on user's living environment, activity level, etc.
- **Compatibility Scoring**: Provide matching scores for each pet with the user
- **Behavioral Analysis**: Analyze pet personality traits and provide detailed behavioral assessments

### 👤 User Experience Enhancement
- **User Accounts**: Registration and login system to save search history and favorites
- **Smart Notifications**: Email alerts when pets matching criteria become available
- **Interactive Maps**: Visual display of pet locations and shelter information
- **Mobile Application**: Develop mobile apps for more convenient user experience

### 📊 Data Analytics & Insights
- **Trend Analysis**: Analyze adoption trends across different regions and breeds
- **Success Rate Tracking**: Track adoption success rates and user feedback
- **Market Insights**: Provide data analysis reports on the pet adoption market
- **Personalized Statistics**: Offer personalized search and preference statistics for users

### 🤝 Partnership Development
- **Official APIs**: Establish official partnerships with major pet adoption platforms
- **Shelter Collaboration**: Create data sharing agreements with local animal shelters
- **Veterinary Networks**: Integrate health records and recommendations from veterinary clinics
- **Transportation Services**: Provide safe pet transportation services

### 🔧 Technical Improvements
- **Real-time Sync**: Implement more frequent data updates and synchronization
- **Performance Optimization**: Improve search speed and response time
- **Security Enhancement**: Strengthen data protection and user privacy security
- **API Expansion**: Provide richer API interfaces for third-party developers


### 🌟 Feature Vision

#### User Features
- **Smart Matching**: Pet-owner compatibility system based on pet personality and user lifestyle
- **Photo Recognition**: AI-powered breed and trait identification
- **Adoption Tracking**: Track successful adoption cases and follow-ups
- **Educational Resources**: Provide pet care and training guides
- **Virtual Meet & Greet**: Remote interaction with pets through video calls

#### Shelter Tools
- **Management Dashboard**: Complete pet management system for shelters
- **Digital Workflow**: Streamlined adoption applications and approval process
- **Volunteer Management**: Coordinate volunteer activities and scheduling
- **Financial Tracking**: Manage donations and expenses

#### Third-Party Integrations
- **Veterinary Networks**: Integrate health records and vaccination information
- **Pet Stores**: Provide post-adoption supplies and service recommendations
- **Transportation Services**: Coordinate long-distance adoption transportation
- **Insurance Services**: Offer pet insurance advice and comparisons

### 🤝 Community & Ecosystem

#### Open Source Contributions
- **Documentation**: Provide comprehensive user guides and development documentation
- **Plugin System**: Support third-party developer extensions
- **Developer Tools**: Provide SDKs and API interfaces
- **Best Practices**: Establish development standards for pet adoption platforms

#### Partnership Development
- **Primary Data Sources**: Establish partnerships with PetFinder, AdoptAPet, Petco Love Lost, and other platforms
- **Local Shelters**: Create direct partnerships with municipal animal shelters and rescue organizations
- **Veterinary Networks**: Integrate services from veterinary clinics and animal hospitals
- **Technology Partnerships**: Collaborate with cloud service providers, AI service providers, etc.
- **International Expansion**: Partner with animal welfare organizations in Canada, UK, Australia, and other countries

### 📊 Success Metrics

#### User Engagement
- **Active Users**: Monthly and daily active user growth
- **Search Volume**: Number of pet searches per month
- **Adoption Success Rate**: Percentage of searches leading to successful adoptions
- **Time to Adoption**: Average time from search to successful adoption
- **User Retention**: Repeat usage and user engagement metrics

#### Platform Performance
- **Response Time**: API and page load performance
- **Data Accuracy**: Pet information quality and update frequency
- **Security**: Zero critical security vulnerabilities
- **Scalability**: Ability to handle increased user load
- **Availability**: 99.9% uptime target

### 💡 Innovation Opportunities

#### Emerging Technologies
- **Artificial Intelligence**: Advanced pet matching algorithms
- **Augmented Reality**: Virtual pet interaction experiences
- **Blockchain**: Secure adoption record management
- **Internet of Things**: Smart pet monitoring devices
- **Big Data**: Predictive analytics for pet welfare

#### Research & Development
- **Genetic Testing**: Breed and health prediction
- **Behavioral Analysis**: Pet personality assessment
- **Environmental Matching**: Home suitability analysis
- **Predictive Modeling**: Adoption success rate prediction
- **Health Research**: Long-term adoption outcome tracking

---

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
