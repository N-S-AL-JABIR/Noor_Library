from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserUpdateForm
from django.views.generic import FormView
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class UserRegistrationView(FormView):
    template_name = "accounts/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = "accounts/login.html"
    title = "Login"

    def get_success_url(self):
        return reverse_lazy("profile")


def LogoutView(request):
    logout(request)
    return redirect("login")


class UserProfileView(View):
    template_name = "accounts/profile.html"
    title = "Profile"
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, self.template_name, {"user": request.user})

class UserUpdateView(View):
    template_name = "accounts/update_profile.html"
    title = "Update Profile"
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})
