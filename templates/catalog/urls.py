from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from .views import *


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^books/$', BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),
    re_path(r'^authors/$', AuthorListView.as_view(), name='authors'),
    re_path(r'^authors/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^mybooks/$', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^on_loan/$', BooksOnLoanListView.as_view(), name='all-borrowed'),
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', renew_book_librarian, name='renew-book-librarian' ),
    re_path(r'^author/create/$', AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
    re_path(r'^book/create/$', BookCreate.as_view(), name='book_create'),
    re_path(r'^book/(?P<pk>\d+)/update/$', BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/(?P<pk>\d+)/delete/$', BookDelete.as_view(), name='book_delete')
]
