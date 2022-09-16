from django.urls import path

from . import views

app_name = 'library'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]