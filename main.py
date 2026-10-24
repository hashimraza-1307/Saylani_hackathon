# DATA (routes, bookings, booking IDs)

SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")  

routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []          
booking_ids = set()    
booking_counter = 1001



#  HELPER FUNCTIONS

def find_route(route_id):
    for route in routes:
        if route["route_id"].upper() == route_id.upper():
            return route
    return None


def generate_booking_id():
    global booking_counter
    while True:
        new_id = "B" + str(booking_counter)
        booking_counter += 1
        if new_id not in booking_ids:
            booking_ids.add(new_id)
            return new_id


def show_menu():
    print("\nSMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("================================")


# VIEW AVAILABLE ROUTES 

def view_routes():
    only_available = input("Show only routes with seats? (y/n): ").strip().lower() == "y"

    print("\nAVAILABLE BUS ROUTES")
    print(f"{'No.':<4}{'Route':<6}{'Journey':<32}{'Depart':<10}{'Fare':<9}Seats")

    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue 

        journey = route["departure_city"] + " -> " + route["destination_city"]
        fare = "Rs." + str(route["ticket_price"])
        if route["available_seats"] == 0:
            seats = "Fully Booked"
        else:
            seats = str(route["available_seats"]) + "/" + str(route["total_seats"])

        print(f"{number:<4}{route['route_id']:<6}{journey:<32}"
              f"{route['departure_time']:<10}{fare:<9}{seats}")


# SEARCH FOR A ROUTE 

def print_route_line(route):
    print(f"{route['route_id']} | {route['departure_city']} -> {route['destination_city']} "
          f"| Rs. {route['ticket_price']} | {route['available_seats']} seats available")


def search_route():
    term = input("Search by route ID or city: ").strip().lower()
    if term == "":
        print("Please enter a route ID or city name.")
        return

    found = False
    for route in routes:
        if route["route_id"].lower() == term:
            print_route_line(route)
            found = True
            break  
        if term in (route["departure_city"].lower(), route["destination_city"].lower()):
            print_route_line(route)
            found = True
    else:
        if found == False :
            print("No matching route found.")



# BOOK A TICKET 

def book_ticket():
    # Name
    name = input("Passenger name: ").strip()
    if name == "":
        print("Error: name cannot be empty.")
        return

    # Age
    age_text = input("Passenger age: ").strip()
    if not age_text.isdigit() or int(age_text) <= 0:
        print("Error: age must be a positive whole number.")
        return
    age = int(age_text)

    # Route ID
    route_id = input("Route ID (e.g. R101): ").strip()
    route = find_route(route_id)
    if route is None:
        print("Error: route not found.")
        return

    # Seats
    seats_text = input("Number of seats: ").strip()
    if not seats_text.isdigit() or int(seats_text) <= 0:
        print("Error: seats must be a whole number greater than zero.")
        return
    seats = int(seats_text)

    # 5) Availability
    if seats > route["available_seats"]:
        print(f"Error: only {route['available_seats']} seat(s) available on this route.")
        return

    
    total_fare = route["ticket_price"] * seats
    booking = {
        "booking_id": generate_booking_id(),
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID:", booking["booking_id"])
    print("Passenger:", name)
    print(f"Route: {route['route_id']} ({route['departure_city']} -> {route['destination_city']})")
    print("Seats booked:", seats)
    print("Fare per seat: Rs.", route["ticket_price"])
    print("Total fare: Rs.", total_fare)
    print("Status: Confirmed")



# VIEW MY BOOKINGS 

def view_bookings():
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print("\nBOOKING HISTORY")
    for number, b in enumerate(bookings, start=1):
        route = find_route(b["route_id"])
        journey = route["departure_city"] + " -> " + route["destination_city"]
        print(f"{number}. {b['booking_id']} | {b['passenger_name']} | {b['route_id']} ({journey}) "
              f"| Seats: {b['seats']} | Rs. {b['total_fare']} | {b['status']}")



# CANCEL A BOOKING 

def cancel_booking():
    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for b in bookings:
        if b["booking_id"] == booking_id:
            if b["status"] == "Cancelled":
                print("This booking is already cancelled. No seats restored.")
            else:
                b["status"] = "Cancelled"                
                route = find_route(b["route_id"])
                route["available_seats"] += b["seats"]    
                print(f"Booking {booking_id} has been cancelled.")
                print("Seats restored:", b["seats"])
                print(f"Route {route['route_id']} available seats: {route['available_seats']}")
            break
    else:
        print("Booking ID not found.")



# SEAT AVAILABILITY 

def get_route_status(route):
    if route["available_seats"] == 0:
        return "Fully Booked"
    elif route["available_seats"] == route["total_seats"]:
        return "Available"
    else:
        return "Partially Booked"


def view_availability():
    only_available = input("Show only routes with seats available? (y/n): ").strip().lower() == "y"

    print("\nSEAT AVAILABILITY")
    for route in routes:
        if route["available_seats"] < 0 or route["available_seats"] > route["total_seats"]:
            print(f"Warning: seat count error on route {route['route_id']}!")

        if only_available and route["available_seats"] == 0:
            continue 

        status = get_route_status(route)
        print(f"{route['route_id']} | {route['departure_city']} -> {route['destination_city']} "
              f"| {route['available_seats']}/{route['total_seats']} seats | {status}")



# BOOKING REPORT 

def generate_report():
    confirmed = 0
    cancelled = 0

    for b in bookings:
        if b["status"] == "Confirmed":
            confirmed += 1
        elif b["status"] == "Cancelled":
            cancelled += 1

    reserved_seats = 0
    revenue = 0
    fully_booked = 0
    route_lines = []

    for route in routes:                     
        route_seats = 0
        route_revenue = 0
        for b in bookings:                   
            if b["route_id"] == route["route_id"] and b["status"] == "Confirmed":
                route_seats += b["seats"]
                route_revenue += b["total_fare"]
        reserved_seats += route_seats
        revenue += route_revenue
        if route["available_seats"] == 0:
            fully_booked += 1
        route_lines.append(f"  {route['route_id']}: {route_seats} seat(s) reserved, "
                           f"Rs. {route_revenue:,}")

    print("\nBOOKING REPORT")
    print("Total bookings created:", len(bookings))
    print("Confirmed bookings:", confirmed)
    print("Cancelled bookings:", cancelled)
    print("Seats currently reserved:", reserved_seats)
    print(f"Confirmed revenue: Rs. {revenue:,}")
    print("Fully booked routes:", fully_booked)

    print("\nConfirmed bookings by route:")
    for line in route_lines:
        print(line)


# ROUTE SCHEDULE 

def show_schedule():
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in SUPPORTED_CITIES:            
        print(city)
        found = False
        for route in routes:                
            if route["departure_city"] == city:
                print(f"  {route['route_id']} -> {route['destination_city']:<12}"
                      f"| {route['departure_time']}")
                found = True
        if not found:
            print("  No scheduled departures.")

# MAIN MENU LOOP

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Invalid input. Please enter a number from 1 to 8.")
            continue

        choice = int(choice)

        if choice == 1:
            view_routes()
        elif choice == 2:
            search_route()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_availability()
        elif choice == 7:
            generate_report()
            show_schedule()
        elif choice == 8:
            print("Thank you for using Smart Bus Reservation System. Goodbye!")
            break
        else:
            print("Unsupported choice. Please enter a number from 1 to 8.")


main()