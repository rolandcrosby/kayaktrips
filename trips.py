from icalendar import Calendar, Event
from datetime import datetime
import requests
import re
import json
import argparse
import sys

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class KayakCalendar(object):
    def __init__(self, ical_string):
        self.flights = []
        ical_data = Calendar.from_ical(ical_string)
        flights = filter(lambda x: ' - Flight ' in x.decoded('summary'), ical_data.subcomponents)
        for f in flights:
            self.add_flight(Flight(ical_event=f))

    def add_flight(self, flight):
        self.flights.append(flight)

    def json(self):
        self._sort_flights()
        return json.dumps([f.__dict__ for f in self.flights], cls=CustomEncoder, indent=4)

    @classmethod
    def from_url(cls, ical_url):
        return KayakCalendar(requests.get(ical_url).content)

    @classmethod
    def from_filename(cls, ical_filename):
        with open(ical_filename, 'r') as ical_file:
            return cls.from_file(ical_file)

    @classmethod
    def from_file(cls, ical_file):
        cal = KayakCalendar(ical_file.read())
        cal._sort_flights()
        return cal

    def _sort_flights(self):
        self.flights.sort(key=lambda f: f.departure_time_utc)

class Flight(object):
    def __init__(self, ical_event):
        self.type = "flight"
        self.airline, self.flight_number = self._parse_summary(ical_event.decoded('summary'))
        self.departure_time_utc = ical_event.decoded('dtstart')
        self.arrival_time_utc = ical_event.decoded('dtend')
        description = ical_event.decoded('description').split("\n")
        departing = self._first_with_prefix(description, "Departing")
        self.departure_airport, self.departure_time_local = self._parse_description_line(departing)
        arriving = self._first_with_prefix(description, "Arriving")
        self.arrival_airport, self.arrival_time_local = self._parse_description_line(arriving)
        self.description = str(self)

    def json(self):
        return json.dumps(self.__dict__, cls=CustomEncoder, indent=4)

    def __str__(self):
        return "%s %d %s-%s, %s" % (self.airline, self.flight_number, self.departure_airport, self.arrival_airport, self._date_fmt(self.departure_time_local))

    def __repr__(self):
        return "<Flight %s %d %s-%s, %s>" % (self.airline, self.flight_number, self.departure_airport, self.arrival_airport, self._datetime_fmt(self.departure_time_local))

    def _parse_summary(self, summary):
        m = re.match('.*Flight ([A-Z0-9]{2})? (\d+)', summary)
        airline = m.group(1)
        flight = int(m.group(2))
        if airline == None:
            airline = "[unknown]"
        return (airline, flight)

    def _parse_description_line(self, line):
        airport_code = re.match('.*\(([A-Z]{3})\)', line).group(1)
        m = re.match('.*(\d{2})/(\d{2})/(\d{4}) (\d{1,2}):(\d{2})([AP]M)', line)
        year = int(m.group(3))
        month = int(m.group(1))
        day = int(m.group(2))
        hour = int(m.group(4))
        minute = int(m.group(5))
        if m.group(6) == "PM" and hour != 12:
            hour = hour + 12
        return (airport_code, datetime(year, month, day, hour, minute))

    def _first_with_prefix(self, l, prefix, default=None):
        all_with_prefix = filter(lambda x: x.startswith(prefix), l)
        if len(all_with_prefix) > 0:
            return all_with_prefix[0]
        else:
            return default

    def _date_fmt(self, dt):
        return dt.strftime('%Y-%m-%d')

    def _datetime_fmt(self, dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')

def main():
    parser = argparse.ArgumentParser(description="Convert your Kayak trips iCal feed to JSON", add_help=True)
    parser.add_argument('-f', action='store', dest='in_file', help='File to load trips from')
    parser.add_argument('-u', action='store', dest='in_url', help='URL to load trips from')
    parser.add_argument('-o', action='store', dest='out_file', help='File to store trips in (defaults to STDOUT)')
    args = parser.parse_args()
    if args.in_file and args.in_url:
        parser.error('Must specify -f or -o only')
    if args.in_file:
        cal = KayakCalendar.from_filename(args.in_file)
    elif args.in_url:
        cal = KayakCalendar.from_url(args.in_url)
    else:
        if sys.stdin.isatty():
            parser.print_usage()
            sys.exit(1)
        cal = KayakCalendar.from_file(sys.stdin)
    json = cal.json()
    if args.out_file:
        with open(args.out_file, 'w') as f:
            f.write(json)
    else:
        print "heyyyyy"
        print(json)

if __name__ == "__main__":
    main()
