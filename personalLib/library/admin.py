from django.contrib import admin

from .models import Author, Publisher, Book


class AuthorAdmin(admin.ModelAdmin):
    fields = ['nombre', 'apellido', 'nacionalidad']
    list_display = ('id', 'nombre', 'apellido', 'nacionalidad')
    list_filter = ['nacionalidad']
    search_fields = ['nombre', 'apellido']


class BookAdmin(admin.ModelAdmin):
    fields = ['libro_id', 'autor', 'editorial', 'isbn', 'leido']
    # fieldsets = [
    #     ('Ids', {'fields': ['id', 'libro_id', 'autor_id', 'editorial_id']}),
    #     ('Book Info', {'fields': ['titulo', 'pags', 'isbn', 'ejemplares']}),
    #     ('Others', {'fields': ['leido', 'observaciones']})
    # ]
    list_display = ('id', 'libro_id', 'titulo', 'isbn', 'leido')
    list_filter = ('autor', 'editorial', 'leido')
    search_fields = ['titulo', 'autor_id', 'editorial_id']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
