# Django Blog Website

## Project Overview
A fully functional blog website built with Django 5.2.8 and Bootstrap 5. The application features a modern, responsive user interface with complete blog functionality including posts, categories, user authentication, and a comment section.

## Features
- **User Authentication**: Registration, login, and logout functionality
- **Blog Posts**: Full CRUD operations (Create, Read, Update, Delete) for posts
- **Categories**: Organize posts by categories with filtering capabilities
- **Comments**: Users can comment on posts and delete their own comments
- **User Dashboard**: Authors can manage their own posts
- **Admin Panel**: Django admin interface for site administration
- **Responsive Design**: Bootstrap 5 responsive UI that works on all devices
- **Image Uploads**: Support for post images with media file handling
- **Slug-based URLs**: SEO-friendly URLs for posts and categories

## Tech Stack
- **Backend**: Django 5.2.8
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (development)
- **Image Processing**: Pillow
- **Configuration**: python-decouple

## Project Structure
```
blogsite/               # Main project directory
  ├── settings.py       # Django settings
  ├── urls.py          # Main URL configuration
  ├── wsgi.py          # WSGI configuration
  └── asgi.py          # ASGI configuration

blog/                  # Blog application
  ├── models.py        # Category, Post, Comment models
  ├── views.py         # All view functions
  ├── forms.py         # User registration, post, comment forms
  ├── urls.py          # Blog URL patterns
  ├── admin.py         # Admin panel configuration
  ├── context_processors.py  # Categories for navbar
  └── management/commands/   # Custom management commands
      └── populate_data.py   # Populate dummy data

templates/             # HTML templates
  ├── base.html        # Base template with navbar
  └── blog/            # Blog-specific templates
      ├── home.html
      ├── post_detail.html
      ├── post_form.html
      ├── user_dashboard.html
      ├── category_list.html
      ├── login.html
      └── register.html

static/css/           # Custom CSS
media/                # User-uploaded images
```

## Models

### Category
- `name`: Unique category name
- `slug`: Auto-generated URL-friendly slug
- `created_at`: Timestamp

### Post
- `title`: Post title
- `slug`: Auto-generated URL-friendly slug
- `content`: Post content
- `image`: Optional image upload
- `author`: Foreign key to User
- `category`: Foreign key to Category
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Comment
- `post`: Foreign key to Post
- `author`: Foreign key to User
- `content`: Comment text
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## URLs
- `/` - Home page (list all posts)
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/dashboard/` - User dashboard
- `/post/new/` - Create new post
- `/post/<slug>/` - Post detail with comments
- `/post/<slug>/edit/` - Edit post
- `/post/<slug>/delete/` - Delete post
- `/categories/` - List all categories
- `/category/<slug>/` - Posts by category
- `/admin/` - Django admin panel

## Setup Instructions

### Running the Project
The project is configured to run on Replit with a workflow that starts the Django development server on port 5000:

```bash
python manage.py runserver 0.0.0.0:5000
```

### Populate Dummy Data
To populate the database with test data (categories, posts, users, comments):

```bash
python manage.py populate_data
```

This creates:
- An admin user and regular test users with passwords generated at runtime
- 6 categories: Technology, Travel, Food, Lifestyle, Education, Health
- 8 blog posts with content
- Multiple comments on each post

### Database Migrations
If you make changes to models:

```bash
python manage.py makemigrations
python manage.py migrate
```

The generated credentials are printed only in the terminal for that command run.
You can provide `DEMO_ADMIN_PASSWORD` and `DEMO_USER_PASSWORD` as local
environment variables if deterministic seed credentials are needed. Never
commit those values.

## Configuration
- Server runs on port 5000 (configured for Replit webview)
- `ALLOWED_HOSTS` can be supplied as a comma-separated environment variable
- Static files served from `/static/`
- Media files uploaded to `/media/`
- Debug mode enabled (development only)

## Recent Changes
- **2025-11-15**: Initial project setup
  - Created Django project and blog app
  - Implemented all models (Category, Post, Comment)
  - Created all views and URL patterns
  - Designed responsive Bootstrap 5 templates
  - Added user authentication and registration
  - Implemented comment system
  - Created dummy data population command
  - Configured for Replit deployment

## Next Steps / Future Enhancements
- Add pagination for post listings
- Implement post search functionality
- Add rich text editor for post content
- Create user profile pages
- Add email verification for registration
- Implement password reset functionality
- Add post tags/multiple categories
- Create RSS feed
- Add social media sharing
- Implement comment moderation
- Add nested comment replies
- Create API endpoints (Django REST framework)
