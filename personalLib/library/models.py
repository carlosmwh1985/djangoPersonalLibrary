from django.db import models


class Author(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.apellido, self.nombre)

    class Meta:
        db_table = 'tblautores'


class Editorial(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tbleditoriales'



class Book(models.Model):
    libro_id = models.CharField(max_length=20)
    titulo = models.TextField()
    autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    pags = models.IntegerField(default=0)
    isbn = models.CharField(max_length=21)
    ejemplares = models.IntegerField(default=1)
    leido = models.BooleanField(default=False)
    observaciones = models.TextField()

    def __str__(self):
        return '{}, \"{}\", by {}'.format(self.libro_id, self.titulo, self.autor.nombre)

    class Meta:
        db_table = 'tbllibros'

