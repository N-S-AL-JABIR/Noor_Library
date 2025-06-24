from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_CHOICES

class LibraryProfile(models.Model):
    total_users = models.IntegerField(default=0)
    total_books = models.IntegerField(default=0)
    total_borrowed_books = models.IntegerField(default=0)
    total_categories = models.IntegerField(default=0)

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(
            f"{self.user.first_name} {self.user.last_name} - {self.user.username}"
        )
