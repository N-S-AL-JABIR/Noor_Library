from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, CategoryForm, ReviewBookForm
from .models import Book, Category, Purchase, ReviewBook
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from Accounts.models import UserAccount
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse
from Accounts.views import send_user_email



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


def BookListView(request, cat_slug=None):
    books = Book.objects.all()
    if cat_slug is not None:
        category = Category.objects.get(slug=cat_slug)
        books = Book.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, "book/book_list.html", {"books": books, "categories": categories})


class BuyBookView(LoginRequiredMixin, CreateView):
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        user = request.user
        print(book.title)
        has_purchased = Purchase.objects.filter(user=user, book=book).first()
        if has_purchased:
            messages.error(request, "You have already purchased this book.")
            return render(request, "book/book_detail.html")
        if book.available_copies == 0:
            messages.error(request, "No copies available.")
            return render(request, "book/book_detail.html")
        if user.account.balance >= book.price and book.available_copies > 0:
            Purchase.objects.create(user=user, book=book)
            book.available_copies -= 1
            user.account.balance -= book.price
            user.account.save()
            book.save()
            messages.success(request, "Book purchased successfully!")
            send_user_email(
                subject="Purchase Successful",
                action="purchase",
                book_title=book.title,
                user=user,
                balance=user.account.balance,
                amount=book.price,
            )
            return redirect("book_detail", id=book.id)
        else:
            return render(request, "book/book_detail.html")


class ReturnBookView(LoginRequiredMixin, CreateView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        user = request.user
        purchase = Purchase.objects.filter(user=user, book=book).first()

        if purchase:
            purchase.delete()
            book.available_copies += 1
            user.account.balance += book.price
            user.account.save()
            book.save()
            messages.success(request, "Book returned successfully!")
            send_user_email(
                subject="Return Successful",
                action="return",
                book_title=book.title,
                user=user,
                balance=user.account.balance,
                amount=book.price,
            )
        else:
            messages.error(request, "You have not purchased this book.")

        return redirect("profile")


class BookDetailView(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user
        context["reviews"] = self.object.reviews.all()
        context["form"] = ReviewBookForm()
        if user.is_authenticated:
            has_purchased = Purchase.objects.filter(user=user, book=book).exists()
            has_reviewed = ReviewBook.objects.filter(user=user, book=book).exists()
            context["can_review"] = has_purchased and not has_reviewed
            context["has_reviewed"] = has_reviewed
            if has_purchased:
                context["purchased"] = True
            else:
                context["purchased"] = False
        else:
            context["can_review"] = False
            context["has_reviewed"] = False
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user = request.user
        form = ReviewBookForm(request.POST)
        has_purchased = Purchase.objects.filter(user=user, book=book).exists()
        has_reviewed = ReviewBook.objects.filter(user=user, book=book).exists()
        if has_purchased and has_reviewed:
            return self.get(request, *args, **kwargs)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = user
            review.save()
            messages.success(request, "Review added successfully!")
        return self.get(request, *args, **kwargs)


def delete_review(request, review_id):
    review = get_object_or_404(ReviewBook, id=review_id)
    if request.user == review.user:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    else:
        messages.error(request, "You can only delete your own reviews.")
    return redirect("book_detail", id=review.book.id)
