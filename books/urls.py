from django.urls import path
from . import views

app_name = 'books' # Good practice to namespace your urls

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/new/', views.book_create, name='book_create'),
    
    # Updated lines below: changed pk to book_id and updated view names
    path('book/<int:book_id>/', views.book_detail, name='book_detail'), 
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
]