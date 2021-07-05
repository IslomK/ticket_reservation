import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import Event
from core.exceptions import InternalServiceError

logger = logging.getLogger(__name__)


class EventView(ViewSet):
    def list(self, request):
        try:
            events = Event.objects.all()
        except DatabaseError as ex:
            logger.error("Error! Can't get the events. Detail - {}".format(ex))
            raise InternalServiceError()

        data = []
        for event in events:
            data.append(event.to_dict())

        return Response(data=data)

    def retrieve(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except ObjectDoesNotExist:
            logger.error("Event with id {} not found".format(pk))
            raise NotFound(detail="Event with given id not found")
        except DatabaseError as ex:
            logger.error("Error! Can't get the events. Detail - {}".format(ex))
            raise InternalServiceError(detail="Error occured. Details - {}".format(ex))

        return Response(data=event.to_dict())


