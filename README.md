# caldav-backup
Python script to export all events in all calendars as `.ics` files from a CalDAV server. These can then be imported using various caldav
clients or when creating a DAViCal calendar.

## Dependencies
See `requirements.txt`.

## Usage
Just run `python export.py`

If you don't want to be prompted for e. g. the calendar URL, create
a `.env` file containing one or more of the following variables:
* `CALENDAR_URL` - the URL of the calendar
* `CALENDAR_USER` - the username for the calendar
* `CALENDAR_PASS` - the password for the calendar
* `DESTINATION` - the resulting folder of the `.ics` files

## License
See `LICENSE.txt`.

This script was heavily inspired by [this excellent repo](https://github.com/mvforell/caldav-export)

---

Copyright (c) 2022 Jay Herron
