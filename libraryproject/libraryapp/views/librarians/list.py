import sqlite3
from django.shortcuts import render
from libraryapp.models import Librarian
from django.contrib.auth.decorators import login_required


@login_required
def librarian_list(request):
    all_librarians = Librarian.objects.all()    

    template_name = 'librarians/list.html'

    context = {
        'all_librarians': all_librarians
    }

    return render(request, template_name, context)
