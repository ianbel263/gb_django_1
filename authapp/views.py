from django.conf import settings
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserAdditionalProfileForm
from authapp.models import User

success_messages = {
    'register': _('You have successfully registered'),
    'profile': _('Changes saved successfully')
}


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'authapp/login.html'
    next = None
    extra_context = {
        'title': 'GeekShop - Авторизация'
    }

    def get(self, request, *args, **kwargs):
        if 'next' in request.GET.keys():
            self.next = request.GET['next']
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print(self.next)
        return super(UserLoginView, self).get_context_data(next=self.next)

    def get_success_url(self):
        self.success_url = self.request.POST['next']
        return super(UserLoginView, self).get_success_url()


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    extra_context = {'title': 'GeekShop - Регистрация'}
    success_url = reverse_lazy('authapp:login')
    success_message = success_messages['register']

    def form_valid(self, form):
        response = super(UserCreateView, self).form_valid(form)
        try:
            self.send_verify_link(self.object)
        except Exception as e:
            pass
        return response

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse_lazy('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME}\nпройдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires_at = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse_lazy('index'))


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'authapp/profile.html'
    extra_context = {
        'title': 'GeekShop - Профиль пользователя',
    }
    success_message = success_messages['profile']

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        user_additional_profile_form = UserAdditionalProfileForm(data=request.POST, instance=request.user.userprofile)

        if user_profile_form.is_valid() and user_additional_profile_form.is_valid():
            return self.form_valid(user_profile_form)
        else:
            return self.form_invalid(user_profile_form)

    def get_context_data(self, **kwargs):
        return super(UserUpdateView, self).get_context_data(
            additional_form=UserAdditionalProfileForm(instance=self.request.user.userprofile),
            **kwargs)

    def get_success_url(self):
        return reverse_lazy('authapp:profile', kwargs={'pk': self.object.pk})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
