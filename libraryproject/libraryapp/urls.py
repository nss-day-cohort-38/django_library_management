from django.urls import path, include
from .views import *

app_name = "libraryapp"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('', home, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', librarian_list, name='librarians'),
    path('libraries/', library_list, name='libraries'),
    path('book/form', book_form, name='book_form'),
    path('books/<int:book_id>/', book_details, name='book'),
    path('books/<int:book_id>/form/', book_edit_form, name='book_edit_form'),
]
