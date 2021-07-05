import logging

from django.db import DatabaseError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Ticket
from core.exceptions import InternalServiceError

logger = logging.getLogger(__name__)


class TicketView(APIView):
    def get(self, request):
        try:
            queryset = Ticket.objects.all().order_by('-created_at')
        except DatabaseError as ex:
            raise InternalServiceError(detail="Error occurred while getting tickets! Details - {}".format(ex))

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        ticket_type = request.GET.get('ticket_type', None)
        available = request.GET.get('available')
        event_id = request.GET.get('event_id')

        if ticket_type:
            queryset.filter(ticket_type=ticket_type)

        if available is not None:
            queryset.filter(available=available)

        if price_from:
            queryset.filter(price__gte=price_from)

        if price_to:
            queryset.filter(price__lte=price_to)

        if event_id:
            queryset.filter(event_id=event_id)

        data = []
        try:
            for ticket in queryset:
                data.append(ticket.to_dict())
        except AttributeError as ex:
            logger.error("Error occurred! Details - {}".format(ex))
            raise InternalServiceError()

        return Response(data=data)