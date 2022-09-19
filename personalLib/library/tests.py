from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .models import Author, Book, DeweySystem, Publisher


CREDENTIALS = {
    'username': 'test_user',
    'email': 'test_user@test_email.com',
    'password': 'testuser_abc_1234',
    'path_login': '/login/'
}

def create_author(name='Test', family_name='Testing'):
    return Author.objects.create(
        nombre=name,
        apellido=family_name
    )

def create_publisher(name='Editor_Testing GmbH'):
    return Publisher.objects.create(
        nombre=name
    )

def create_book(cat_id='XXX', title='My Test Book', pags=666):
    author = create_author()
    publisher = create_publisher()
    return Book.objects.create(
        libro_id=cat_id,
        titulo=title,
        autor=author,
        editorial=publisher,
        pags=pags
    )

def create_book_by(author, cat_id='XXX', title='My Test Book', pags=666):
    publisher = create_publisher()
    return Book.objects.create(
        libro_id=cat_id,
        titulo=title,
        autor=author,
        editorial=publisher,
        pags=pags
    )

def create_user(credentials):
    return User.objects.create_user(
        username=credentials.get('username'),
        email=credentials.get('email'),
        password=credentials.get('password')
    )


class BookDetailViewTests(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.client = Client()
        self.user = create_user(CREDENTIALS)

    def test_book_view(self):
        """
        The detail view of a book should content the most important fields of a Book: title, author, Catalog Id...
        """
        self.client.login(username=self.user_name, password=self.password)
        book = create_book()
        url = reverse('library:book_detail', args=(book.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book.titulo)
        self.assertContains(response, book.autor)
        self.assertContains(response, book.libro_id)

    def test_no_book_view(self):
        """
        There is no book in the DB, with the give ID
        """
        self.client.login(username=self.user_name, password=self.password)
        url = reverse('library:book_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AuthorDetailViewTests(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.client = Client()
        self.user = create_user(CREDENTIALS)

    def test_author_view(self):
        """
        The detail view of an author should content at leats his/her name and family name
        """
        self.client.login(username=self.user_name, password=self.password)
        author = create_author()
        url = reverse('library:author_detail', args=(author.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, author.nombre)
        self.assertContains(response, author.apellido)

    def test_no_author_view(self):
        """
        There is no author in the DB, with the given ID
        """
        self.client.login(username=self.user_name, password=self.password)
        url = reverse('library:author_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_books_by_author(self):
        """
        One should have all the books writen by a given author, when visiting
        the Author Detail View
        """
        self.client.login(username=self.user_name, password=self.password)
        author1 = create_author(name='Test1', family_name='Test1')
        author2 = create_author(name='Test2', family_name='Test2')
        books_by_1 = []
        books_by_2 = []
        books_by_1.append(create_book_by(author1, cat_id='XXX_T10'))
        for i in range(3):
            books_by_2.append(create_book_by(author2, cat_id='XXX_T2{}'.format(i+1)))
        
        url = reverse('library:author_detail', args=(author1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['books_by'], books_by_1)


class BookListViewTests(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.client = Client()
        self.user = create_user(CREDENTIALS)

    def test_no_books(self):
        """
        If no books exists, it should return a message
        """
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('library:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No book list available/found')
        self.assertQuerysetEqual(response.context['book_list'], [])
    
    def test_list_with_one_book(self):
        """
        Test the book index view, with one book
        """
        self.client.login(username=self.user_name, password=self.password)
        book = create_book()
        response = self.client.get(reverse('library:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['book_list'],
            [book]
        )


class AuthorListViewTests(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.client = Client()
        self.user = create_user(CREDENTIALS)

    def test_no_authors(self):
        """
        If there are no authors, it should return a message
        """
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('library:author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No author list available/found')
        self.assertQuerysetEqual(response.context['author_list'], [])
    
    def test_list_with_one_author(self):
        """
        Test the author list view, with one author
        """
        self.client.login(username=self.user_name, password=self.password)
        author = create_author()
        response = self.client.get(reverse('library:author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['author_list'],
            [author]
        )


class LoginTest(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.path_login = CREDENTIALS.get('path_login')
        self.client = Client()
        self.user = create_user(CREDENTIALS)
        self.credentials = CREDENTIALS
        self.false_credentials = {
            'username': self.user_name,
            'password': 'xXx',
        }

    def test_login(self):
        response = self.client.post(
            self.path_login,
            self.credentials,
            follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password')
    
    def test_login_wrong_password(self):
        response = self.client.post(
            self.path_login,
            self.false_credentials,
            follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(
            response,
            'Your username and password didn\'t match. Please try again.'
        )


class CatalogViewsTests(TestCase):

    def setUp(self):
        self.user_name = CREDENTIALS.get('username')
        self.password = CREDENTIALS.get('password')
        self.email = CREDENTIALS.get('email')
        self.client = Client()
        self.user = create_user(CREDENTIALS)
    
    def test_no_dewey_catalog(self):
        """
        If there are no IDs in the catalog, it should return a message
        """
        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(reverse('library:catalog_system'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No catalog items are available')
        self.assertQuerysetEqual(response.context['determinants'], [])
    
    def test_list_with_one_catalog_item(self):
        """
        Test the Catalog System view, with one item
        """
        self.client.login(username=self.user_name, password=self.password)
        cat_item = DeweySystem.objects.create(id="XXX", nombre="Test")
        response = self.client.get(reverse('library:catalog_system'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['determinants'],
            [cat_item]
        )
