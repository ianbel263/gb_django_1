from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket

success_messages = {
    'register': _('You have successfully registered'),
    'profile': _('Changes saved successfully')
}


def register(request):
    title = 'GeekShop - Регистрация'
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, success_messages['register'])
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegisterForm()

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'authapp/register.html', context)


def login(request):
    title = 'GeekShop - Авторизация'
    next_page = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': title,
        'form': form,
        'next': next_page
    }
    return render(request, 'authapp/login.html', context)


@login_required
def profile(request):
    title = 'GeekShop - Профиль пользователя'
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid() and form.changed_data:
            form.save()
            messages.success(request, success_messages['profile'])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': title,
        'form': form,
        'baskets': Basket.objects.filter(user=request.user)
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'mainapp/index.html')
