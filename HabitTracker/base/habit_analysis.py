def min_longest_streak(habits):
    """
    gets the habit that has the shortest longest-streak.
    """
    return habits.order_by('-longest_streak').last()

def max_longest_streak(habits):
    """
    gets the habit that has the longest longest-streak.
    """
    return habits.order_by('-longest_streak').first()

def habits_by_periodicity(habits,q): 
    """
    fillters the habits by their periodicity (daily/weekly).
    """  
    return habits.filter(periodicity=q) 



