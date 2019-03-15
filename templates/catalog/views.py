from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
import datetime

from .forms import RenewBookForm
from .models import *


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_filter = Book.objects.filter(title__icontains = 'lord').count()
    return render(request, 'index.html', context = {'num_books':num_books, 'num_instances' : num_instances, 'num_instances_available' : num_instances_available, 'num_authors' : num_authors, 'num_genres' : num_genres, 'num_books_filter':num_books_filter, 'num_visits': num_visits})

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class BookListView(ListView):
    model = Book
    template_name = 'books_list.html'
    paginate_by = 10
#    def get_queryset(self):
#        return Book.objects.filter(title__icontains='of')[:5] #5 books with 'of' in title

#    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
#        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и иниуиализируем ее некоторым значением
#        context['some_data'] = 'This is just some data'
#        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(ListView):
    model = Author
    template_name = 'authors_list.html'
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(author__pk=self.kwargs.get('pk'))
        context['books_instances_available'] = Book.objects.filter(author__pk=self.kwargs.get('pk'))
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrowed=self.request.user).filter(status__exact='o').order_by('due_back')

class BooksOnLoanListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'books_on_loan_list.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'2019-02-27',}
    template_name = 'author_form.html'
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    template_name = 'author_form.html'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'
    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'
