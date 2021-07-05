from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from api.views import EventView
from core.test_utils import Helper


class TestEvents(APITestCase):
    PATH_TO_EVENTS_LIST = 'v1/events/'
    PATH_TO_EVENTS_DETAIL = 'v1/events/{}/'

    def setUp(self) -> None:
        self.event = Helper.add_event()
        self.factory = APIRequestFactory()

    def test_can_get_events_list(self):
        self.event_view = EventView.as_view({"get": "list"})

        request = self.factory.get(self.PATH_TO_EVENTS_LIST, content_type='application/json')
        response = self.event_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_event_detail(self):
        self.event_view = EventView.as_view({"get": "retrieve"})

        request = self.factory.get(self.PATH_TO_EVENTS_DETAIL.format(self.event.id), content_type='application/json')
        response = self.event_view(request, self.event.id)

        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)