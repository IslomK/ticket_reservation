from django.db import models

from core.exceptions import OutOfStockError


class Event(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    datetime = models.DateTimeField(null=False, blank=False)
    premium_tickets = models.BooleanField(default=False)
    regular_tickets = models.BooleanField(default=False)
    vip_tickets = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "ticket_types": {
                "premium": self.premium_tickets,
                "regular": self.regular_tickets,
                "vip": self.vip_tickets
            }
        }


class Ticket(models.Model):
    VIP = 'vip'
    REGULAR = 'regular'
    PREMIUM = 'premium'

    TICKET_TYPES = (
        (VIP, 'Vip'),
        (REGULAR, 'Regular'),
        (PREMIUM, 'Premium')
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='event_tickets')
    quantity = models.IntegerField(default=0)
    ticket_type = models.CharField(choices=TICKET_TYPES, default=REGULAR, max_length=250)
    price = models.IntegerField()
    available = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "ticket_type": self.ticket_type,
            "price": self.price,
            "available": self.available,
            "event": {
                "id": self.event.id,
                "name": self.event.name,
                "date": self.event.datetime
            }
        }

    def decrease_quantity(self, quantity):
        if quantity <= self.quantity:
            self.quantity -= quantity
            if self.quantity == 0:
                self.available = False
            self.save()
        else:
            raise OutOfStockError()