from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ========================================
# PROJECT MODEL
# ========================================
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App'),
        ('desktop', 'Desktop Application'),
        ('data', 'Data Science'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    
    # Tech Stack
    technologies = models.CharField(max_length=500, help_text="Comma-separated: Python, Django, PostgreSQL")
    
    # Links
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    demo_video = models.URLField(blank=True, null=True)
    
    # Images
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    image1 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image2 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image3 = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    # Metadata
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['-featured', 'order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.title
    
    def get_tech_list(self):
        """Returns technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',')]


# ========================================
# BLOG POST MODEL
# ========================================
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    # Content
    excerpt = models.TextField(max_length=300, help_text="Short preview")
    content = models.TextField()
    
    # Images
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # Categories
    category = models.CharField(max_length=100, default='Tutorial')
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    read_time = models.IntegerField(default=5, help_text="Read time in minutes")
    views = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Returns tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])


# ========================================
# SERVICE MODEL
# ========================================
class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    
    # Pricing
    price_range = models.CharField(max_length=100, help_text="e.g., $500 - $2000")
    pricing_type = models.CharField(max_length=50, default="Per Project")
    
    # Features (JSON or comma-separated)
    features = models.TextField(help_text="One feature per line")
    
    # Icon/Image
    icon_class = models.CharField(max_length=100, blank=True, help_text="Font Awesome class")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # Metadata
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_features_list(self):
        """Returns features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]


# ========================================
# CONTACT MESSAGE MODEL
# ========================================
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'new':
            self.status = 'read'
            self.read_at = timezone.now()
            self.save()


# ========================================
# TESTIMONIAL MODEL
# ========================================
class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    
    testimonial = models.TextField()
    rating = models.IntegerField(default=5, help_text="1-5 stars")
    
    # Project reference
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Metadata
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-featured', '-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


# ========================================
# SKILL MODEL
# ========================================
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('database', 'Database'),
        ('tool', 'Tool/Software'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(default=50, help_text="0-100%")
    
    # Icon
    icon_class = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='skills/', blank=True, null=True)
    
    # Display
    show_on_home = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"