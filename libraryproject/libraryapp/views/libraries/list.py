import sqlite3
from django.shortcuts import render
from libraryapp.models import Library, Book
from django.contrib.auth.decorators import login_required


def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["library_id"]
    library.name = _row["name"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["title"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)


@login_required
def library_list(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_library
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        li.id library_id,
        li.name,
        li.address,
        b.id book_id,
        b.title,
        b.author,
        b.year_published,
        b.isbn
    FROM libraryapp_library li
    LEFT JOIN libraryapp_book b ON li.id = b.location_id
        """)

        libraries_with_books = db_cursor.fetchall()

        # Start with an empty dictionary
        library_groups = {}

        # Iterate the list of tuples
        for (library, book) in libraries_with_books:

            # If the dictionary does have a key of the current
            # library's `id` value, add the key and set the value
            # to the current library
            if library.id not in library_groups:
                library_groups[library.id] = library
                library.books.append(book)

            # If the key does exist, just append the current
            # book to the list of books for the current library
            else:
                library_groups[library.id].books.append(book)

    template_name = 'libraries/list.html'

    context = {
        'libraries': library_groups.values()
    }

    return render(request, template_name, context)
