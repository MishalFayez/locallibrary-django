from django.db.models import Count
from django.shortcuts import render

from .models import Author, Book, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    tasy_genre = Genre.objects.filter(name__contains='tasy')
    num_tasy_genre = tasy_genre.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_tasy_genre':num_tasy_genre,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    template_name = 'books/book_list.html'  # Specify your own template name/location
    paginate_by = 2


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

from django.shortcuts import get_object_or_404


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'   # your own name for the list as a template variable
    template_name = 'books/book_detail.html'  # Specify your own template name/location


    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'books/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'   # your own name for the list as a template variable
    template_name = 'authors/author_list.html'  # Specify your own template name/location
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author'   # your own name for the list as a template variable
    template_name = 'authors/author_detail.html'  # Specify your own template name/location

    # def get_context_data(self, **kwargs):
    #     num_instance = Author.objects.annotate(Count('book')).count()
    #     context = super().get_context_data(**kwargs)
    #     context['hello'] = num_instance
    #     return context



    # def author_detail_view(request, primary_key):
    #     author = get_object_or_404(Author, pk=primary_key)
    #     num_instance = Author.objects.annotate(Count('bookinstance'))
    #     context = {
    #         'author': author,
    #         'num_instance': num_instance,
    #         'hello': 'hello world'
    #     }
    #     return render(request, 'authors/author_detail.html', context=context)
