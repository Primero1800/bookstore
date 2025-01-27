from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from books.filters import AuthorAdsSettingsFilterSet
from books.models import Book, Author, AuthorAdsSettings
from django.core.serializers import serialize

from books.serializers import AuthorAdsSettingsSerializer
from books.service import create_author_ads_settings
from books.tasks import clicked


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

    #clicked.delay(2)

    return render(request, 'books/author_detail.html', context={'author': author.to_dict()})



class APIAuthorAdsSettingViewSet(ModelViewSet):
    queryset = AuthorAdsSettings.objects.all()
    serializer_class = AuthorAdsSettingsSerializer
    filterset_class = AuthorAdsSettingsFilterSet
    search_fields = ('url', )
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        settings = create_author_ads_settings(serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response(AuthorAdsSettingsSerializer(settings).data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_destroy(self, instance):
        try:
            instance.crontab.delete()
        except AttributeError:
            pass
        instance.delete()

