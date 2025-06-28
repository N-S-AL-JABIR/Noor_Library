from django import forms
from .models import Book , Category,ReviewBook

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
    def clean_cover_image(self):
        cover_image = self.cleaned_data.get("cover_image")
        if cover_image:
            # Validate the cover image (e.g., file size, type)
            if cover_image.size > 0.5 * 1024 * 1024:  # 0.5 MB limit
                raise forms.ValidationError("Cover image file size must be under 0.5 MB.")
            if not cover_image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Cover image must be a PNG or JPG file.")
        return cover_image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ReviewBookForm(forms.ModelForm):
    class Meta:
        model = ReviewBook
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Rate the book (1-5)'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['rating'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['comment'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['rating'].label = "Rating (1-5)"
    #     self.fields['comment'].label = "Review Comment"
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
