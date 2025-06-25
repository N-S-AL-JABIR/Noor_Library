from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, CategoryForm, ReviewBookForm
from .models import Book, Category, Purchase,ReviewBook
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from Accounts.models import UserAccount
from django.contrib import messages


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "book/book_form.html"
    success_url = reverse_lazy("home")


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "book/category_form.html"
    success_url = reverse_lazy("home")


class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.all().order_by("title")


class BuyBookView(LoginRequiredMixin, CreateView):
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        user = request.user
        print(book.title)

        if book.available_copies > 0:
            Purchase.objects.create(user=user, book=book)
            book.available_copies -= 1
            book.save()
            return redirect("home")
        else:
            return render(
                request, "book/book_list.html", {"error": "No copies available"}
            )

class BookDetailView(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user = request.user
        review_form = ReviewBookForm(self.request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = user
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect("book_detail", id=book.id)
        # If form is invalid, supply all context including reviews
        reviews = ReviewBook.objects.filter(book=book)
        return render(
            request,
            "book/book_detail.html",
            {
                "book": book,
                "form": review_form,
                "reviews": reviews,
            }
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['book'] = book
        context['reviews'] = ReviewBook.objects.filter(book=book)
        context['form'] = ReviewBookForm()
        return context