from django.forms import ModelForm 
from .models import Habit

"""
this is the form that the user has to fill in order to create a habit.
"""
class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = ['name','task','periodicity']
