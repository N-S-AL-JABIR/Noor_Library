from django import forms
from .models import Book , Category

class BookForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    cover_image = forms.ImageField(required=True)
    available_copies = forms.IntegerField(required=True, min_value=0)
    class Meta:
        model = Book
        fields = [
            
            "title",
            "author",
            "category",
            "price",
            "pages",
            "cover_image",
            "description",
            "available_copies",
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
