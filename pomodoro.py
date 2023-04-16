########################################################################
##                                                                    ##
## IMPORTANT:                                                         ##
##                                                                    ##
## DO NOT TAKE PRODUCTIVITY TOO SERIOUSLY, NO MATTER WHAT YOU SEE     ##
## ON LINKED IN. KEEP IN MIND THAT IT'S ONLY A VERY TOXIC PLATFORM    ##
## MOSTLY FOR SHOWING OFF ANXIETY AND FOR CIRCLE JERK.                ##
##                                                                    ##
## TAKE BREAKS. STEP BACK. ENJOY YOUR LIFE!                           ##
##                                                                    ##
########################################################################

'''
This is a pomodoro scheduler that allows you to set your own parameters.

I have set the default parameters to my own preferences with
- an hour lunch break around noon
- an hour dog walk break around 3pm
- a pomodoro of 45 minutes (mocking school classes)
- 8 pomodoros per day
- varying short and long recess times between pomodoros

All the above parameters can be adjusted at the beginning.
It starts the working day at the current time by default. (Can be adjusted.)
The code felxibly adjusts lunch and dog walk breaks to fit in with the pomodoro
schedule.

The code returns a timetable.
It DOES NOT set alarms or notifications. It was not a requirement for me but
it can be easily added as a feature. The "timetable" dictionary is a friendly
format for that. :)
'''

#############################
## IMPORTS AND DEFINITIONS ##
#############################

# Datetime module handles time and date objects
import datetime

# The timetable dictionary will store the timetable in a friendly format
timetable = {}

# DEFAULT VALUES FOR THE PARAMETERS
# Day starts when you run the code by default
DEFAULT_DAY_START = datetime.datetime.now().time().strftime('%H:%M')

# Lunch and dog walk times should be far enough to fit pomodoros in between
DEFAULT_LUNCH = "12:00"
DEFAULT_DOG_WALK = "15:00"

# I mimic my old high school schedule of 45 minutes per class and vaying recess times
DEFAULT_NUMBER_OF_POMODOROS = 8
DEFAULT_POMODORO = 45
DEFAULT_SHORT_RECESS = 10
DEFAULT_LONG_RECESS = 15
DEFAULT_RECREATION = 60

# This constant is used to determine when to have a long recess.
'''
This part is very specific to my own preferences. This is the time that I can do
some minor household stuff, prepare snacks or play with the dog a bit to keep her
calm while I'm working.
'''
NUM_SHORT_BREAKS = 2
CONSECUTIVE_SHORT_BREAKS = 0

# OVERWRITE DEFAULT VALUES WITH USER INPUT
'''
It might be annoying to keep hitting enter in the beginning, so perhaps a logic
can be added to only ask for user input if the default value is not suitable.
On the other hand this also makes you a bit more mindful. Not a bug, a feature. :)
'''
DAY_START = input(f"What time would you like to start your day (HH:MM)? (default: {DEFAULT_DAY_START}) ") or DEFAULT_DAY_START
LUNCH = input(f"What time would you have lunch (HH:MM)? (default: {DEFAULT_LUNCH}) ") or DEFAULT_LUNCH
DOG_WALK = input(f"What time would you like to take your dog for a walk (HH:MM)? (default: {DEFAULT_DOG_WALK}) ") or DEFAULT_DOG_WALK
NUMBER_OF_POMODOROS = int(input(f"How many pomodoros would you like to do today? (default: {DEFAULT_NUMBER_OF_POMODOROS}) ") or DEFAULT_NUMBER_OF_POMODOROS)
POMODORO = int(input(f"How long would you like your pomodoros to be (in minutes)? (default: {DEFAULT_POMODORO}) ") or DEFAULT_POMODORO)
SHORT_RECESS = int(input(f"How long would you like your short recesses to be (in minutes)? (default: {DEFAULT_SHORT_RECESS}) ") or DEFAULT_SHORT_RECESS)
LONG_RECESS = int(input(f"How long would you like your long recesses to be (in minutes)? (default: {DEFAULT_LONG_RECESS}) ") or DEFAULT_LONG_RECESS)
RECREATION = int(input(f"How long would you like your recreation to be (in minutes)? (default: {DEFAULT_RECREATION}) ") or DEFAULT_RECREATION)

