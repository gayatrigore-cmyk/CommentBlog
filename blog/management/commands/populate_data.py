from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment
from django.utils.text import slugify
import os
import random
import secrets


class Command(BaseCommand):
    help = 'Populate the database with dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        admin_password = os.environ.get('DEMO_ADMIN_PASSWORD') or secrets.token_urlsafe(18)
        user_password = os.environ.get('DEMO_USER_PASSWORD') or secrets.token_urlsafe(18)
        created_credentials = []

        # Create superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', admin_password)
            created_credentials.append(('admin', admin_password))
            self.stdout.write(self.style.SUCCESS('Superuser created: admin'))
        
        # Create regular users
        users = []
        for i in range(1, 4):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username,
                    f'{username}@example.com',
                    user_password,
                )
                users.append(user)
                created_credentials.append((username, user_password))
                self.stdout.write(self.style.SUCCESS(f'User created: {username}'))
            else:
                users.append(User.objects.get(username=username))

        # Create categories
        category_names = ['Technology', 'Travel', 'Food', 'Lifestyle', 'Education', 'Health']
        categories = []
        for name in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category created: {name}'))

        # Create posts
        post_data = [
            {
                'title': 'Getting Started with Django',
                'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It\'s free and open source.\n\nDjango was designed to help developers take applications from concept to completion as quickly as possible. It includes dozens of extras you can use to handle common web development tasks. Django takes care of user authentication, content administration, site maps, RSS feeds, and many more tasks — right out of the box.',
                'category': 'Technology'
            },
            {
                'title': 'Best Travel Destinations for 2025',
                'content': 'Planning your next adventure? Here are the top destinations you should consider visiting in 2025. From pristine beaches to bustling cities, these locations offer unforgettable experiences.\n\nJapan continues to be a favorite with its perfect blend of ancient traditions and modern innovation. The cherry blossoms in spring and autumn foliage create magical atmospheres. Iceland offers breathtaking natural wonders including waterfalls, geysers, and the Northern Lights.',
                'category': 'Travel'
            },
            {
                'title': 'Delicious Homemade Pizza Recipe',
                'content': 'Making pizza at home is easier than you think! With the right ingredients and technique, you can create restaurant-quality pizza in your own kitchen.\n\nStart with a simple dough made from flour, water, yeast, salt, and olive oil. Let it rise for at least an hour, or overnight in the refrigerator for better flavor. The key to great pizza is a very hot oven - preheat to the highest temperature possible.',
                'category': 'Food'
            },
            {
                'title': 'Minimalist Living: A Beginner\'s Guide',
                'content': 'Minimalism isn\'t about having less for the sake of having less. It\'s about making room for more of what matters. By removing the excess, we create space for the things that truly bring us joy and fulfillment.\n\nStart small - declutter one room or even one drawer at a time. Ask yourself if each item adds value to your life. If it doesn\'t serve a purpose or bring you joy, consider letting it go.',
                'category': 'Lifestyle'
            },
            {
                'title': 'The Future of Online Learning',
                'content': 'The education landscape has transformed dramatically in recent years. Online learning platforms have made quality education accessible to millions worldwide.\n\nInteractive courses, virtual classrooms, and AI-powered tutoring are revolutionizing how we learn. Students can now access world-class education from anywhere, at their own pace. The future of learning is personalized, flexible, and inclusive.',
                'category': 'Education'
            },
            {
                'title': '10 Simple Habits for Better Health',
                'content': 'Good health doesn\'t require drastic changes. Small, consistent habits can make a big difference over time.\n\n1. Drink more water - aim for 8 glasses daily\n2. Get 7-9 hours of sleep\n3. Move your body for 30 minutes daily\n4. Eat more whole foods\n5. Practice gratitude\n6. Limit screen time before bed\n7. Take regular breaks when sitting\n8. Connect with loved ones\n9. Spend time outdoors\n10. Manage stress through meditation or yoga',
                'category': 'Health'
            },
            {
                'title': 'Bootstrap 5: What\'s New and Improved',
                'content': 'Bootstrap 5 brings exciting new features and improvements to the world\'s most popular front-end framework. With the removal of jQuery dependency, it\'s lighter and more modern than ever.\n\nNew utility classes make responsive design even easier. The updated grid system offers more flexibility, and the new offcanvas component is perfect for modern navigation patterns. If you\'re building websites, Bootstrap 5 is definitely worth exploring.',
                'category': 'Technology'
            },
            {
                'title': 'Hidden Gems: Underrated European Cities',
                'content': 'While Paris, Rome, and Barcelona are amazing, Europe has countless lesser-known cities worth visiting. These hidden gems offer authentic experiences without the overwhelming crowds.\n\nPorto, Portugal charms visitors with its colorful buildings and port wine cellars. Ljubljana, Slovenia combines Austrian and Mediterranean influences in a compact, walkable city. Bruges, Belgium feels like stepping into a medieval fairy tale.',
                'category': 'Travel'
            }
        ]

        posts = []
        for i, data in enumerate(post_data):
            category = Category.objects.get(name=data['category'])
            author = random.choice(users)
            
            title = data['title']
            slug = slugify(title)
            
            if not Post.objects.filter(slug=slug).exists():
                post = Post.objects.create(
                    title=title,
                    slug=slug,
                    content=data['content'],
                    author=author,
                    category=category
                )
                posts.append(post)
                self.stdout.write(self.style.SUCCESS(f'Post created: {title}'))

        # Create comments
        if posts:
            comment_texts = [
                'Great article! Thanks for sharing.',
                'This is exactly what I was looking for.',
                'Very informative and well-written.',
                'I learned a lot from this post.',
                'Looking forward to more content like this!',
                'Excellent tips, will definitely try these.',
                'This helped me so much, thank you!',
                'Well explained and easy to follow.',
            ]

            for post in posts:
                num_comments = random.randint(2, 5)
                for _ in range(num_comments):
                    Comment.objects.create(
                        post=post,
                        author=random.choice(users),
                        content=random.choice(comment_texts)
                    )
            self.stdout.write(self.style.SUCCESS(f'Comments created for all posts'))

        self.stdout.write(self.style.SUCCESS('✓ Dummy data populated successfully!'))
        if created_credentials:
            self.stdout.write(self.style.WARNING(
                '\nCredentials created during this run (do not commit or reuse them):'
            ))
            for username, password in created_credentials:
                self.stdout.write(f'  {username}: {password}')
        else:
            self.stdout.write('No new users were created; existing passwords were unchanged.')
