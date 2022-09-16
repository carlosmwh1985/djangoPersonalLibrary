from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Author, Editorial, Book


class HomeView(generic.base.TemplateView):
    """View class for the home page"""

    template_name = 'library/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.all().count()
        context['num_authors'] = Author.objects.count()
        return context


class BookListView(generic.ListView):
    """View class for the list of all books"""
    template_name = 'library/book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """Return all books, ordered by Catalog Id"""
        return Book.objects.order_by('libro_id')


class AuthorListView(generic.ListView):
    """View class for the list of all authors"""
    template_name = 'library/author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        """Return all authors, ordered ba Family Name"""
        return Author.objects.order_by('apellido')


class BookDetailView(generic.DetailView):
    """View class for the detailed view of a particular book"""
    template_name = 'library/book_detail.html'
    model = Book


class AuthorDetailView(generic.DetailView):
    """View class for the detailed view of a particular author"""
    template_name = 'library/author_detail.html'
    model = Author