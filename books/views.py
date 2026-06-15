from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

def book_list(request):
       books = Book.objects.all() # Retrieve all records[cite: 3]
       return render(request, 'books/book_list.html', {'books': books})

def book_create(request):
       if request.method == 'POST':
           form = BookForm(request.POST) # Form sent from the user[cite: 3]
           if form.is_valid():
               form.save()
               return redirect('book_list')
       else:
           form = BookForm()
       return render(request, 'books/book_form.html', {'form': form})

def book_edit(request, book_id):
       book = get_object_or_404(Book, pk=book_id)
       if request.method == 'POST':
           form = BookForm(data=request.POST, instance=book) # Pass the instance to update[cite: 3]
           if form.is_valid():
               form.save()
               return redirect('book_list')
       else:
           form = BookForm(instance=book)
       return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, book_id):
       book = get_object_or_404(Book, pk=book_id)
       if request.method == 'POST':
           book.delete() # Delete the record[cite: 3]
           return redirect('book_list')
       return render(request, 'books/book_confirm_delete.html', {'book': book})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})