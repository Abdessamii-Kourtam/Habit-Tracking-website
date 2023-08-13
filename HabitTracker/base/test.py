from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .habit_analysis import min_longest_streak, max_longest_streak, habits_by_periodicity

class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        habits_data = [
            {
                'name': 'Jogging',
                'periodicity': 'Daily',
                'last_check': timezone.make_aware(timezone.datetime(2023, 8, 11, 18, 43)),
                'streak': 14,
                'longest_streak': 14,
            },
            {
                'name': 'Learn oop',
                'periodicity': 'Daily',
                'last_check': timezone.make_aware(timezone.datetime(2023, 8, 11, 17, 57)),
                'streak': 1,
                'longest_streak': 10,
            },
            {
                'name': 'Learn Django',
                'periodicity': 'Daily',
                'last_check': timezone.make_aware(timezone.datetime(2023, 8, 11, 17, 57)),
                'streak': 1,
                'longest_streak': 10,
            },
            {
                'name': 'Swimming',
                'periodicity': 'Weekly',
                'last_check': timezone.make_aware(timezone.datetime(2023, 8, 12, 18, 46)),
                'streak': 3,
                'longest_streak': 3,
            },
            {
                'name': 'Learn Python',
                'periodicity': 'Weekly',
                'last_check': timezone.make_aware(timezone.datetime(2023, 8, 7, 18, 37)),
                'streak': 3,
                'longest_streak': 3,
            },
            {
                'name': 'Reading a book',
                'periodicity': 'Weekly',
                'last_check': timezone.make_aware(timezone.datetime(2023, 7, 24, 18, 46)),
                'streak': 0,
                'longest_streak': 1,
            },
        ]

        self.habits = []
        for habit_data in habits_data:
            habit = Habit.objects.create(user=self.user, **habit_data)
            self.habits.append(habit)

    #Testing the Habit Model:

    def test_check_off_daily_increase_streak(self):
        daily_habit = self.habits[1]  # "Learn oop" is the second habit
        daily_habit.last_check = timezone.now() - timedelta(days=1)
        daily_habit.save()
        daily_habit.check_off()
        self.assertEqual(daily_habit.streak, 2)

    def test_check_off_daily_reset_streak(self):
        daily_habit = self.habits[2]  # "Learn Django" is the third habit
        daily_habit.last_check = timezone.now() - timedelta(weeks=1)
        daily_habit.streak = 5
        daily_habit.save()
        daily_habit.check_off()
        self.assertEqual(daily_habit.streak, 1)

    def test_check_off_weekly_increase_streak(self):
        weekly_habit = self.habits[3]  # "Swimming" is the fourth habit
        weekly_habit.last_check = timezone.now() - timedelta(weeks=1)
        weekly_habit.save()
        weekly_habit.check_off()
        self.assertEqual(weekly_habit.streak, 4)

    def test_check_off_weekly_reset_streak(self):
        weekly_habit = self.habits[4]  # "Learn Python" is the fifth habit
        weekly_habit.last_check = timezone.now() - timedelta(weeks=2)
        weekly_habit.streak = 5
        weekly_habit.save()
        weekly_habit.check_off()
        self.assertEqual(weekly_habit.streak, 1)

    def test_uncheck_daily(self):
        daily_habit = self.habits[1]  # "Learn oop" is the second habit
        daily_habit.streak = 3
        daily_habit.last_check = timezone.now() - timedelta(days=2)
        daily_habit.save()
        Habit.uncheck_daily()
        daily_habit.refresh_from_db()
        self.assertEqual(daily_habit.streak, 0)

    def test_uncheck_weekly(self):
        weekly_habit = self.habits[3]  # "Swimming" is the fourth habit
        weekly_habit.streak = 4
        weekly_habit.last_check = timezone.now() - timedelta(weeks=3)
        weekly_habit.save()
        Habit.uncheck_weekly()
        weekly_habit.refresh_from_db()
        self.assertEqual(weekly_habit.streak, 0)
    
    #Testing the habit_analysis:

    def test_min_longest_streak(self):
        habit = min_longest_streak(Habit.objects.all())
        self.assertEqual(habit.name, 'Reading a book')

    def test_max_longest_streak(self):
        habit = max_longest_streak(Habit.objects.all())
        self.assertEqual(habit.name, 'Jogging')

    def test_habits_by_periodicity_daily(self):
        daily_habits = habits_by_periodicity(Habit.objects.all(), 'Daily')
        self.assertEqual(daily_habits.count(), 3)

    def test_habits_by_periodicity_weekly(self):
        weekly_habits = habits_by_periodicity(Habit.objects.all(), 'Weekly')
        self.assertEqual(weekly_habits.count(), 3)






