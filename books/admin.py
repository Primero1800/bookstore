from django.contrib import admin
from books.models import Book, Author, AuthorAdsSettings


class BookInline(admin.StackedInline):
    model = Book.authors.through


class AuthorInline(admin.StackedInline):
    model = Author.books.through

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'slug', 'born', 'died')
    list_display_links = ('name', 'surname', )
    search_fields = ('name', 'surname',)
    prepopulated_fields = {'slug': ('name', 'surname',)}
    inlines = [BookInline]
    list_per_page = 30


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'year')
    list_display_links = ('title', 'slug', )
    search_fields = ('title', 'authors',)
    prepopulated_fields = {'slug': ('title', 'authors',)}
    #inlines = [BookInline]
    list_per_page = 30


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

admin.site.register(AuthorAdsSettings)
