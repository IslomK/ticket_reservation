import json

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import ReservationView
from core.test_utils import Helper


class TestReservations(APITestCase):
    RESERVATION_PATH = 'v1/reservations/'
    RESERVATION_DETAIL_PATH = 'v1/reservations/{}'

    def setUp(self) -> None:
        self.reservation_view = ReservationView.as_view()
        self.factory = APIRequestFactory()
        self.client = Helper.add_client()
        self.event = Helper.add_event()
        self.vip_ticket = Helper.add_vip_tickets(
            event_id=self.event.id,
            quantity=100,
            price=2000
        )

    def test_can_create_reservation(self):
        data = {
            "client_id": self.client.id,
            "ticket_id": self.vip_ticket.id,
            "quantity": 10
        }

        request = self.factory.post(self.RESERVATION_PATH, data=json.dumps(data), content_type="application/json")
        response = self.reservation_view(request)

        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validation_error(self):
        data = {
            "ticket_id": self.vip_ticket.id,
            "quantity": 10
        }

        request = self.factory.post(self.RESERVATION_PATH, data=json.dumps(data), content_type="application/json")
        response = self.reservation_view(request)

        response.render()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_ticket_id(self):
        data = {
            "client_id": self.client.id,
            "ticket_id": 123123123123,
            "quantity": 10
        }

        request = self.factory.post(self.RESERVATION_PATH, data=json.dumps(data), content_type="application/json")
        response = self.reservation_view(request)

        response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)