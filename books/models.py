from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Category(models.Model):
    # Minimum 2 characters validation [cite: 470]
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.name

class Book(models.Model):
    # Title length between 10 and 50 characters [cite: 469]
    title = models.CharField(max_length=50, validators=[MinLengthValidator(10)])
    desc = models.TextField()
    rate = models.DecimalField(max_digits=3, decimal_places=1)
    views = models.IntegerField(default=0)
    
    # Each book must be related to an existing user (Many-to-One) [cite: 462]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    
    # Each book must be related to one or more category (Many-to-Many) [cite: 463]
    categories = models.ManyToManyField(Category, related_name='books')

    def __str__(self):
        return self.title

class ISBN(models.Model):
    # Each book has only one ISBN, each ISBN belongs to one book [cite: 464]
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='isbn')
    
    # Author title, book title, and auto-generated ISBN number [cite: 465]
    author_title = models.CharField(max_length=100, blank=True, null=True)
    book_title = models.CharField(max_length=100, blank=True, null=True)
    isbn_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.isbn_number)

# --- BONUS: Signal to auto-create ISBN --- #
# Build a signal to create ISBN object and assign it to the created book [cite: 475]
@receiver(post_save, sender=Book)
def create_isbn_for_book(sender, instance, created, **kwargs):
    if created:
        ISBN.objects.create(
            book=instance,
            book_title=instance.title
        )