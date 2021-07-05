import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, Ticket, Reservation
from api.serializers import ReservationSerializer
from api.tasks import update_reservation_status
from core.error_codes import DATA_VALIDATION
from core.exceptions import InternalServiceError, OutOfStockError

logger = logging.getLogger(__name__)


class ReservationView(APIView):
    def get(self, request):
        try:
            qs = Reservation.objects.all()
        except DatabaseError as ex:
            logger.error("Error while getting reservation list. Exeption - {}".format(ex))
            raise InternalServiceError()

        event_id = request.GET.get('event_id', None)
        ticket_id = request.GET.get('ticket_id', None)
        client_id = request.GET.get('client_id', None)

        if event_id:
            qs.filter(ticket__event_id=event_id)

        if client_id:
            qs.filter(client_id=client_id)

        if ticket_id:
            qs.filter(ticket_id=ticket_id)

        data = []
        for reservation in qs:
            data.append(reservation.to_dict())

        return Response(data=data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError({
                'error': {
                    'type': DATA_VALIDATION,
                    'message': serializer.errors
                }
            })

        validated_data = serializer.validated_data

        client_id = validated_data.get('client_id')
        ticket_id = validated_data.get('ticket_id')
        quantity = validated_data.get('quantity')

        with transaction.atomic():
            logger.info("Creating a reservation. client_id - {}, ticket_id - {}, quantity - {}"
                        .format(client_id, ticket_id, quantity))
            try:
                client = User.objects.get(id=client_id, user_type=User.CLIENT)
            except ObjectDoesNotExist:
                logger.error("Client not found! Id - {}".format(client_id))
                raise NotFound(detail="Client with id - {} not found".format(client_id))

            try:
                ticket = Ticket.objects.get(id=ticket_id)
            except ObjectDoesNotExist:
                logger.error("Ticket not found! Id - {}".format(ticket_id))
                raise NotFound(detail="Ticket not found with id - {}".format(ticket_id))

            if not ticket.available:
                raise OutOfStockError()


            try:
                reservation = Reservation.objects.create(
                    ticket_id=ticket_id,
                    client_id=client_id,
                    quantity=quantity,
                    total_price=int(quantity * ticket.price)
                )

                ticket.decrease_quantity(quantity)
                update_reservation_status.delay(reservation.id)
            except DatabaseError as ex:
                logger.error("Cannot create reservation. Details - {}".format(ex))
                raise InternalServiceError()

        return Response(data={"status": "success"})


class ReservationDetailView(APIView):
    def get(self, request, pk):
        try:
            reservation = Reservation.objects.get(id=pk)
        except ObjectDoesNotExist:
            logger.error("Reservation not found! Id - {}".format(pk))
            raise NotFound(detail="Reservation with id - {} not found".format(pk))

        return Response(data=reservation.to_dict())




