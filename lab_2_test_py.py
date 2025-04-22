import unittest
from lab_2 import Stop, Route, Train, TicketOffice

class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.stop1 = Stop("Kyiv")
        self.stop2 = Stop("Lviv")
        self.route = Route([self.stop1, self.stop2])
        self.train = Train("IC125", self.route)
        self.office = TicketOffice()

    def test_successful_booking(self):
        ticket = self.office.sell_ticket(self.train, 1, 1, "John", self.stop1, self.stop2)
        self.assertNotEqual(ticket, "Seat is already taken!")
        self.assertEqual(ticket.passenger_name, "John")

    def test_duplicate_booking(self):
        self.office.sell_ticket(self.train, 1, 1, "John", self.stop1, self.stop2)
        ticket = self.office.sell_ticket(self.train, 1, 1, "Jane", self.stop1, self.stop2)
        self.assertEqual(ticket, "Seat is already taken!")

    def test_ticket_info_format(self):
        ticket = self.office.sell_ticket(self.train, 1, 2, "John", self.stop1, self.stop2)
        self.assertIn("Ticket: John", str(ticket))
        self.assertIn("Kyiv -> Lviv", str(ticket))

if __name__ == '__main__':
    unittest.main()

