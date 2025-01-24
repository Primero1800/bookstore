from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import book_list, book_detail, author_list, author_detail, APIAuthorAdsSettingViewSet

app_name = 'books'

router = DefaultRouter()

router.register('ads', APIAuthorAdsSettingViewSet)

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('books/<slug>/', book_detail, name='book_detail'),
    path('authors/', author_list, name='author_list'),
    path('authors/<slug>/', author_detail, name='author_detail'),

    path(f'api/', include(router.urls)),
    path('api/', router.APIRootView.as_view(), name='root')
]