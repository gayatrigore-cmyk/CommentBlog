from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Post, Category, Comment
from .forms import UserRegistrationForm, PostForm, CategoryForm, CommentForm


def favicon(request):
    return FileResponse(
        open(settings.BASE_DIR / 'static' / 'favicon.svg', 'rb'),
        content_type='image/svg+xml',
    )


def home(request):
    posts = Post.objects.all().select_related('author', 'category').annotate(comment_count=Count('comments'))
    context = {
        'posts': posts,
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('author', 'category'), slug=slug)
    comments = post.comments.all().select_related('author')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': 'Edit Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('home')
    
    context = {
        'post': post,
        'title': 'Delete Post'
    }
    return render(request, 'blog/post_confirm_delete.html', context)


def category_list(request):
    categories = Category.objects.annotate(post_count=Count('posts'))
    context = {
        'categories': categories,
        'title': 'Categories'
    }
    return render(request, 'blog/category_list.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all().select_related('author', 'category').annotate(comment_count=Count('comments'))
    context = {
        'category': category,
        'posts': posts,
        'title': f'{category.name} Posts'
    }
    return render(request, 'blog/category_posts.html', context)


@login_required
def user_dashboard(request):
    user_posts = Post.objects.filter(author=request.user).select_related('category').annotate(comment_count=Count('comments'))
    context = {
        'user_posts': user_posts,
        'title': 'My Dashboard'
    }
    return render(request, 'blog/user_dashboard.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'blog/register.html', context)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', slug=post_slug)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted.')
        return redirect('post_detail', slug=post_slug)
    
    context = {
        'comment': comment,
        'title': 'Delete Comment'
    }
    return render(request, 'blog/comment_confirm_delete.html', context)
