from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    available_copies = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="purchases_book"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases_user"
    )
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.book.title}"
