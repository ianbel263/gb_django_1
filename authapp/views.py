from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from basketapp.models import Basket

success_messages = {
    'register': _('You have successfully registered'),
    'profile': _('Changes saved successfully')
}


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'authapp/login.html'
    next = None
    # redirect_to = '/'
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

    # def get_success_url(self):
    #     return self.redirect_to if 'next' not in self.request.POST.keys() \
    #         else self.request.POST['next']
    #
    # def post(self, request, *args, **kwargs):
    #     self.redirect_to = request.POST['next'] if 'next' in request.POST.keys() else ''
    #     self.extra_context.update({'next': self.redirect_to})
    #     return super(UserLoginView, self).get(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    extra_context = {'title': 'GeekShop - Регистрация'}
    success_url = reverse_lazy('authapp:login')
    success_message = success_messages['register']


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'authapp/profile.html'
    extra_context = {
        'title': 'GeekShop - Профиль пользователя',
    }
    success_message = success_messages['profile']

    def get_context_data(self, **kwargs):
        self.extra_context.update({'baskets': Basket.objects.filter(user=self.object.pk)})
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('authapp:profile', kwargs={'pk': self.object.pk})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