# CONVERTING INPUTS TO DATETIME OBJECTS - boring stuff. Don't worry about it.
day_start_time = datetime.datetime.strptime(DAY_START, '%H:%M').time()
lunch_time = datetime.datetime.strptime(LUNCH, '%H:%M').time()
dog_walk_time = datetime.datetime.strptime(DOG_WALK, '%H:%M').time()
pomodoro_duration = datetime.timedelta(minutes=POMODORO)
short_recess_duration = datetime.timedelta(minutes=SHORT_RECESS)
long_recess_duration = datetime.timedelta(minutes=LONG_RECESS)
recreation_duration = datetime.timedelta(minutes=RECREATION)

########################
## DEFINING FUNCTIONS ##
########################

'''
This is the brain of the code. It defines the functions that will be used to
create the timetable. Don't change this if you don't know what you're doing.
'''

# First pomodoro is always at the start of the day.
def first_pomodoro(day_start_time, pomodoro_duration, timetable):
    pomodoro_count = 1
    pomodoro_end = (datetime.datetime.combine(datetime.date.min, day_start_time) + pomodoro_duration).time()
    pomodoro_start_str = day_start_time.strftime('%H:%M')
    pomodoro_end_str = pomodoro_end.strftime('%H:%M')
    # Extend timetable dictionary with pomodoro_count, pomodoro_start, pomodoro_end
    timetable[f'pomodoro_{pomodoro_count}'] = (pomodoro_start_str, pomodoro_end_str)
    return pomodoro_count, pomodoro_end

# There are three types of recesses: short, long and recreation (very long)
def add_recess(pomodoro_end, recess_type, timetable):
    timetable[f'recess_{pomodoro_count}'] = recess_type
    if recess_type == 'long':
        recess_duration = datetime.timedelta(minutes=LONG_RECESS)
    elif recess_type == 'short':
        recess_duration = datetime.timedelta(minutes=SHORT_RECESS)
    elif recess_type == 'recreation':
        recess_duration = datetime.timedelta(minutes=RECREATION)
    else:
        raise ValueError('Invalid recess type')
    # ValueError should never happen. It's just a safety net for future changes.
    pomodoro_start = (datetime.datetime.combine(datetime.date.min, pomodoro_end) + recess_duration).time()
    return pomodoro_start

# All the other pomodoros are created a bit differently than the first one
def subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable):
    pomodoro_count += 1  # Increment pomodoro_count by 1
    pomodoro_end = (datetime.datetime.combine(datetime.date.min, pomodoro_start) + pomodoro_duration).time()
    pomodoro_start_str = pomodoro_start.strftime('%H:%M')
    pomodoro_end_str = pomodoro_end.strftime('%H:%M')
    timetable[f'pomodoro_{pomodoro_count}'] = (pomodoro_start_str, pomodoro_end_str)
    return pomodoro_count, pomodoro_end

#############################
## CREATING TIMETABLE DATA ##
#############################

# Creating the first pomodoro is relatively simple
pomodoro_count, pomodoro_end = first_pomodoro(day_start_time, pomodoro_duration, timetable)

# Adding the appropriate recesses and subsequent pomodoros
'''
This might look a bit awkward, so here is what this loop does.
It first checks how much time is left until lunch and dog walk.
- If not much, it adds a recreation (Enough to fix lunch, walk with the dog.)
- If there is enough time for pomodoros, it adds a short recess and the next pomodoro, and so on.
- However, if there were two short breaks, the next one will be long. And so on.

As the loop goes on it populates the timetable dictionary with start, end times
and recess types. It also keeps track of the pomodoro_count.
'''

