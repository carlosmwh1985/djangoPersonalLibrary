from django.db import models


class TblAutores(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=100)


class TblEditoriales(models.Model):
    nombre = models.CharField(max_length=255)


class TblLibros(models.Model):
    libro_id = models.CharField(max_length=20)
    titulo = models.TextField()
    autor_id = models.ForeignKey(TblAutores, on_delete=models.CASCADE)
    editorial_id = models.ForeignKey(TblEditoriales, on_delete=models.CASCADE)
    pags = models.IntegerField(default=0)
    isbn = models.CharField(max_length=21)
    ejemplares = models.IntegerField(default=1)
    leido = models.BooleanField(default=False)
    observaciones = models.TextField()

