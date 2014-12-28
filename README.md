# Kayak Trips iCal Parser
I use Kayak's [Trips](https://www.kayak.com/trips) functionality to track flights and other reservations, because it does the same thing as TripIt but looks way nicer. I wrote this Python module to get data about my past flights in JSON format.

## Usage
1. Get your My Trips iCalendar URL from [this page](https://www.kayak.com/trips-preferences/?tfd=t)
2. Do something like this:

```python
  from trips import *
  cal = KayakCalendar.from_url("https://www.kayak.com/trips/ical/pbbbbbbt/what/isthis/calendar.ics")
  cal.flights
  # [<Flight DL 1473 SEA-JFK, 2014-09-18 10:59:00>, <Flight DL 443 JFK-SEA, 2014-09-22 18:45:00>, etc.]
  cal.flights[0].airline # "DL"
  cal.flights[0].departure_time_utc # datetime.datetime(2014, 9, 18, 17, 59, tzinfo=<UTC>)
  print cal.flights[0].json()
  # {
  #   "departure_time_local": "2014-09-18T10:59:00",
  #   "departure_airport": "SEA",
  #   "arrival_airport": "JFK",
  #   "arrival_time_utc": "2014-09-18T23:22:00+00:00",
  #   "flight_number": 1473,
  #   "airline": "DL",
  #   "arrival_time_local": "2014-09-18T19:22:00",
  #   "departure_time_utc": "2014-09-18T17:59:00+00:00"
  # }
  print cal.json()
  # [
  #   {
  #     "departure_time_local": "2014-09-18T10:59:00",
  #     "departure_airport": "SEA",
  #     "arrival_airport": "JFK",
  #     "arrival_time_utc": "2014-09-18T23:22:00+00:00",
  #     "flight_number": 1473,
  #     "airline": "DL",
  #     "arrival_time_local": "2014-09-18T19:22:00",
  #     "departure_time_utc": "2014-09-18T17:59:00+00:00"
  #   },
  #     {
  #     "departure_time_local": "2014-09-22T18:45:00",
  #     "departure_airport": "JFK",
  #     "arrival_airport": "SEA",
  #     "arrival_time_utc": "2014-09-23T04:55:00+00:00",
  #     "flight_number": 443,
  #     "airline": "DL",
  #     "arrival_time_local": "2014-09-22T21:55:00",
  #     "departure_time_utc": "2014-09-22T22:45:00+00:00"
  #   },
  #   etc.
  # ]
```

## Caveats
* Only parses flights right now
* Doesn't capture any fields besides the ones shown in the output above
* Doesn't really do any error checking
* Probably should be further refactored, ¯\\_(ツ)_/¯
