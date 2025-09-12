##### IMPORTS #####
from datetime import datetime

#####################################################################################
# ERRORS SECTION
#####################################################################################

### ERROR MESSAGES ###
format_error = "Error: Invalid format."
month_error = "Error: Month must be in [1, 12]."
hour_error = "Error: Hour must be in [0, 23]."
minute_error = "Error: Minute must be in [0, 59]."
second_error = "Error: Second must be in [0, 59]."

"""
This function checks whether the day is valid based on the year and month.
This accounts for leap years.
"""
def day_error(year, month, day):
    max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Fix February maximum for leap-year
    if year % 4 == 0:
        max_days[1] = 29

    # Error check for invalid day
    if day < 1 or day > max_days[month-1]:
        return f"Error: Day must be in [1, {max_days[month-1]}]."
    return ""

#####################################################################################
# TIME SECTION
#####################################################################################

"""
This function returns the time based on whether the user has inputted
time elapsed or start and end dates. If the latter, work is passed onto
the time_elapsed function to calculate the difference between the start
and end dates.
"""
def get_time(dates, time_input, start_date, end_date):
    if not dates:
        return time_input
    else:
        return time_elapsed(start_date, end_date)

"""
This function calculates the time elapsed between a start date and end date.
It checks for the following errors:
   Invalid number of dash separators
   Invalid length of year/month/day/hour/minute/second
   Non-integer date/time inputs
   Negative date/time inputs
   Invalid month
   Invalid day
   Invalid hour
   Invalid minute
   Invalid second
If no errors apply, we return the difference between the two dates in seconds.
"""
def time_elapsed(start_date, end_date):
    start_split = start_date.split("-")
    end_split = end_date.split("-")

    # Error check for invalid format
    if len(start_split) != 6 or len(end_split) != 6:
        return format_error

    # Error check for invalid format
    if len(start_split[0]) != 4 or len(end_split[0]) != 4 or\
        len(start_split[1]) != 2 or len(end_split[1]) != 2 or\
        len(start_split[2]) != 2 or len(end_split[2]) != 2 or\
        len(start_split[3]) != 2 or len(end_split[3]) != 2 or\
        len(start_split[4]) != 2 or len(end_split[4]) != 2 or\
        len(start_split[5]) != 2 or len(end_split[5]) != 2:
        return format_error

    # Error check for non-integer date/time inputs
    try:
        for x in range(6):
            start_split[x] = int(start_split[x])
            end_split[x] = int(end_split[x])
    except ValueError:
        return format_error

    # Error check for negative date/time inputs
    for x in range(6):
        if start_split[x] < 0 or end_split[x] < 0:
            return format_error

    # Error check for invalid month
    if start_split[1] < 1 or start_split[1] > 12 or\
       end_split[1] < 1 or end_split[1] > 12:
        return month_error

    # Error check for invalid day
    start_day_error = day_error(start_split[0], start_split[1], start_split[2])
    end_day_error = day_error(end_split[0], end_split[1], end_split[2])
    if start_day_error:
        return start_day_error
    if end_day_error:
        return end_day_error

    # Error check for invalid hour
    if start_split[3] > 23 or end_split[3] > 23:
        return hour_error

    # Error check for invalid minute
    if start_split[4] > 59 or end_split[3] > 59:
        return minute_error

    # Error check for invalid second
    if start_split[5] > 59 or end_split[5] > 59:
        return second_error

    # Format
    fmt = "%Y-%m-%d-%H-%M-%S"

    # Example dates
    d1 = datetime.strptime(start_date, fmt)
    d2 = datetime.strptime(end_date, fmt)

    # Difference in seconds
    diff_seconds = int((d2 - d1).total_seconds())
    return diff_seconds