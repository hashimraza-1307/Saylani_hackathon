# Smart Bus Ticket Booking & Reservation System

## Purpose
A text-based (console) Python application for a small bus service. Through a numbered menu the user can browse routes, search for routes, book seats, view bookings, cancel bookings, check seat availability, and generate a booking report with a route schedule.

It is a learning project that shows how Python lists, dictionaries, sets, tuples, loops and functions can solve a realistic reservation problem.

## Python requirement
- Python 3 (3.8 or newer recommended)
- No external libraries, database, or internet connection are needed. Only built-in Python features are used.

## How to run
1. Save the program as `main.py`.
2. Open a terminal in the folder that contains `main.py`.
3. Run:
   ```
   python main.py
   ```
   If `python` is not recognised, try `py main.py` or `python3 main.py`.
4. Type a menu number and press Enter.

Run the program in a real terminal. Read-only output panels (for example the VS Code Code Runner "Output" tab) cannot accept `input()`.

## Starting data
The program starts with five routes stored in memory:

| Route ID | Journey | Departure time | Fare (Rs.) | Seats |
|---|---|---|---|---|
| R101 | Karachi -> Hyderabad | 08:00 AM | 1200 | 40 |
| R102 | Karachi -> Sukkur | 09:30 AM | 2000 | 36 |
| R103 | Hyderabad -> Mirpur Khas | 11:00 AM | 800 | 32 |
| R104 | Karachi -> Lahore | 07:00 PM | 5000 | 45 |
| R105 | Sukkur -> Hyderabad | 02:00 PM | 1500 | 30 |

## Menu guide
| Option | What it does |
|---|---|
| 1. View Available Routes | Lists all routes with number, route ID, journey, departure time, fare and seats. Asks whether to show only routes with seats left. Shows `Fully Booked` when no seats remain. |
| 2. Search for a Route | Search by route ID, departure city, or destination city (case-insensitive). Shows all matches, or a no-match message. |
| 3. Book a Ticket | Asks for passenger name, age, route ID and number of seats, validates everything, then confirms the booking with a booking ID and total fare. |
| 4. View My Bookings | Lists all bookings, including cancelled ones. |
| 5. Cancel a Booking | Cancels a booking by ID. Only a Confirmed booking can be cancelled. The record is kept with status Cancelled and its seats are restored once. |
| 6. View Seat Availability | Shows available/total seats for every route with a status: Available, Partially Booked, or Fully Booked. Optional filter for routes with seats left. |
| 7. Generate Booking Report | Shows the booking report, then the route schedule grouped by departure city. |
| 8. Exit | Ends the program. |

Invalid menu input (text or an unsupported number) shows a helpful message and the menu appears again.

## Validation rules (Option 3)
| Field | Rule |
|---|---|
| Name | Must not be empty or only spaces |
| Age | Must be a positive whole number (text, 0 and negatives are rejected) |
| Route ID | Must be an existing route |
| Seats | Must be a whole number greater than zero and not more than the available seats |

All checks happen before anything is changed. If a check fails, no booking is created and seat counts stay the same.
Total fare = ticket price x number of seats. Booking IDs look like `B1001`, `B1002`, ... and are never repeated.

## Booking report (Option 7)
- Total bookings created, Confirmed bookings, Cancelled bookings
- Seats currently reserved and Confirmed revenue (Confirmed bookings only; cancelled bookings are excluded)
- Number of fully booked routes
- Confirmed seats and revenue for each route
- Route schedule by departure city (cities with no departures show `No scheduled departures.`)

## Sample workflow
```
Choose 3 -> Ahmed, 25, R101, 2
```
```
Booking confirmed!
Booking ID: B1001
Passenger: Ahmed
Route: R101 (Karachi -> Hyderabad)
Seats booked: 2
Fare per seat: Rs. 1200
Total fare: Rs. 2400
Status: Confirmed
```
```
Choose 6 -> R101 | Karachi -> Hyderabad | 38/40 seats | Partially Booked
Choose 5 -> B1001
```
```
Booking B1001 has been cancelled.
Seats restored: 2
Route R101 available seats: 40
```
```
Choose 7 -> Total bookings created: 1
            Confirmed bookings: 0
            Cancelled bookings: 1
            Confirmed revenue: Rs. 0
```

## How the program is organised (main.py)
| Part | Purpose |
|---|---|
| `SUPPORTED_CITIES` (tuple) | Cities used for the route schedule |
| `routes` (list of dictionaries) | Route ID, cities, time, ticket price, total and available seats |
| `bookings` (list of dictionaries) | Booking ID, passenger name and age, route ID, seats, total fare, status |
| `booking_ids` (set) | Booking IDs already issued, so IDs are never duplicated |
| `find_route()` | Finds a route by ID |
| `generate_booking_id()` | Creates a new unique booking ID |
| `show_menu()` | Prints the main menu |
| `view_routes()` | Option 1 |
| `search_route()` | Option 2 |
| `book_ticket()` | Option 3 |
| `view_bookings()` | Option 4 |
| `cancel_booking()` | Option 5 |
| `get_route_status()`, `view_availability()` | Option 6 |
| `generate_report()`, `show_schedule()` | Option 7 |
| `main()` | Menu loop (`while True`) that calls the functions above; Option 8 exits |

Python concepts used: `print()`, `input()`, `while`, `if/elif/else`, `for`, `break`, `continue`, `for-else`, `enumerate()`, lists, dictionaries, sets, tuples, functions, nested loops, and f-strings.

## Storage limitation (important)
All routes and bookings are stored **in memory only**. They exist only while the program is running and are **lost when the application closes**. Nothing is saved to a file or a database, so every new run starts again with the original five routes and no bookings.

## Constraints and out of scope
No GUI, website, mobile app, database, payment gateway, third-party API, external library, login or user accounts, and no saving of data between runs.

## Files
- `main.py` - the application
- `README.md` - this file
- `test_cases.txt` - the 12 required test scenarios with expected and actual results