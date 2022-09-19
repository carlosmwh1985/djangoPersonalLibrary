from django.db import models
from django.contrib import admin


class Author(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        # return '{}, {}'.format(self.apellido, self.nombre)
        return '{} {}'.format(self.nombre, self.apellido)

    class Meta:
        db_table = 'tblautores'
    
    # TODO: add a function to translate family name to the catalog ID...


class Publisher(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tbleditoriales'



class Book(models.Model):
    libro_id = models.CharField(max_length=20)
    titulo = models.TextField()
    autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pags = models.IntegerField(default=0)
    isbn = models.CharField(max_length=21)
    ejemplares = models.IntegerField(default=1)
    leido = models.BooleanField(default=False)
    observaciones = models.TextField()

    def get_author_id(self):
        return int(self.autor.id)

    def book_read_icon(self):
        """Function to help to recognise the `read` field as a Python Boolean"""
        if self.leido:
            return "fa-solid fa-circle-check true"
        else:
            return "fa-solid fa-circle-xmark false"

    def __str__(self):
        return '{}, \"{}\", by {}'.format(self.libro_id, self.titulo, self.autor.nombre)

    class Meta:
        db_table = 'tbllibros'

