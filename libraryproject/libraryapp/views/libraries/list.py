import sqlite3
from django.shortcuts import render
from libraryapp.models import Library, Book
from django.contrib.auth.decorators import login_required


@login_required
def library_list(request):
    libraries = Library.objects.all()
    
    for library in libraries:
        library.books = Book.objects.filter(location_id = library.id)

    template_name = 'libraries/list.html'

    context = {
        'libraries': libraries
    }

    return render(request, template_name, context)
