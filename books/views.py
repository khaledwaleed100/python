from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required

# DRF Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# App Imports
from .models import Book, Movie
from .forms import BookForm
from .serializers import MovieSerializer

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================
def register(request):
    """Handles new user sign-ups and logs them in automatically."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto log-in after registration
            return redirect('books:book_list') # Assuming app_name='books'
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ==========================================
# BOOKSTORE VIEWS (Lab 3)
# ==========================================
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

@login_required(login_url='/login/')
@permission_required('books.add_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user 
            book.save() 
            form.save_m2m() 
            return redirect('books:book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required(login_url='/login/')
@permission_required('books.change_book', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save() 
            return redirect('books:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required(login_url='/login/')
@permission_required('books.delete_book', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


# ==========================================
# REST API VIEWS (Lab 4)
# ==========================================
@api_view(['GET', 'POST'])
def movie_list_api(request):
    # READ ALL
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # CREATE
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_detail_api(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # READ ONE
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    # FULL UPDATE
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PARTIAL UPDATE
    elif request.method == 'PATCH':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)