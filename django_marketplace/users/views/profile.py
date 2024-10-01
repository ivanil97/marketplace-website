from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from users.forms import ProfileDataForm
from users.models import User


class ProfileView(LoginRequiredMixin, FormView):
    """
    View-функция для представления профиля пользователя и изменения информации о нем
    """
    login_url = 'user:login'
    template_name = 'templates_users/user_profile.html'
    form_class = ProfileDataForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.request.user
        context['user'] = user_data
        print(vars(self.request.session))

        if 'form_submitted' in self.request.session:
            context['form_submitted'] = True
            del self.request.session['form_submitted']

        return context

    def form_valid(self, form):
        user = User.objects.filter(id=self.request.user.id).first()
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]
        user.phone_number = form.cleaned_data["phone_number"]

        if form.cleaned_data["profile_picture"]:
            user.profile_picture = form.cleaned_data["profile_picture"]

        if form.cleaned_data["password"]:
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(self.request, user)

        user.save()
        self.request.session['form_submitted'] = True

        return redirect('user:user_profile')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))