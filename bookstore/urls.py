from django.contrib import admin
from django.urls import path, include
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    
    # Add built-in auth URLs and your custom register view
    path('', include('django.contrib.auth.urls')), 
    path('register/', book_views.register, name='register'),
]