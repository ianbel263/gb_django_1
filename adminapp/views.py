from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from adminapp.forms import UserCreateForm, UserUpdateForm
from authapp.models import User


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


@user_passes_test(lambda user: user.is_superuser)
def users(request):
    title = 'Geekshop - Пользователи'
    all_users = User.objects.all()
    context = {
        'title': title,
        'users': all_users
    }
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda user: user.is_superuser)
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


@user_passes_test(lambda user: user.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    title = f'Geekshop - Редактирование пользователя - {current_user.username}'
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=current_user)
        if form.is_valid():
            if form.changed_data:
                form.save()
                messages.success(request, f'Пользователь {current_user.username} обновлен')
            else:
                messages.success(request, 'Вы ничего не изменили')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = UserUpdateForm(instance=current_user)
    context = {
        'title': title,
        'form': form,
        'user': current_user
    }
    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, pk):
    if request.method == 'POST':
        current_user = get_object_or_404(User, pk=pk)
        current_user.is_active = False
        current_user.save()
        messages.success(request, 'Пользователь успешно удален')
    return HttpResponseRedirect(reverse('adminapp:users'))
