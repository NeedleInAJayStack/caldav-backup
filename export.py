from io import TextIOWrapper
from caldav import DAVClient
from caldav import objects
from caldav.lib.error import AuthorizationError
from dotenv import load_dotenv
from getpass import getpass
from os import getenv
from os.path import join
from sys import exit
import re


URL_ENV   = 'CALENDAR_URL'
USER_ENV  = 'CALENDAR_USER'
PASS_ENV  = 'CALENDAR_PASS'
DESTINATION_ENV = 'DESTINATION'

def main():
    url      = getenv(URL_ENV)
    username = getenv(USER_ENV)
    password = getenv(PASS_ENV)
    destination = getenv(DESTINATION_ENV)

    if url is None:
        url = input('URL: ')
    if username is None:
        username = input('Username: ')
    if password is None:
        password = getpass(prompt='Password: ')

    client = DAVClient(
        url=url,
        username=username,
        password=password
    )

    try:
        principal = client.principal()
    except AuthorizationError:
        print('Invalid URL or credentials.')
        exit(1)

    if destination is None:
        username = input('Destination: ')

    for cal in principal.calendars():
        filename = join(destination, f'{cal.name}.ics')
        with open(filename, 'w') as f:
            write_calendar(cal, f)
            print(f'Exported events from calendar \'{cal.name}\' to {filename}')

def write_calendar(cal: objects.Calendar, f: TextIOWrapper):
    # This aggregates all events from a calendar into a multi-event ics file. Since the python
    # caldav package only exports data per event, we stitch together a file:
    # 1. Extract calendar data from a single event and write it
    # 2. Go thorugh each event, strip off calendar data, and write it
    # 3. Write a calendar close statement

    # Regex to separate calendar data and event data.
    icsFormat = re.compile('(BEGIN:VCALENDAR\n.*)(BEGIN:VEVENT\n.*)END:VCALENDAR', re.DOTALL)

    events = cal.events()

    # Write calendar details once
    if len(events) < 1:
        return
    calMatch = icsFormat.match(events[0].data)
    if calMatch is None:
        print('Invalid ics data formatting')
        exit(1)
    f.write(calMatch.group(1))

    # Write all event details for each event
    for event in events:
        match = icsFormat.match(event.data)
        if calMatch is None:
            print('Invalid ics data formatting')
            exit(1)
        f.write(match.group(2))
    
    # Write once to close the calendar
    f.write('END:VCALENDAR\n')

if __name__ == '__main__':
    try:
        load_dotenv()
        main()
    except KeyboardInterrupt:
        print('\nInterrupted.')
        exit(1)
