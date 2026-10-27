
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Tasks
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),

    # Goals
    path('add-goal/', views.add_goal, name='add_goal'),
    path('edit-goal/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('toggle-goal/<int:goal_id>/', views.toggle_goal, name='toggle_goal'),
    path('delete-goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),

    # Habits
    path('add-habit/', views.add_habit, name='add_habit'),
    path('toggle-habit/<int:habit_id>/', views.toggle_habit, name='toggle_habit'),
    path('delete-habit/<int:habit_id>/', views.delete_habit, name='delete_habit'),
]
