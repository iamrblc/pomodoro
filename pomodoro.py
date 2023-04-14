# Import libraries
import datetime

# Define dictionary
timetable = {}

# Define default values
DEFAULT_DAY_START = datetime.datetime.now().time().strftime('%H:%M')
DEFAULT_LUNCH = "12:00"
DEFAULT_DOG_WALK = "15:00"
DEFAULT_NUMBER_OF_POMODOROS = 8
DEFAULT_POMODORO = 45
DEFAULT_SHORT_RECESS = 10
DEFAULT_LONG_RECESS = 15
DEFAULT_RECREATION = 60

# Define constants
CONSECUTIVE_SHORT_BREAKS = 0

# Prompt user for input with default values
DAY_START = input(f"What time would you like to start your day (HH:MM)? (default: {DEFAULT_DAY_START}) ") or DEFAULT_DAY_START
LUNCH = input(f"What time would you have lunch (HH:MM)? (default: {DEFAULT_LUNCH}) ") or DEFAULT_LUNCH
DOG_WALK = input(f"What time would you like to take your dog for a walk (HH:MM)? (default: {DEFAULT_DOG_WALK}) ") or DEFAULT_DOG_WALK
NUMBER_OF_POMODOROS = int(input(f"How many pomodoros would you like to do today? (default: {DEFAULT_NUMBER_OF_POMODOROS}) ") or DEFAULT_NUMBER_OF_POMODOROS)
POMODORO = int(input(f"How long would you like your pomodoros to be (in minutes)? (default: {DEFAULT_POMODORO}) ") or DEFAULT_POMODORO)
SHORT_RECESS = int(input(f"How long would you like your short recesses to be (in minutes)? (default: {DEFAULT_SHORT_RECESS}) ") or DEFAULT_SHORT_RECESS)
LONG_RECESS = int(input(f"How long would you like your long recesses to be (in minutes)? (default: {DEFAULT_LONG_RECESS}) ") or DEFAULT_LONG_RECESS)
RECREATION = int(input(f"How long would you like your recreation to be (in minutes)? (default: {DEFAULT_RECREATION}) ") or DEFAULT_RECREATION)

# Conversions
day_start_time = datetime.datetime.strptime(DAY_START, '%H:%M').time()
lunch_time = datetime.datetime.strptime(LUNCH, '%H:%M').time()
dog_walk_time = datetime.datetime.strptime(DOG_WALK, '%H:%M').time()
pomodoro_duration = datetime.timedelta(minutes=POMODORO)
short_recess_duration = datetime.timedelta(minutes=SHORT_RECESS)
long_recess_duration = datetime.timedelta(minutes=LONG_RECESS)
recreation_duration = datetime.timedelta(minutes=RECREATION)

# Define first pomodoro function
def first_pomodoro(day_start_time, pomodoro_duration, timetable):
    pomodoro_count = 1
    pomodoro_end = (datetime.datetime.combine(datetime.date.min, day_start_time) + pomodoro_duration).time()
    pomodoro_start_str = day_start_time.strftime('%H:%M')
    pomodoro_end_str = pomodoro_end.strftime('%H:%M')
    # Extend timetable dictionary with pomodoro_count, pomodoro_start, pomodoro_end
    timetable[f'pomodoro_{pomodoro_count}'] = (pomodoro_start_str, pomodoro_end_str)
    return pomodoro_count, pomodoro_end

# Define recesses function
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
    pomodoro_start = (datetime.datetime.combine(datetime.date.min, pomodoro_end) + recess_duration).time()
    return pomodoro_start

# Define subsequent pomodoros function
def subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable):
    pomodoro_count += 1  # Increment pomodoro_count by 1
    pomodoro_end = (datetime.datetime.combine(datetime.date.min, pomodoro_start) + pomodoro_duration).time()
    pomodoro_start_str = pomodoro_start.strftime('%H:%M')
    pomodoro_end_str = pomodoro_end.strftime('%H:%M')
    timetable[f'pomodoro_{pomodoro_count}'] = (pomodoro_start_str, pomodoro_end_str)
    return pomodoro_count, pomodoro_end

# Create firt pomodoro
pomodoro_count, pomodoro_end = first_pomodoro(day_start_time, pomodoro_duration, timetable)

for i in range(NUMBER_OF_POMODOROS - 1):
    # Calculate time till lunch and time till dog walk
    time_till_lunch = abs(lunch_time.hour * 60 + lunch_time.minute - pomodoro_end.hour * 60 - pomodoro_end.minute)
    time_till_dog_walk = abs(dog_walk_time.hour * 60 + dog_walk_time.minute - pomodoro_end.hour * 60 - pomodoro_end.minute)

    if time_till_lunch < pomodoro_duration.seconds / 60 / 2 or time_till_dog_walk < pomodoro_duration.seconds / 60 / 2:
        # If time till lunch or time till dog walk is less than half of pomodoro duration, add recreation
        pomodoro_start = add_recess(pomodoro_end, recess_type='recreation', timetable=timetable)
        pomodoro_count, pomodoro_end = subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable)
        CONSECUTIVE_SHORT_BREAKS = 0
    else:
        if CONSECUTIVE_SHORT_BREAKS == 2:
            # If three consecutive short breaks have been added, add a long recess
            pomodoro_start = add_recess(pomodoro_end, recess_type='long', timetable=timetable)
            CONSECUTIVE_SHORT_BREAKS = 0
        else:
            # Otherwise, add a short recess
            pomodoro_start = add_recess(pomodoro_end, recess_type='short', timetable=timetable)
            CONSECUTIVE_SHORT_BREAKS += 1
        pomodoro_count, pomodoro_end = subsequent_pomodoros(pomodoro_count, pomodoro_start, pomodoro_duration, timetable)

# Create a list of tuples to hold the table data
table_data = []

# Iterate through the dictionary keys and values
for key, value in timetable.items():
    if key.startswith('pomodoro'):  # Check if key starts with 'pomodoro'
        # Create a row with key and value elements
        row = [key.strip('pomodoro_'), value[0], value[1], '']
        table_data.append(row)
    else:  # For other keys, use the value as a single cell in the table
        table_data[-1][-1] = value

# Define the column headers
column_headers = ['Pomodoro', 'Start Time', 'End Time', 'Break']

# Print the table using f-strings
print(f"{column_headers[0]:<12} {column_headers[1]:<12} {column_headers[2]:<12} {column_headers[3]:<12}")
for row in table_data:
    print(f"{row[0]:<12} {row[1]:<12} {row[2]:<12} {row[3]:<12}")
