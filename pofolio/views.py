from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
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
# CONTACT VIEWS - ENHANCED
# ========================================
def contact(request):
    """Contact page with form and email notification"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validation
        if not all([name, email, subject, message]):
            messages.error(request, '❌ Please fill in all required fields.')
            return redirect('contact')
        
        # Email validation
        if '@' not in email or '.' not in email:
            messages.error(request, '❌ Please enter a valid email address.')
            return redirect('contact')
        
        try:
            # Create contact message in database
            contact_msg = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            # Send email notification to admin
            try:
                send_contact_notification(contact_msg)
            except Exception as e:
                # Log email error but don't fail the submission
                print(f"Email notification failed: {e}")
            
            # Success message with checkmark
            messages.success(
                request, 
                '✅ Thank you for your message! I will get back to you soon.'
            )
            
            return redirect('contact')
            
        except Exception as e:
            messages.error(
                request, 
                f'❌ An error occurred while sending your message. Please try again.'
            )
            print(f"Contact form error: {e}")
            return redirect('contact')
    
    context = {
        'page_title': 'Contact Me - Simon Macharia'
    }
    return render(request, 'pofolio/contact.html', context)


def send_contact_notification(contact_message):
    """Send email notification when new contact message is received"""
    
    # Your email (where you want to receive notifications)
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'simon7chris777@gmail.com')
    
    # Email subject
    subject = f'New Contact Form Message: {contact_message.subject}'
    
    # Plain text message
    plain_message = f"""
New contact form submission from your portfolio website:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone}
Subject: {contact_message.subject}

Message:
{contact_message.message}

---
Received at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Message ID: {contact_message.id}

View in admin: {settings.SITE_URL}/admin/pofolio/contactmessage/{contact_message.id}/change/
"""
    
    # HTML message (prettier version)
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
            .info-row {{ margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }}
            .label {{ font-weight: bold; color: #667eea; }}
            .message-box {{ background: white; padding: 15px; border-left: 4px solid #667eea; margin: 15px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>📩 New Contact Form Message</h2>
            </div>
            <div class="content">
                <div class="info-row">
                    <span class="label">👤 Name:</span> {contact_message.name}
                </div>
                <div class="info-row">
                    <span class="label">📧 Email:</span> <a href="mailto:{contact_message.email}">{contact_message.email}</a>
                </div>
                <div class="info-row">
                    <span class="label">📱 Phone:</span> {contact_message.phone or 'Not provided'}
                </div>
                <div class="info-row">
                    <span class="label">📝 Subject:</span> {contact_message.subject}
                </div>
                <div class="message-box">
                    <p><strong>Message:</strong></p>
                    <p>{contact_message.message}</p>
                </div>
                <div class="info-row">
                    <span class="label">🕒 Received:</span> {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}
                </div>
                <a href="{settings.SITE_URL}/admin/pofolio/contactmessage/{contact_message.id}/change/" class="btn">
                    View in Admin Panel
                </a>
            </div>
            <div class="footer">
                <p>This email was sent from your portfolio contact form</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
            reply_to=[contact_message.email]  # Allow direct reply
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        print(f"✅ Email notification sent for contact message #{contact_message.id}")
        
    except Exception as e:
        print(f"❌ Failed to send email notification: {e}")
        raise


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