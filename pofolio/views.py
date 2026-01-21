from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, BlogPost, Service, ContactMessage, Testimonial, Skill

# ========================================
# HOME VIEW
# ========================================
def home(request):
    """Homepage with featured content"""
    context = {
        'featured_projects': Project.objects.filter(featured=True)[:3],
        'featured_posts': BlogPost.objects.filter(status='published', featured=True)[:3],
        'skills': Skill.objects.filter(show_on_home=True),
        'testimonials': Testimonial.objects.filter(active=True, featured=True)[:3],
        'page_title': 'Home - Simon Macharia'
    }
    return render(request, 'pofolio/home.html', context)


# ========================================
# ABOUT VIEW
# ========================================
def about(request):
    """About page with full story and skills"""
    context = {
        'skills': Skill.objects.all(),
        'testimonials': Testimonial.objects.filter(active=True),
        'page_title': 'About Me - Simon Macharia'
    }
    return render(request, 'pofolio/about.html', context)


# ========================================
# PROJECTS VIEWS
# ========================================
def projects(request):
    """Projects listing page with filter"""
    category = request.GET.get('category', None)
    search = request.GET.get('search', None)
    
    projects_list = Project.objects.all()
    
    # Filter by category
    if category:
        projects_list = projects_list.filter(category=category)
    
    # Search functionality
    if search:
        projects_list = projects_list.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(technologies__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(projects_list, 9)  # 9 projects per page
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    context = {
        'projects': projects_page,
        'categories': Project.CATEGORY_CHOICES,
        'current_category': category,
        'search_query': search,
        'page_title': 'Projects - Simon Macharia'
    }
    return render(request, 'pofolio/projects.html', context)


def project_detail(request, slug):
    """Single project detail page"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'page_title': f'{project.title} - Projects'
    }
    return render(request, 'pofolio/project_detail.html', context)


# ========================================
# BLOG VIEWS
# ========================================
def blog(request):
    """Blog listing page"""
    category = request.GET.get('category', None)
    search = request.GET.get('search', None)
    
    posts_list = BlogPost.objects.filter(status='published')
    
    # Filter by category
    if category:
        posts_list = posts_list.filter(category=category)
    
    # Search functionality
    if search:
        posts_list = posts_list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    # Get all categories for filter
    all_categories = BlogPost.objects.filter(status='published').values_list('category', flat=True).distinct()
    
    context = {
        'posts': posts_page,
        'categories': all_categories,
        'current_category': category,
        'search_query': search,
        'page_title': 'Blog - Simon Macharia'
    }
    return render(request, 'pofolio/blog.html', context)


def blog_detail(request, slug):
    """Single blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment views
    post.increment_views()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': f'{post.title} - Blog'
    }
    return render(request, 'pofolio/blog_detail.html', context)


# ========================================
# SERVICES VIEW
# ========================================
def services(request):
    """Services page"""
    services_list = Service.objects.filter(active=True)
    testimonials = Testimonial.objects.filter(active=True, featured=True)
    
    context = {
        'services': services_list,
        'testimonials': testimonials,
        'page_title': 'Services - Simon Macharia'
    }
    return render(request, 'pofolio/services.html', context)


# ========================================
# CONTACT VIEWS
# ========================================
def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')
        
        # Create contact message
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('contact')
    
    context = {
        'page_title': 'Contact Me - Simon Macharia'
    }
    return render(request, 'pofolio/contact.html', context)


# ========================================
# SEARCH VIEW (Global)
# ========================================
def search(request):
    """Global search across projects, blog, and services"""
    query = request.GET.get('q', '')
    
    if not query:
        return redirect('home')
    
    # Search projects
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(technologies__icontains=query)
    )[:5]
    
    # Search blog posts
    posts = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__icontains=query),
        status='published'
    )[:5]
    
    # Search services
    services_list = Service.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query),
        active=True
    )[:5]
    
    context = {
        'query': query,
        'projects': projects,
        'posts': posts,
        'services': services_list,
        'total_results': projects.count() + posts.count() + services_list.count(),
        'page_title': f'Search: {query}'
    }
    return render(request, 'pofolio/search.html', context)