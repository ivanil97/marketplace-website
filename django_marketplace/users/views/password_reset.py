from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = "templates_users/password_reset.html"
    email_template_name = "templates_users/password_reset_email.html"
    subject_template_name = "templates_users/password_reset_subject.txt"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("user:account")
