from urllib import response
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Editorial


def create_author(name='Test', family_name='Testing'):
    return Author.objects.create(
        nombre=name,
        apellido=family_name
    )

def create_editorial(name='Editor_Testing GmbH'):
    return Editorial.objects.create(
        nombre=name
    )

def create_book(cat_id='XXX', title='My Test Book', pags=666):
    author = create_author()
    editor = create_editorial()
    return Book.objects.create(
        libro_id=cat_id,
        titulo=title,
        autor=author,
        editorial=editor,
        pags=pags
    )

def create_book_by(author, cat_id='XXX', title='My Test Book', pags=666):
    editor = create_editorial()
    return Book.objects.create(
        libro_id=cat_id,
        titulo=title,
        autor=author,
        editorial=editor,
        pags=pags
    )


class BookDetailViewTests(TestCase):

    def test_book_view(self):
        """
        The detail view of a book should content the most important fields of a Book: title, author, Catalog Id...
        """
        book = create_book()
        url = reverse('library:book_detail', args=(book.id,))
        response = self.client.get(url)
        self.assertContains(response, book.titulo)
        self.assertContains(response, book.autor)
        self.assertContains(response, book.libro_id)

    def test_no_book_view(self):
        """
        There is no book in the DB, with the give ID
        """
        url = reverse('library:book_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AuthorDetailViewTests(TestCase):

    def test_author_view(self):
        """
        The detail view of an author should content at leats his/her name and family name
        """
        author = create_author()
        url = reverse('library:author_detail', args=(author.id,))
        response = self.client.get(url)
        self.assertContains(response, author.nombre)
        self.assertContains(response, author.apellido)

    def test_no_author_view(self):
        """
        There is no author in the DB, with the given ID
        """
        url = reverse('library:author_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # def test_get_all_books_by_author(self):
    #     """
    #     One should have all the books writen by a given author, when visiting
    #     the Author Detail View
    #     """
    #     author1 = create_author(name='Test1', family_name='Test1')
    #     author2 = create_author(name='Test2', family_name='Test2')
    #     books_by_1 = []
    #     books_by_2 = []
    #     for i in range(3):
    #         books_by_1.append(create_book_by(author1, cat_id='XXX_T1{}'.format(i+1)))
    #     for i in range(2):
    #         books_by_2.append(create_book_by(author2, cat_id='XXX_T2{}'.format(i+1)))
        
    #     url = reverse('library:author_detail', args=(author1.id,))
    #     response = self.client.get(url)
    #     print(books_by_1)
    #     self.assertQuerysetEqual(response.context['books'], books_by_1)


class BookListViewTests(TestCase):

    def test_no_books(self):
        """
        If no books exists, it should return a message
        """
        response = self.client.get(reverse('library:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No book list available/found')
        self.assertQuerysetEqual(response.context['book_list'], [])
    
    def list_with_one_book(self):
        """
        Test the book index view, with one book
        """
        book = create_book()
        response = self.client.get('library:book_list')
        self.assertQuerysetEqual(
            response.context['book_list'],
            [book]
        )


class AuthorListViewTests(TestCase):

    def test_no_authors(self):
        """
        If there are no authors, it should return a message
        """
        response = self.client.get(reverse('library:author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No author list available/found')
        self.assertQuerysetEqual(response.context['author_list'], [])
    
    def list_with_one_author(self):
        """
        Test the author list view, with one author
        """
        author = create_author()
        response = self.client.get('library:author_list')
        self.assertQuerysetEqual(
            response.context['author_list'],
            [author]
        )

