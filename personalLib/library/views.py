from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author, Editorial, Book


# TODO: add user to perform the tests!



class HomeView(LoginRequiredMixin, generic.base.TemplateView):
    """View class for the home page"""

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.all().count()
        context['num_authors'] = Author.objects.all().count()
        # context['num_visits'] = request.session['num_visits']
        return 
    

class BookListView(LoginRequiredMixin, generic.ListView):
    """View class for the list of all books"""

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """Return all books, ordered by Catalog Id"""
        return Book.objects.order_by('libro_id')


class AuthorListView(LoginRequiredMixin, generic.ListView):
    """View class for the list of all authors"""

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        """Return all authors, ordered ba Family Name"""
        return Author.objects.order_by('apellido')
    

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the detailed view of a particular book"""
    
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    
    template_name = 'library/book_detail.html'
    model = Book


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the detailed view of a particular author"""

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/author_detail.html'
    model = Author

    def get_context_data(self, **kwargs):
        """Add to the context all books associated with this Author"""
        context = super().get_context_data(**kwargs)
        context['books_by'] = Book.objects.filter(autor=self.get_object())
        return context