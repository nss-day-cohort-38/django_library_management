import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, Librarian


def get_book(book_id):
    return Book.objects.get(pk=book_id)


@login_required
def book_details(request, book_id):
    book = get_book(book_id)
    if request.method == 'GET':

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

            book.delete()

            return redirect(reverse('libraryapp:books'))

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):

            book.title = form_data['title']
            book.author = form_data['author']
            book.isbn = form_data['isbn']
            book.year_published = form_data['year_published']
            book.publisher = form_data['publisher']
            book.location_id = form_data['location']

            book.save()

            return redirect(reverse('libraryapp:book', args=[book.id]))
