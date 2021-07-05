import datetime

from api.models import User, Event, Ticket, Reservation
from api.models.transactions import Transaction


class Helper(object):
    @staticmethod
    def add_client():
        """
        Creates a client
        :return: a User object
        """

        client = User.objects.create(
            user_type=User.CLIENT,
            first_name="John",
            last_name="Doe",
            phone="99893939393",
            email="iasdfdasf.as@mail.com",
            username="islomkasdf@asdfas.com"
        )

        return client

    @staticmethod
    def add_event():
        """
        Creates an event
        :return:
        """

        event = Event.objects.create(
            name="Big event",
            datetime=datetime.datetime.now(),
            premium_tickets=True,
            regular_tickets=True,
            vip_tickets=True
        )

        return event

    @staticmethod
    def add_vip_tickets(event_id, quantity, price):
        event = Event.objects.get(id=event_id)

        if event.vip_tickets:
            vip_ticket = Ticket.objects.create(
                event_id=event_id,
                quantity=quantity,
                price=price,
                available=True,
                ticket_type=Ticket.VIP
            )

            return vip_ticket

    @staticmethod
    def add_regular_tickets(event_id, quantity, price):
        event = Event.objects.get(id=event_id)

        if event.regular_tickets:
            regular = Ticket.objects.create(
                event_id=event_id,
                quantity=quantity,
                price=price,
                available=True,
                ticket_type=Ticket.REGULAR
            )

            return regular

    @staticmethod
    def add_premium_tickets(event_id, quantity, price):
        event = Event.objects.get(id=event_id)

        if event.regular_tickets:
            premium = Ticket.objects.create(
                event_id=event_id,
                quantity=quantity,
                price=price,
                available=True,
                ticket_type=Ticket.PREMIUM
            )

            return premium

    @staticmethod
    def add_reservation(client_id, ticket_id, quantity):
        ticket = Ticket.objects.get(id=ticket_id)

        reservation = Reservation.objects.create(
            client_id=client_id,
            ticket_id=ticket_id,
            quantity=quantity,
            total_price=(ticket.price * quantity)
        )

        ticket.decrease_quantity(quantity)
        ticket.save()

        return reservation

    @staticmethod
    def add_transaction(reservation_id, total_cost):
        transaction = Transaction.objects.create(
            reservation_id=reservation_id,
            amount=total_cost
        )

        return transaction