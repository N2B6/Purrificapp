# Purrfect Dog - Pet Management Web Application

<img src="home.png" alt="Pet Management App" width="600">

A Django-based web application for pet lovers to manage their pets, events, and connect with other pet owners. Originally built with AWS cloud services, now deployed on Render with SQLite.

## Key Features
- 🐾 User registration & authentication
- 🐶 Pet profile management (add/edit/delete pets)
- 📅 Event creation and management for pet meetups
- 📞 Contact form for user inquiries
- 🔍 Search & filter pets by type, breed, age
- 📸 Image uploads for pets and events
- 📱 Responsive design for mobile devices
- 🔍 **Advanced Search** powered by custom-made [petsearch](#petsearch-library) library

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Django 5.0
- **Database**: SQLite (RDS MySQL version available in AWS branch)
- **Deployment**: Render.com (AWS Elastic Beanstalk version available in AWS branch)
- **Storage**: Local file storage (AWS S3 version available in AWS branch)

## Installation (Local Development)
1. Clone repository:
   ```bash
   git clone https://github.com/N2B6/Purrificapp.git
   cd Purrificapp
   ```


2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

<!-- ## Deployment on Render
1. Create new **Web Service** on Render
2. Connect your GitHub repository
3. Set environment variables:
   ```env
   PYTHON_VERSION = 3.9.6
   DJANGO_SETTINGS_MODULE = CAT.settings
   ```
4. Set build command:
   ```bash
   pip install -r requirements.txt && python manage.py migrate
   ```
5. Set start command:
   ```bash
   gunicorn CAT.wsgi:application -->
   <!-- ``` -->

## AWS Architecture (Original Implementation)
This project was originally deployed using these AWS services:

```plaintext
- Cloud9 IDE: Development Environment
- GitHub Repository: Version Control
- CodePipeline: CI/CD Orchestration
- CodeBuild: Build Automation
- CodeDeploy: Deployment Service
- Elastic Beanstalk: Application Hosting
- Amazon RDS MySQL: Database Service
- Amazon S3 Bucket: Media Storage
- Amazon SNS: Notification Service
```

```mermaid
graph TD
    classDef aws_env fill:#e3f2fd,color:#0a1f4a
    classDef ci_cd fill:#e0f7fa,color:#003d40
    classDef app_layer fill:#fff3e0,color:#b33c00
    classDef storage fill:#f3e5f5,color:#4a126b
    classDef notifications fill:#ffebee,color:#8a1b1b

    subgraph DevEnv["Development Environment"]
        C9[Cloud9 IDE]:::dev-tools
        GH[GitHub Repository]:::dev-tools
    end
    class DevEnv aws_env

    subgraph Pipeline["CI/CD Pipeline"]
        CP[CodePipeline]:::pipeline
        CB[CodeBuild]:::pipeline
        CD[CodeDeploy]:::pipeline
    end
    class Pipeline ci_cd

    subgraph AppLayer["Application Layer"]
        EB[Elastic Beanstalk]:::hosting
        APP[Django Web App]:::hosting
    end
    class AppLayer app_layer

    subgraph Storage["Storage Layer"]
        RDS[(Amazon RDS MySQL)]:::database
        S3[Amazon S3 Bucket]:::storage-service
    end
    class Storage storage

    subgraph Notifications["Notification Service"]
        SNS[Amazon SNS]:::messaging
        EMAIL[Email Notifications]:::messaging
    end
    class Notifications notifications

    C9 -->|Push Code| GH
    GH -->|Webhooks Trigger| CP
    CP -->|Build Stage| CB
    CB -->|Artifact| CD
    CD -->|Deploy Stage| EB
    EB --> |Host| APP
    APP -->|Store Data| RDS
    APP -->|Static Files| S3
    APP -->|Send Notifications| SNS
    SNS -->|Deliver| EMAIL

    classDef dev-tools fill:#e6f3ff,stroke:#0066cc,color:#0a1f4a,stroke-width:2px
    classDef pipeline fill:#e0f7fa,stroke:#0097a7,color:#003d40,stroke-width:2px
    classDef hosting fill:#fff3e0,stroke:#ef6c00,color:#b33c00,stroke-width:2px
    classDef database fill:#f3e5f5,stroke:#9c27b0,color:#4a126b,stroke-width:2px
    classDef storage-service fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px
    classDef messaging fill:#ffebee,stroke:#d32f2f,color:#8a1b1b,stroke-width:2px
```

## Project Structure
```plaintext
purrfect-dog/
├── CAT/                   # Django project config
│   ├── __init__.py
│   ├── settings.py        # Combined AWS/Render settings
│   ├── urls.py
│   └── wsgi.py
├── KITTEN/                # Main application
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html      # Base template
│   │   └── mylistings.html # Pet listings
│   ├── static/
│   │   ├── admin/         # Django admin static files
│   │   ├── css/           # Custom styles
│   │   └── js/            # Custom scripts
│   ├── models.py          # Database models
│   ├── views.py           # Application logic
│   └── urls.py            # URL routing
├── petsearch/             # Custom search library
│   └── petsearch.egg-info/
├── requirements.txt       # Dependencies
└── manage.py              # Django CLI
```

## petsearch Library
Custom Python library for pet filtering and sorting. Key capabilities:

```python
# Example usage in views.py
from petsearch import PetFilter

def pet_list(request):
    filters = {
        'type': request.GET.get('pet_type'),
        'age_min': request.GET.get('age_min'),
        'breed': request.GET.get('breed')
    }
    filtered_pets = PetFilter(filters).execute()
    return render(request, 'mylistings.html', {'pets': filtered_pets})
```

**Features**:
- Multi-criteria filtering (type, breed, age)
- Weighted sorting algorithm
- Pagination support
- Search relevance scoring

## Credits
- Developed by [Nipun Bakshi](https://www.linkedin.com/in/nipunbakshi/)
- Django Framework 5.0
- Render.com for free hosting

<!-- [![View Live Demo on Render](https://img.shields.io/badge/View_Live_Demo-Render-5f3dc4?style=for-the-badge&logo=render&logoColor=white&labelColor=000000)](https://purrificapp.onrender.com) -->



<!-- Or for HTML-compatible rendering (e.g., GitHub Pages) -->
<a href="https://purrificapp.onrender.com" style="display: inline-block; padding: 12px 24px; background-color: #5f3dc4; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s ease; border: 2px solid #4a2fa3; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
    🚀 Check it live on Render
</a>
