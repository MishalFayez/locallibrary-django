from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
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

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksAllUsersListView(LoginRequiredMixin,generic.ListView, PermissionRequiredMixin):
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed_all_users.html'
    paginate_by = 3
    permission_required = 'catalog.can_mark_returned'


    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'books/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    template_name = 'authors/author_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    template_name = 'authors/author_form.html'
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    template_name = 'authors/author_confirm_delete.html'
    model = Author
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    template_name = 'books/book_form.html'
    fields = "__all__"

class BookUpdate(UpdateView):
    template_name = 'books/book_form.html'
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(DeleteView):
    template_name = 'books/book_confirm_delete.html'
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')