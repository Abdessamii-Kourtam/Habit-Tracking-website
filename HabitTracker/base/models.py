from django.db import models
from django.contrib.auth.models import User
import datetime as dt

Choices = (
    ('Daily' , 'Daily'),
    ('Weekly' , 'Weekly'),   
)

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    task = models.TextField(null= True, blank=True)
    periodicity = models.CharField(max_length=10, choices=Choices, default='Daily')
    last_check = models.DateTimeField(default= dt.datetime.now())
    created = models.DateTimeField(auto_now_add=True)
    streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    class Meta:
        ordering =['-longest_streak','-created']

    def __str__(self) -> str:
        return self.name
    
    def check_off(self):
        '''
        Updates the fields streak, longest-streak, last-check when the habit is completed.
        '''
        current_date = dt.date.today()
        # for daily habits, if the duration (in days) between the current date and the last check date is one day, we increase the streak by 1
        if(self.periodicity=='Daily'):
            if (current_date - self.last_check.date())== dt.timedelta(days=1):
                self.streak += 1
            elif (current_date - self.last_check.date())> dt.timedelta(days=1):
                self.streak = 1 

        # for weekly habits, if the difference between the current week number and the last check week number is 1 , we increase the streak by 1
        else:
            if (current_date.isocalendar()[1] - self.last_check.date().isocalendar()[1])== 1:
                self.streak += 1
            elif (current_date.isocalendar()[1] - self.last_check.date().isocalendar()[1])> 1:
                self.streak = 1 

        # update the longest_streak
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak 

        # for habits that has been just created
        if self.last_check.date()==self.created.date():
            self.streak=1
            self.longest_streak=1

        self.last_check = dt.datetime.now()
        self.save(update_fields=['streak','longest_streak','last_check'])
    


    @classmethod
    def uncheck_daily(cls):
            '''
            sets streaks of all the daily habits that has their streaks broken to 0
            '''
            Daily_habits = cls.objects.filter(periodicity='Daily')
            current_date = dt.date.today()
            for Daily_habit in Daily_habits:
                if (current_date - Daily_habit.last_check.date())> dt.timedelta(days=1):
                    Daily_habit.streak=0
                    Daily_habit.save(update_fields=['streak'])
    @classmethod
    def uncheck_weekly(cls):
            '''
            sets streaks of all the weekly habits that has their streaks broken to 0
            '''
            Weekly_habits = cls.objects.filter(periodicity='Weekly')
            current_date = dt.date.today()
            for Weekly_habit in Weekly_habits:
                if(current_date.isocalendar()[1] - Weekly_habit.last_check.date().isocalendar()[1])> 1:
                    Weekly_habit.streak=0
                    Weekly_habit.save(update_fields=['streak'])


            