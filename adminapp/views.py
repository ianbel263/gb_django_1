from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from adminapp.forms import UserCreateForm
from authapp.models import User


def index(request):
    return render(request, 'adminapp/admin.html')


def users(request):
    title = 'Geekshop - Пользователи'
    all_users = User.objects.all()
    context = {
        'title': title,
        'users': all_users
    }
    return render(request, 'adminapp/admin-users-read.html', context)


def user_create(request):
    title = 'Geekshop - Создание пользователя'
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь добавлен')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = UserCreateForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/admin-users-create.html', context)


def user_update(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')


def user_delete(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')
