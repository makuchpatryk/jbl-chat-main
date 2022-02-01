from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('users/', views.Users.as_view(), name='users'),

    path('message/<int:receiver_id>/', views.Message.as_view(), name='message'),
]