from django.shortcuts import render

# Create your views here.
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
    return render(request, 'adminapp/admin-users-create.html')


def user_update(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')


def user_delete(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')
