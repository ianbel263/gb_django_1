from django.urls import path

from authapp.views import UserLoginView, UserCreateView, UserUpdateView, UserLogoutView

app_name = 'authapp'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('profile/<int:pk>', UserUpdateView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>', UserCreateView.verify, name='verify')
]
