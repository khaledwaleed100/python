from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# ==========================================
# SHARED MODELS
# ==========================================
class Category(models.Model):
    # Minimum 2 characters validation
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.name


# ==========================================
# BOOKSTORE MODELS (Lab 3)
# ==========================================
class Book(models.Model):
    # Title length between 10 and 50 characters
    title = models.CharField(max_length=50, validators=[MinLengthValidator(10)])
    desc = models.TextField()
    rate = models.DecimalField(max_digits=3, decimal_places=1)
    views = models.IntegerField(default=0)
    
    # Each book must be related to an existing user (Many-to-One)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    
    # Each book must be related to one or more category (Many-to-Many)
    categories = models.ManyToManyField(Category, related_name='books')

    def __str__(self):
        return self.title

class ISBN(models.Model):
    # Each book has only one ISBN, each ISBN belongs to one book
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='isbn')
    
    # Author title, book title, and auto-generated ISBN number
    author_title = models.CharField(max_length=100, blank=True, null=True)
    book_title = models.CharField(max_length=100, blank=True, null=True)
    isbn_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.isbn_number)

# Build a signal to create ISBN object and assign it to the created book
@receiver(post_save, sender=Book)
def create_isbn_for_book(sender, instance, created, **kwargs):
    if created:
        ISBN.objects.create(
            book=instance,
            book_title=instance.title
        )


# ==========================================
# MOVIE & SERIES API MODELS (Lab 4)
# ==========================================
class Cast(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Abstract Base Class for shared information
class MediaInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    
    # We are reusing the Category model from the top of the file!
    categories = models.ManyToManyField(Category, related_name="%(class)s_categories")
    casts = models.ManyToManyField(Cast, related_name="%(class)s_casts")
    poster_image = models.ImageField(upload_to='posters/', null=True, blank=True)

    class Meta:
        abstract = True # This tells Django NOT to create a table for MediaInfo

class Movie(MediaInfo):
    pass # Inherits everything from MediaInfo

class Series(MediaInfo):
    pass # Inherits everything from MediaInfo