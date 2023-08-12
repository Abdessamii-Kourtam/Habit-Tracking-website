from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Habit
from .forms import HabitForm  
from .habit_analysis import max_longest_streak,  habits_by_periodicity, min_longest_streak
# Create your views here.

def register_page(request):
    """
    Renders the login-register page if the request method is not POST.
    if the request method is POST( the user has filled the UserCreationForm) it checks if the data is valid and then saves the user and logs him in or return an error message
    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration!")  
        
    context = {'form':form}
    return render(request,'base/login_register.html',context)

def login_page(request):
    """
    Renders the login-register page if the request method is not POST.
    if the request method is POST( the user has entered his login credential), it authenticates the user and logs him else it return an error message.
    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password doesn't exist")
    
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logout_user(request):
    """
    logs the user out.
    """
    logout(request)
    return redirect('home')

def home(request):
    """
    renders the home page.
    if the user is authenticated, it shows the habits created by that user.
    if the user is not authenticated, it shows the pre-defined habits.
    it fillters the habit list into all, daily and weekly.
    it also shows the habit that has the longest longest-streak and the habit that has the shortest longest-streak.
    """
    Habit.uncheck_daily()
    Habit.uncheck_weekly()
    if request.user.is_authenticated:
        habits = Habit.objects.filter(user_id=request.user.id)
    else:
        habits = Habit.objects.filter(user_id=2)
    if request.GET.get('q') != None:
        habits = habits_by_periodicity(habits,request.GET.get('q')) 
    habit_count = habits.count()
    mls_habit = min_longest_streak(habits)
    MLS_habit = max_longest_streak(habits)
    
    context = {'habits': habits, 'habit_count': habit_count,'MLS_habit': MLS_habit, 'mls_habit':mls_habit}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def create_habit(request):
    """
    Renders the habit_form page if the request method is not POST.
    if the request method is POST( the user has entered the habit name,task and periodicity), it checks if the data is valid and then saves it.
    if the user is not logged in it redirect him to the login page.
    """
    form = HabitForm()
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit=form.save(commit=False)
            habit.user=request.user
            habit.save()
            return redirect('home')
    context = {'form' : form}
    return render(request,'base/habit_form.html',context)

#@login_required(login_url='login')
def update_habit(request, pk):
    """
    Renders the habit_form page filled with the data of the selected habit(habit that has id=pk) if the request method is not POST.
    if the request method is POST (the user has updated the habit name,task or periodicity), it checks if the data is valid and then saves it.
    """
    habit = Habit.objects.get(id=pk)
    form = HabitForm(instance=habit)
    if request.method =='POST':
        form = HabitForm(request.POST,instance=habit)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/habit_form.html', context)

def check_habit_off(request, pk):
    """
    checks the habit that has id = pk
    """
    habit = Habit.objects.get(id=pk)
    habit.check_off()
    return redirect('home')


#@login_required(login_url='login')
def delete_habit(request, pk):
    """
    Renders the delete_obj page
    if the request method is post, it deletes the habit that has id=pk
    """
    habit = Habit.objects.get(id=pk)
    if request.method == 'POST':
        habit.delete()
        return redirect('home')
    return render(request,'base/delete_obj.html',{'obj':habit.name})