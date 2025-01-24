import time
from random import randint, choice


from celery import shared_task
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet

from books.filters import AuthorAdsSettingsFilterSet
from books.models import Book, Author, AuthorAdsSettings
from django.core.serializers import serialize

from books.serializers import AuthorAdsSettingsSerializer
from bookstore.telegram_bot import send_message_to_bot


def book_list(request):
    books = Book.objects.filter(status=1)
    return render(request, 'books/book_list.html', context={'books': [book.to_dict() for book in books]})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'books/book_detail.html', context={'book': book.to_dict()})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/author_list.html', context={'authors': [author.to_dict() for author in authors]})


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)

    clicked.delay(2)

    return render(request, 'books/author_detail.html', context={'author': author.to_dict()})


@shared_task
def clicked(x: int):
    time.sleep(15)
    rand_base = randint(0, 1)
    if rand_base == 0:
        base = Author.objects.all()
    else:
        base = Book.objects.all()
    rand_object = choice(base)
    send_message_to_bot(instance=f'BOOKSTORE {x} - {rand_object}')


class APIAuthorAdsSettingViewSet(ModelViewSet):
    queryset = AuthorAdsSettings.objects.all()
    serializer_class = AuthorAdsSettingsSerializer
    filterset_class = AuthorAdsSettingsFilterSet
    search_fields = ('url', )
    ordering_fields = '__all__'

