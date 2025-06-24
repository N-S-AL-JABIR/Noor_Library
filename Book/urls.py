from django.urls import path
from .views import (
    AddBookView,
    AddCategoryView,
    BookListView,
    BuyBookView,
)

urlpatterns = [
    path("add-book/", AddBookView.as_view(), name="add_book"),
    path("add-category/", AddCategoryView.as_view(), name="add_category"),
    path("book-list/", BookListView.as_view(), name="Book_List"),
    path("buy-book/<int:id>/", BuyBookView.as_view(), name="buy_book"),
]