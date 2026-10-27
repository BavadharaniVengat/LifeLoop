from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Goal, Habit



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', password)

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')




@login_required(login_url='login')
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    habits = Habit.objects.filter(user=request.user).order_by('-created_at')

    # Task statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    # Goal statistics
    total_goals = goals.count()
    completed_goals = goals.filter(completed=True).count()

    # Habit statistics
    total_habits = habits.count()
    completed_habits = habits.filter(completed_today=True).count()

    # Progress percentages
    task_progress = round(completed_tasks * 100 / total_tasks) if total_tasks else 0
    goal_progress = round(completed_goals * 100 / total_goals) if total_goals else 0
    habit_progress = round(completed_habits * 100 / total_habits) if total_habits else 0

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'goals': goals,
        'habits': habits,

        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_goals': total_goals,
        'completed_goals': completed_goals,

        'total_habits': total_habits,
        'completed_habits': completed_habits,

        'task_progress': task_progress,
        'goal_progress': goal_progress,
        'habit_progress': habit_progress,
    })

@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description
            )
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')

        messages.error(request, 'Please enter a task title.')

    return render(request, 'add_task.html')


@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            task.title = title
            task.description = description
            task.save()
            messages.success(request, 'Task updated!')
            return redirect('dashboard')

        messages.error(request, 'Task title is required.')

    return render(request, 'add_task.html', {'task': task})


@login_required(login_url='login')
def toggle_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
    return redirect('dashboard')


@login_required(login_url='login')
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        messages.success(request, 'Task deleted.')
    return redirect('dashboard')


@login_required(login_url='login')
def add_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            Goal.objects.create(
                user=request.user,
                title=title,
                description=description
            )
            messages.success(request, 'Goal added successfully!')
            return redirect('dashboard')

        messages.error(request, 'Please enter a goal title.')

    return render(request, 'add_goal.html')


@login_required(login_url='login')
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            goal.title = title
            goal.description = description
            goal.save()
            messages.success(request, 'Goal updated!')
            return redirect('dashboard')

        messages.error(request, 'Goal title is required.')

    return render(request, 'add_goal.html', {'goal': goal})


@login_required(login_url='login')
def toggle_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.completed = not goal.completed
        goal.save()
    return redirect('dashboard')


@login_required(login_url='login')
def delete_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.delete()
        messages.success(request, 'Goal deleted.')
    return redirect('dashboard')  



@login_required(login_url='login')
def add_habit(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()

        if title:
            Habit.objects.create(
                user=request.user,
                title=title
            )
            messages.success(request, 'Habit added successfully!')
            return redirect('dashboard')

        messages.error(request, 'Please enter a habit title.')

    return render(request, 'add_habit.html')


@login_required(login_url='login')
def toggle_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(
            Habit,
            id=habit_id,
            user=request.user
        )
        habit.completed_today = not habit.completed_today
        habit.save()

    return redirect('dashboard')


@login_required(login_url='login')
def delete_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(
            Habit,
            id=habit_id,
            user=request.user
        )
        habit.delete()
        messages.success(request, 'Habit deleted.')

    return redirect('dashboard')


