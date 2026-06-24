from django.contrib import admin
from .models import Book, Category, ISBN

# Provide a usage for the admin stacked model [cite: 467]
class ISBNInline(admin.StackedInline):
    model = ISBN
    extra = 0 # Prevents empty blank forms from showing

# Allow the admin panel to display and filter books [cite: 466]
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'rate', 'views')
    list_filter = ('categories', 'user', 'rate')
    inlines = [ISBNInline]

admin.site.register(Category)