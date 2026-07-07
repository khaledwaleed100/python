from django.urls import path
from . import views

app_name = 'books' # Good practice to namespace your urls

urlpatterns = [
    # Bookstore HTML Views
    path('', views.book_list, name='book_list'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'), 
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    
    # REST API Views
    path('api/movies/', views.movie_list_api, name='api-movie-list'),
    path('api/movies/<int:pk>/', views.movie_detail_api, name='api-movie-detail'),
]