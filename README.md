# CommentBlog

CommentBlog is a server-rendered Django blog application with user accounts,
category browsing, post management, image uploads, and a comment section.
It is styled with Bootstrap and custom CSS and is configured for local
development and Replit deployment.

## Features

- User registration, login, logout, and session-based authentication
- Create, view, edit, and delete blog posts
- Ownership checks so authors can manage only their own posts
- Optional post image uploads
- Categories with SEO-friendly slug URLs
- Authenticated comments on blog posts
- Users can delete their own comments
- Personal dashboard for each author
- Django admin panel for site administration
- Responsive Bootstrap 5 interface
- Static file serving through WhiteNoise in production
- Demo data management command for local development

## Technology stack

- **Python 3.12+**
- **Django 5.2.8**
- **SQLite** for the current development database
- **Django ORM** and migrations
- **Django built-in authentication**
- **Bootstrap 5.3** and **Bootstrap Icons**
- **HTML5 and CSS3**
- **Pillow** for image uploads
- **Gunicorn** for production WSGI serving
- **WhiteNoise** for production static files
- **Replit Autoscale** deployment configuration

## Project structure

```text
CommentBlog/
├── blog/                     # Blog application
│   ├── models.py             # Category, Post, and Comment models
│   ├── views.py              # Page and form handling
│   ├── forms.py              # Registration, post, category, comment forms
│   ├── urls.py               # Blog routes
│   ├── admin.py              # Django admin configuration
│   ├── migrations/           # Database migrations
│   └── management/commands/ # Custom management commands
├── blogsite/                 # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/                # Server-rendered HTML templates
├── static/                   # Custom CSS and favicon
├── media/                    # Local uploaded media directory
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .replit                   # Replit workflow and deployment settings
```

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/gayatrigore-cmyk/CommentBlog.git
cd CommentBlog
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

At minimum, provide a secret key:

```bash
export SECRET_KEY="replace-this-with-a-long-random-value"
export DEBUG=True
```

For a hosted environment, use:

```bash
export DEBUG=False
export SECRET_KEY="replace-this-with-a-long-random-value"
export ALLOWED_HOSTS="your-domain.example,www.your-domain.example"
```

Do not commit `.env` files or real secret values. Replit users can store
secrets in the workspace Secrets tool instead of putting them in source code.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Optional: create sample content

```bash
python manage.py populate_data
```

The command creates sample users, categories, posts, and comments. Passwords
for newly created sample users are generated at runtime and printed only to
the terminal. To provide temporary local seed passwords, use environment
variables without committing them:

```bash
export DEMO_ADMIN_PASSWORD="temporary-local-password"
export DEMO_USER_PASSWORD="temporary-local-password"
python manage.py populate_data
```

### 7. Start the development server

```bash
python manage.py runserver 0.0.0.0:5000
```

Open `http://127.0.0.1:5000/`.

## Main routes

| Route | Purpose |
|---|---|
| `/` | Blog homepage |
| `/register/` | Register a user |
| `/login/` | Log in |
| `/logout/` | Log out |
| `/dashboard/` | Manage the current user's posts |
| `/post/new/` | Create a post |
| `/post/<slug>/` | View a post and comments |
| `/post/<slug>/edit/` | Edit an owned post |
| `/post/<slug>/delete/` | Delete an owned post |
| `/categories/` | Browse categories |
| `/category/<slug>/` | Browse posts in a category |
| `/admin/` | Django administration |

## Production serving

Collect static files and run Gunicorn:

```bash
python manage.py collectstatic --no-input
DEBUG=False gunicorn --bind 0.0.0.0:5000 --reuse-port blogsite.wsgi:application
```

The included Replit configuration uses the same Gunicorn command with
Autoscale deployment and runs `collectstatic` as its build step.

## Security and deployment notes

- `SECRET_KEY` and `SESSION_SECRET` are read from environment variables.
- If production runs with `DEBUG=False` and no secret is configured, Django
  stops with an explicit configuration error.
- Local development can generate a temporary in-memory key when `DEBUG=True`.
- Local SQLite databases, uploaded media, environment files, caches, and
  collected static files are excluded by `.gitignore`.
- SQLite and local media are appropriate for a demo or single instance, but
  a serious multi-instance deployment should use a persistent PostgreSQL
  database and persistent object storage for uploads.
- Set `ALLOWED_HOSTS` to the real production hostnames instead of using `*`
  for a hardened deployment.

## Development checks

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
```

## License

No license has been selected for this repository yet. Add a license file
before distributing the project outside your own use.