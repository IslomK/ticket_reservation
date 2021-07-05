import json

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import PaymentView, Reservation
from core.test_utils import Helper


class PaymentTestCase(APITestCase):
    PATH_TO_PAY = '/v1/reservations/{}/pay/'

    def setUp(self):
        self.payment_view = PaymentView.as_view()
        self.factory = APIRequestFactory()
        self.client = Helper.add_client()
        self.event = Helper.add_event()
        self.vip_ticket = Helper.add_vip_tickets(
            event_id=self.event.id,
            quantity=100,
            price=2000
        )

        self.reservation = Helper.add_reservation(
            client_id=self.client.id,
            ticket_id=self.vip_ticket.id,
            quantity=2
        )

    def test_can_pay_successfully(self):
        self.reservation.status = Reservation.NOT_PAID

        request = self.factory.post(
            self.PATH_TO_PAY.format(self.reservation.id),
            data=json.dumps({"currency": "EUR", "total_cost": self.reservation.total_price}),
            content_type='application/json'
        )

        response = self.payment_view(request, self.reservation.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_currency(self):
        self.reservation.status = Reservation.NOT_PAID
        self.reservation.save()

        request = self.factory.post(
            self.PATH_TO_PAY.format(self.reservation.id),
            data=json.dumps({"currency": "UZS", "total_cost": self.reservation.total_price}),
            content_type='application/json'
        )

        response = self.payment_view(request, self.reservation.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validation_error(self):
        self.reservation.status = Reservation.NOT_PAID
        self.reservation.save()

        request = self.factory.post(
            self.PATH_TO_PAY.format(self.reservation.id),
            data=json.dumps({"total_cost": self.reservation.total_price}),
            content_type='application/json'
        )

        response = self.payment_view(request, self.reservation.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reservation_cancelled(self):
        self.reservation.status = Reservation.CANCELLED
        self.reservation.save()

        request = self.factory.post(
            self.PATH_TO_PAY.format(self.reservation.id),
            data=json.dumps({"currency": "EUR", "total_cost": self.reservation.total_price}),
            content_type='application/json'
        )

        response = self.payment_view(request, self.reservation.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_already_paid(self):
        self.reservation.status = Reservation.PAID
        self.reservation.save()

        request = self.factory.post(
            self.PATH_TO_PAY.format(self.reservation.id),
            data=json.dumps({"currency": "EUR", "total_cost": self.reservation.total_price}),
            content_type='application/json'
        )
        response = self.payment_view(request, self.reservation.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
