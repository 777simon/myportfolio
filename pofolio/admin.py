from django.contrib import admin
from .models import Project, BlogPost, Service, ContactMessage, Testimonial, Skill

# ========================================
# PROJECT ADMIN
# ========================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'created_at']
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured']
    ordering = ['-featured', 'order', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ('Technical Details', {
            'fields': ('technologies',)
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'demo_video')
        }),
        ('Images', {
            'fields': ('thumbnail', 'image1', 'image2', 'image3')
        }),
        ('Display Options', {
            'fields': ('featured', 'order')
        }),
    )


# ========================================
# BLOG POST ADMIN
# ========================================
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'featured', 'views', 'published_at']
    list_filter = ['status', 'category', 'featured', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured']
    ordering = ['-published_at', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Tags & Categorization', {
            'fields': ('tags',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'read_time', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


# ========================================
# SERVICE ADMIN
# ========================================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_range', 'active', 'order']
    list_filter = ['active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['active', 'order']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price_range', 'pricing_type')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Visual', {
            'fields': ('icon_class', 'image')
        }),
        ('Display Options', {
            'fields': ('active', 'order')
        }),
    )


# ========================================
# CONTACT MESSAGE ADMIN
# ========================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'read_at', 'replied_at']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'read_at', 'replied_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(status='new').update(status='read')
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = 'Mark selected as replied'


# ========================================
# TESTIMONIAL ADMIN
# ========================================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'featured', 'active']
    list_filter = ['rating', 'featured', 'active']
    search_fields = ['client_name', 'client_company', 'testimonial']
    list_editable = ['featured', 'active']
    ordering = ['-featured', '-created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'rating', 'project')
        }),
        ('Display Options', {
            'fields': ('active', 'featured')
        }),
    )


# ========================================
# SKILL ADMIN
# ========================================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'show_on_home', 'order']
    list_filter = ['category', 'show_on_home']
    search_fields = ['name']
    list_editable = ['proficiency', 'show_on_home', 'order']
    ordering = ['category', 'order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'proficiency')
        }),
        ('Visual', {
            'fields': ('icon_class', 'logo')
        }),
        ('Display Options', {
            'fields': ('show_on_home', 'order')
        }),
    )