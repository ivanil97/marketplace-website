from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterForm


class RegisterView(CreateView):
    """
    Crate new use View
    """
    form_class = RegisterForm
    template_name = "templates_users/register.html"
    success_url = reverse_lazy("user:account")
    extra_context = {'simple_header': True}

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(
            username=username,
            password=password,
        )
        login(self.request, user=user)
        return response
