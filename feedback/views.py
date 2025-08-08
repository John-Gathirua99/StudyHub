from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request, room_name):
    return render(request, 'feedback/chat.html', {
        'room_name': room_name,
        'user': request.user,
    })


import calendar
from datetime import datetime
from django.shortcuts import render

def calendar_view(request):
    # Get the current date
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day

    # Generate the calendar
    cal = calendar.HTMLCalendar()
    # Highlight today's date by replacing the date cell with a class "today"
    html_calendar = cal.formatmonth(year, month).replace(
        f'>{day}<', f' class="today">{day}<'
    )

    # Pass the calendar and current date details to the template
    return render(request, 'feedback/calendar.html', {'calendar': html_calendar, 'year': year, 'month': month})



@login_required
def timetable_view(request):
    # Define the days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Define the time slots
    time_slots = ['9:00 AM - 10:00 AM', '10:00 AM - 11:00 AM', '11:00 AM - 12:00 PM', '1:00 PM - 2:00 PM', '2:00 PM - 3:00 PM']

    # Define the timetable data
    timetable = {
        'Monday': ['Math', 'English', 'Physics', 'Chemistry', 'History'],
        'Tuesday': ['Biology', 'Geography', 'Math', 'English', 'Computer Science'],
        'Wednesday': ['Physics', 'Chemistry', 'Math', 'History', 'English'],
        'Thursday': ['Geography', 'Biology', 'English', 'Computer Science', 'Math'],
        'Friday': ['History', 'Physics', 'Chemistry', 'Math', 'English'],
    }

    # Pass the data to the template
    return render(request, 'feedback/timetable.html', {
        'days': days,
        'time_slots': time_slots,
        'timetable': timetable,
    })