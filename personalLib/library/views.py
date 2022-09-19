from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author, DeweySystem, Publisher, Book


class HomeView(LoginRequiredMixin, generic.base.TemplateView):
    """View class for the home page"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.all().count()
        context['total_authors'] = Author.objects.all().count()
        return 
    

class BookListView(LoginRequiredMixin, generic.ListView):
    """View class for the list of all books"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """Return all books, ordered by Catalog Id"""
        return Book.objects.order_by('libro_id')


class AuthorListView(LoginRequiredMixin, generic.ListView):
    """View class for the list of all authors"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        """Return all authors, ordered ba Family Name"""
        return Author.objects.order_by('apellido')
    

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the detailed view of a particular book"""
    
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    template_name = 'library/book_detail.html'
    model = Book


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the detailed view of a particular author"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/author_detail.html'
    model = Author

    def get_context_data(self, **kwargs):
        """Add to the context all books associated with this Author"""
        context = super().get_context_data(**kwargs)
        context['books_by'] = Book.objects.filter(autor=self.get_object())
        return context


class CatalogSystemView(LoginRequiredMixin, generic.ListView):
    """View class for the whole Dewey-Catalog system, used to catalog the whole library.\n
    Use it only as a reference"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/dewey_system.html'
    context_object_name = 'determinants'

    def get_queryset(self):
        """Return all the Ids and Subjects of the catalog (Dewey System)"""
        return DeweySystem.objects.order_by('id')
