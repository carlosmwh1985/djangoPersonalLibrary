from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Author, Editorial, Book

class IndexView(generic.ListView):
    template_name = 'library/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """Return..."""
        return Book.objects.order_by('libro_id')


class DetailView(generic.DetailView):
    template_name: str = 'library/detail.html'
    model = Book

