from threading import Lock
from datetime import datetime

class Stop:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Route:
    def __init__(self, stops):
        self.stops = stops  # List of Stop objects

    def __str__(self):
        return " -> ".join(str(stop) for stop in self.stops)

class Ticket:
    def __init__(self, train, car, seat, passenger_name, departure, arrival):
        self.train = train
        self.car = car
        self.seat = seat
        self.passenger_name = passenger_name
        self.departure = departure
        self.arrival = arrival
        self.timestamp = datetime.now()

    def __str__(self):
        return f"Ticket: {self.passenger_name}, Train {self.train.train_id}, Car {self.car}, Seat {self.seat}, {self.departure} -> {self.arrival} ({self.timestamp})"

class Train:
    def __init__(self, train_id, route, seats_per_car=10, num_cars=5):
        self.train_id = train_id
        self.route = route
        self.seats = {car: {seat: None for seat in range(1, seats_per_car+1)} for car in range(1, num_cars+1)}
        self.lock = Lock()

    def book_seat(self, car, seat, passenger_name, departure, arrival):
        with self.lock:
            if self.seats.get(car, {}).get(seat) is None:
                self.seats[car][seat] = Ticket(self, car, seat, passenger_name, departure, arrival)
                return self.seats[car][seat]
            else:
                return None

class TicketOffice:
    def __init__(self):
        self.sales = []

    def sell_ticket(self, train, car, seat, passenger_name, departure, arrival):
        ticket = train.book_seat(car, seat, passenger_name, departure, arrival)
        if ticket:
            self.sales.append(ticket)
            return ticket
        else:
            return "Seat is already taken!"