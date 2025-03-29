import os
import re
import uuid
from enum import Enum
from pathlib import Path
from bs4 import BeautifulSoup
from icalendar import Event, Calendar
from datetime import datetime, timedelta, date


class HolidayType(Enum):
    NATIONAL_HOLIDAY = 1
    STATE_HOLIDAY = 2
    MUNICIPAL_HOLIDAY = 3
    OPTIONAL_HOLIDAY = 4


def month_to_number(month):
    months = {
        'janeiro': 1,
        'fevereiro': 2,
        'março': 3,
        'abril': 4,
        'maio': 5,
        'junho': 6,
        'julho': 7,
        'agosto': 8,
        'setembro': 9,
        'outubro': 10,
        'novembro': 11,
        'dezembro': 12
    }

    month = month.lower()

    if month in months.keys():
        return months[month]
    else:
        return -1


def create_calendar(name, description):
    # init the calendar
    cal = Calendar()

    # Some properties are required to be compliant
    cal.add('PRODID', '-//Feriados Espirito Santo//lspaulucio//BR')
    cal.add('VERSION', '2.0')
    cal.add('CALSCALE', 'GREGORIAN')
    cal.add('METHOD', 'PUBLISH')
    cal.add("X-WR-CALNAME", name)
    cal.add("X-WR-TIMEZONE", "UTC")
    cal.add("X-WR-CALDESC", description)

    return cal


def create_calendar_event(eventInfo):
    event = Event()
    # Default parameters
    event.add('CLASS', 'PUBLIC')
    event.add('STATUS', 'CONFIRMED')
    event.add('TRANSP', 'TRANSPARENT')
    event.add('UID', f'{uuid.uuid4()}@calendares')
    event.add('DTSTAMP', datetime.now())

    event.add('NAME', eventInfo['description'])
    event.add('SUMMARY', eventInfo['description'])
    event.add('DESCRIPTION', eventInfo['description'])

    day = eventInfo['day']
    month = month_to_number(eventInfo['month'])
    year = datetime.now().year

    event_date = date(year, month, day)

    event.add('DTSTART', event_date)
    event.add('DTEND', event_date + timedelta(days=1))

    return event


def process_entry(entry):
    data = entry.split('.')[1]

    if ',' in data:
        day = data.split(',')[0].split()[0].strip()
        month = data.split(',')[0].split()[2].strip()
        weekday = data.split(" -")[1].strip()
        description = data.split(',')[1].split(" -")[0].strip()
    else:
        weekday = data.split(" -")[1].strip()
        day = data.split(" -")[0].split()[0].strip()
        month = data.split(" -")[0].split()[2].strip()
        description = data.split(" -")[0].split()[3:]
        if isinstance(description, list):
            description = " ".join(description)

    day = parser_day(day)

    print(
        f"""
        Dia da Semana: {weekday}\t\t
        Descrição: {description}\t
        Dia/Mes: {day}/{month}
    """)

    return {'day': day, 'month': month, 'description': description}


def parser_day(day_string):
    pattern = re.compile(r"[0-3]{0,1}[0-9]")

    return int(pattern.match(day_string).group())


def parser_content(html_content):

    events = []

    pattern = re.compile("^(X{0,3})(IX|IV|V?I{0,3})", re.ASCII)

    soup = BeautifulSoup(html_content, "html.parser")
    content_div = soup.find("div", class_="content-body")
    holidays = content_div.find_all(
        "p", string=lambda text: pattern.match(text).group() != '')

    for holiday in holidays:
        holiday = holiday.text

        # print(holiday)
        holiday_info = process_entry(holiday)
        events.append(create_calendar_event(holiday_info))

    return events


def save_calendar(calendar, filename='calendarES.ics'):
    directory = Path.cwd() / "CalendarES"
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder already exists")
    else:
        print("Folder was created")

    with open(os.path.join(directory, filename), 'wb') as f:
        f.write(calendar.to_ical())


def read_calendar(filepath):
    with open(filepath, 'rb') as f:
        calendar = Calendar.from_ical(f.read())
    return calendar
