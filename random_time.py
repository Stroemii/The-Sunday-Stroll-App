from datetime import datetime, timedelta

# the app wants to find couples to meet for a stroll on a sunday.
# app users can register to participate for one of the next four sundays.
# in order to simulate the user input data we need to create a list of the next four sundays


def next_4_saturdays():
    now = datetime.now().date()                 # current date which will be processed in the function
                                        
    while now.weekday() != 6:                   # 6 is sunday
        now += timedelta(days=1)                # find date of upcoming sunday
    
    upcoming_sunday = now                       # upcoming_sunday is needed in main.py and therefore needs to stay untouched
    next_4_sundays = [now]                      # create the list with the first sunday

    for _ in range(3):                          # append the three sundays after to the list
        now += timedelta(days=7)
        next_4_sundays.append(now)

    # we assume that the users choose the dates according to how near in the future it is. If it´s the next sunday, 40% of the users choose this date, 30% for the following sunday, 20%..., 10%... .
    probabilities = [0.4, 0.3, 0.2, 0.1]
    
    return next_4_sundays, probabilities, upcoming_sunday