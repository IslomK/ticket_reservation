from django.db import models


class Reservation(models.Model):
    PAID = 'paid'
    CANCELLED = 'cancelled'
    NOT_PAID = 'not_paid'

    RESERVATION_STATUSES = (
        (PAID, 'Paid'),
        (CANCELLED, 'Cancelled'),
        (NOT_PAID, 'Not paid')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    status = models.CharField(choices=RESERVATION_STATUSES, default=NOT_PAID, max_length=250)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "ticket": {
                "id": self.ticket.id,
                "type": self.ticket.ticket_type,
                "price": self.ticket.price
            },
            "client": {
                "id": self.client.id,
                "first_name": self.client.first_name,
                "last_name": self.client.last_name
            },
            "status": self.status,
            "total_price": self.total_price
        }