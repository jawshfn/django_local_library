from django.shortcuts import render
from django.db.models import Count, Q
from .models import Book, Author, BookInstance, Genre

# Create Views Here
def index(request):
    """View function for home page of site."""
    search_word = request.GET.get('search_word', '')
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Count genres
    genre_counts = Genre.objects.annotate(num_books=Count('book'))

    # Count books containing the searched word (case insensitive)
    books_with_word = Book.objects.filter(title__icontains=search_word).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genre_counts': genre_counts,
        'books_with_word': books_with_word,
        'search_word': search_word,  # Pass the search word to the template
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
      # Specify your own template name/location
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author  # Provide the template name for the author list

class AuthorDetailView(generic.DetailView):
    model = Author