for i in range(NUMBER_OF_POMODOROS - 1):
    # Lunch_t, dogwalk_t and pomend_t are times after midnight in minutes
    lunch_t = lunch_time.hour * 60 + lunch_time.minute
    dogwalk_t = dog_walk_time.hour * 60 + dog_walk_time.minute
    pomend_t = pomodoro_end.hour * 60 + pomodoro_end.minute

    if (lunch_t - (POMODORO / 2)) <= pomend_t <= (lunch_t + (POMODORO)) or (dogwalk_t - (POMODORO / 2)) <= pomend_t <= (dogwalk_t + (POMODORO)):
        # If time till lunch or time till dog walk is less than half of pomodoro duration, add recreation
        pomodoro_start = add_recess(pomodoro_end, recess_type='recreation', timetable=timetable)
        pomodoro_count, pomodoro_end = subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable)
        CONSECUTIVE_SHORT_BREAKS = 0
    else:
        if CONSECUTIVE_SHORT_BREAKS == NUM_SHORT_BREAKS:
            # If three consecutive short breaks have been added, add a long recess
            pomodoro_start = add_recess(pomodoro_end, recess_type='long', timetable=timetable)
            CONSECUTIVE_SHORT_BREAKS = 0
        else:
            # Otherwise, add a short recess
            pomodoro_start = add_recess(pomodoro_end, recess_type='short', timetable=timetable)
            CONSECUTIVE_SHORT_BREAKS += 1
        pomodoro_count, pomodoro_end = subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable)


###########################################
## CREATING THE HUMAN READABLE TIMETABLE ##
###########################################

# CREATE A LIST OF TUPLES FOR THE TABLE - boring stuff, don't worry about it
table_data = []

# Iterate through the dictionary keys (pomodoros and recesses) and values (start and end times and recess types)
for key, value in timetable.items():
    if key.startswith('pomodoro'):  # Check if key starts with 'pomodoro'
        # Create a row with key and value elements
        row = [key.strip('pomodoro_'), value[0], value[1], '']
        table_data.append(row)
    else:  # For other keys, use the value as a single cell in the table
        table_data[-1][-1] = value

# Define the column headers for the table
column_headers = ['Pomodoro', 'Start Time', 'End Time', 'Break']

# Print the table using f-strings
print(f"{column_headers[0]:<12} {column_headers[1]:<12} {column_headers[2]:<12} {column_headers[3]:<12}")
for row in table_data:
    print(f"{row[0]:<12} {row[1]:<12} {row[2]:<12} {row[3]:<12}")

'''
Feel free to use this code in your own projects. If you do, please give credit. Thanks.
If you have any questions, feel free to ask: robilaci@gmail.com

And don't take productivity too seriously. Enjoy your life. :)
'''

#######################################################
## THE FOLLOWING CODE IS FOR TESTING A BEEPER MODULE ##
##   IT'S NOT YET INTEGRATED INTO THE MAIN PROGRAM   ##
#######################################################

import time
import pygame

# Create beeptime list from the timetable dictionary
start_beep_times = []
alert_beep_times = []
end_beep_times = []
for key, value in timetable.items():
    if key.startswith('pomodoro'):
        start_beep_times.append(value[0])
        end_beep_times.append(value[1])
        # Convert value[1] to datetime.time object
        end_time = datetime.datetime.strptime(value[1], '%H:%M').time()
        # Subtract 5 minutes from end_time
        alert_time = (datetime.datetime.combine(datetime.date.min, end_time) - datetime.timedelta(minutes=5)).time()
        # Convert alert_time to string
        alert_beep_times.append(alert_time.strftime('%H:%M'))

def play_beep(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.mixer.music.stop()

# Initialize Pygame
pygame.init()

# Start beeps
for beep_time in start_beep_times:
    current_time = time.strftime('%H:%M')
    while current_time != beep_time:
        current_time = time.strftime('%H:%M')
        time.sleep(1)
    play_beep('start_beep.mp3')
    time.sleep(1)

# Alert beeps
for beep_time in alert_beep_times:
    current_time = time.strftime('%H:%M')
    while current_time != beep_time:
        current_time = time.strftime('%H:%M')
        time.sleep(1)
    play_beep('alert_beep.mp3')
    time.sleep(1)

# End beeps
for beep_time in end_beep_times:
    current_time = time.strftime('%H:%M')
    while current_time != beep_time:
        current_time = time.strftime('%H:%M')
        time.sleep(1)
    play_beep('end_beep.mp3')
    time.sleep(1)

# Clean up pygame
pygame.mixer.quit()
