from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm

# --- Authentication Views ---
def register(request):
    """Handles new user sign-ups and logs them in automatically."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto log-in after registration
            # Note: adjust 'book_list' if you named your urls namespace differently
            return redirect('book_list') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Public Views ---
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

# --- Protected Views (Require Login & Permissions) ---
@login_required(login_url='/login/')
@permission_required('books.add_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Pause saving to attach the logged-in user
            book = form.save(commit=False)
            book.user = request.user 
            book.save() # Now save the book to the DB
            
            # Since we used commit=False, we must manually save ManyToMany fields (categories)
            form.save_m2m() 
            
            return redirect('book_list')
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
            form.save() # User is already attached, so normal save is fine
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required(login_url='/login/')
@permission_required('books.delete_book', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})