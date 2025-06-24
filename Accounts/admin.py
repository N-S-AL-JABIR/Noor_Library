from django.contrib import admin
from .models import UserAccount, LibraryProfile

admin.site.register(
    [
        UserAccount,
        LibraryProfile,
    ]
)
