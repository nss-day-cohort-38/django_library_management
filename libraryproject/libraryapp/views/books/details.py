import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, Librarian


def get_book(book_id):
    return Book.objects.get(pk=book_id)


@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)

        template = 'books/details.html'
        context = {
            'book': book
        }

        return render(request, template, context)

    if request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for deleting a book
        #
        # Note: You can use parenthesis to break up complex
        #       `if` statements for higher readability
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            book_to_delete = get_book(book_id)
            book_to_delete.delete()

            return redirect(reverse('libraryapp:books'))

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            book_to_update = get_book(book_id)

            book_to_update.title = form_data['title']
            book_to_update.author = form_data['author']
            book_to_update.isbn = form_data['isbn']
            book_to_update.year = form_data['year_published']
            book_to_update.location_id = form_data['location']

            book_to_update.save()

            return redirect(reverse('libraryapp:books'))
