from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'adminapp/admin.html')


def users(request):
    title = 'Geekshop - пользователи'
    return render(request, 'adminapp/admin-users-read.html')


def user_create(request):
    return render(request, 'adminapp/admin-users-create.html')


def user_update(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')


def user_delete(request, pk):
    return render(request, 'adminapp/admin-users-update-delete.html')
