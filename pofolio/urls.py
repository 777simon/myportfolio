from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # About
    path('about/', views.about, name='about'),
    
    # Projects
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Blog
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Services
    path('services/', views.services, name='services'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Search
    path('search/', views.search, name='search'),
]