from django.shortcuts import render,redirect,get_object_or_404
from .forms import BookForm, CategoryForm
from .models import Book, Category, Purchase
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('home')

class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'book/category_form.html'
    success_url = reverse_lazy('home')

class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().order_by('title')

class BuyBookView(CreateView):
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        user = request.user
        print(book.title)

        if book.available_copies > 0:
            Purchase.objects.create(user=user, book=book)
            book.available_copies -= 1
            book.save()
            return redirect('home')
        else:
            return render(request, 'book/book_list.html', {'error': 'No copies available'})
