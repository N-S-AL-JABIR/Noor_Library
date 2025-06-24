from django.shortcuts import render
from django.views import View
from Book.models import Book, Category


class HomeView(View):
    def get(self, request, cat_slug=None):
        books = Book.objects.all().order_by("title")
        if cat_slug:
            books = books.filter(category__slug=cat_slug)
        categories = Category.objects.all()
        return render(
            request, "index.html", {"books": books, "categories": categories}
        )
