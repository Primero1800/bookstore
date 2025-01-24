from django.urls import path

from books.views import book_list, book_detail, author_list, author_detail

app_name = 'books'

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/<slug>/', book_detail, name='book_detail'),
    path('authors/', author_list, name='author_list'),
    path('authors/<slug>/', author_detail, name='author_detail')
]