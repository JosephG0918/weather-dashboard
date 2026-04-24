import re

def convert_to_12hour(day):
    """Converts time from 24-hour format (HH:MM) to 12-hour format (HH:MM AM/PM)."""
    time24 = re.search("[0-9]+-[0-9]+-[0-9]+ (.+)", day).group(1)
    day_without_time = re.search("([0-9]+-[0-9]+-[0-9]+) .+", day).group(1)

    hours = int(time24[:2])
    minutes = time24[3:]
    period = "AM"

    if hours >= 12:
        period = "PM"
        if hours > 12:
            hours -= 12
    elif hours == 0:
        hours = 12

    return f"{day_without_time} {hours:02}:{minutes} {period}"
