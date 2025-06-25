from django import forms
from django.contrib.auth.models import User
from .models import UserAccount
from .constants import GENDER_CHOICES
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "id": "required"}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "id": "required"}),
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "@username", "id": "required"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "example@example.com", "id": "required"}
        )
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    address = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Street,City,Country", "rows": 3}),
        required=False,
        max_length=255,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "gender",
            "date_of_birth",
            "address",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            gender = self.cleaned_data.get("gender")
            date_of_birth = self.cleaned_data.get("date_of_birth")
            address = self.cleaned_data.get("address")
            UserAccount.objects.create(
                user=user,
                gender=gender,
                date_of_birth=date_of_birth,
                address=address,
            )
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "id": "required"}),
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Username", "id": "required"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "id": "required"})
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    address = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Street,City,Country", "rows": 3}),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "gender",
            "date_of_birth",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
            except user_account.DoesNotExist:
                user_account = None
            if user_account:
                self.fields["first_name"].initial = user_account.user.first_name
                self.fields["last_name"].initial = user_account.user.last_name
                self.fields["username"].initial = user_account.user.username
                self.fields["email"].initial = user_account.user.email
                self.fields["gender"].initial = user_account.gender
                self.fields["date_of_birth"].initial = user_account.date_of_birth
                self.fields["address"].initial = user_account.address

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.gender = self.cleaned_data.get("gender")
            user_account.date_of_birth = self.cleaned_data.get("date_of_birth")
            user_account.address = self.cleaned_data.get("address")
            user_account.save()
        return user


class DepositMoneyForm(forms.Form):
    balance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"placeholder": "Enter amount to deposit", "id": "required"}
        ),
    )

    class Meta:
        fields = ["balance"]
    def clean_balance(self):
        balance = self.cleaned_data.get("balance")
        if balance <= 0:
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return balance