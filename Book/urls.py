from django.urls import path
from .views import (
    AddBookView,
    AddCategoryView,
    BookListView,
    BuyBookView,
    BookDetailView,
    ReturnBookView,
    delete_review,
)

urlpatterns = [
    path("add-book/", AddBookView.as_view(), name="add_book"),
    path("add-category/", AddCategoryView.as_view(), name="add_category"),
    path("all-books/", BookListView, name="all_books"),
    path("categories/<slug:cat_slug>/", BookListView, name="book_list"),
    path("buy-book/<int:id>/", BuyBookView.as_view(), name="buy_book"),
    path("book-details/<int:id>/", BookDetailView.as_view(), name="book_detail"),
    path("return-book/<int:id>/", ReturnBookView.as_view(), name="return_book"),
    path("delete-review/<int:review_id>/", delete_review, name="delete_review"),
]
