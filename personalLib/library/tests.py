from venv import create

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
        url = reverse('library:book_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)