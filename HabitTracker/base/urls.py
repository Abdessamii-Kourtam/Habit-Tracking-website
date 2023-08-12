from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('create-habit/',views.create_habit, name='create-habit'),
    path('update-habit/<str:pk>/',views.update_habit, name='update-habit'),
    path('delete-habit/<str:pk>/',views.delete_habit, name='delete-habit'),
    path('check-habit/<str:pk>/',views.check_habit_off, name='check-habit'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register')
]