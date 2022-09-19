import unidecode

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author, Publisher, Book
from .models import DeweySystem, CatalogCodes
from .models import AuthorNameCodes, HistoryCodes, LanguageCodes, LiteratureCodes, LiteratureInSpanish


class HomeView(LoginRequiredMixin, generic.base.TemplateView):
    """View class for the home page"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.all().count()
        context['total_authors'] = Author.objects.all().count()
        return context
    

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
        context['name_code'] = self.get_name_code()
        return context

    def get_name_code(self):
        text = unidecode.unidecode(getattr(self.get_object(), 'apellido'))
        if len(text) < 3:
            return text[0]
        num_1 = getattr(
            AuthorNameCodes.objects.filter(letras__contains=text[1].lower()).first(),
            'numero'
        )
        num_2 = getattr(
            AuthorNameCodes.objects.filter(letras__contains=text[2].lower()).first(),
            'numero'
        )
        return '{}{}{}'.format(text[0], num_1, num_2)


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


class DeterminantsView(LoginRequiredMixin, generic.ListView):
    """View class for the different determinants (Form, Language, History, Author Name),
    used to catalog the whole library.\n
    Use it only as a reference"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'library/catalog_codes.html'
    context_object_name = 'determinants'

    def get_queryset(self):
        """Return all the Ids and Subjects of the catalog (Dewey System)"""
        return CatalogCodes.objects.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['det_language'] = LanguageCodes.objects.all().order_by('num')
        context['det_history'] = HistoryCodes.objects.all().order_by('num')
        context['det_literature'] = LiteratureCodes.objects.all().order_by('num')
        context['det_spanish_lit'] = LiteratureInSpanish.objects.all().order_by('id')
        context['det_author_name'] = AuthorNameCodes.objects.all().order_by('numero')
        return context

