import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Reservation
from api.models.transactions import Transaction
from api.serializers import PaymentSerializer
from core.error_codes import DATA_VALIDATION
from core.exceptions import ReservationCancelledError, BadRequestError, InternalServiceError
from core.payments import payment_service, CardError, PaymentError, CurrencyError

logger = logging.getLogger(__name__)


class PaymentView(APIView):
    def post(self, request, pk):
        serializer = PaymentSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError({
                'error': {
                    'type': DATA_VALIDATION,
                    'message': serializer.errors
                }
            })

        validated_data = serializer.validated_data

        total_cost = validated_data.get('total_cost')
        currency = validated_data.get('currency')

        reservation_id = pk

        with transaction.atomic():
            logger.info("Creating a payment for reservation - {}".format(reservation_id))
            try:
                reservation = Reservation.objects.get(id=reservation_id)
            except ObjectDoesNotExist:
                logger.error("Reservation not found! Id - {}".format(reservation_id))
                raise NotFound(detail="Reservation with id - {} not found".format(reservation_id))

            if reservation.status == Reservation.CANCELLED:
                raise ReservationCancelledError()

            if reservation.status == Reservation.PAID:
                return Response(data={"status": "success", "message": "reservation already paid"})

            try:
                payment_result = payment_service.charge(
                    amount=total_cost,
                    token='client_card_token',
                    currency=currency
                )
            except (CardError, PaymentError, CurrencyError) as ex:
                logger.error("Error occurred while using payment gateway. Ex - {}".format(ex))
                raise BadRequestError('Error occurred while paying the reservation. Details - {}'.format(ex))

            try:
                Transaction.objects.create(
                    reservation_id=reservation_id,
                    amount=payment_result.amount,
                    currency=payment_result.currency
                )
            except DatabaseError as ex:
                logger.error("Error occured while creating transaction! Reservation id - {}. Details - {}"
                             .format(reservation_id, ex))

                raise InternalServiceError()

            reservation.status = Reservation.PAID
            reservation.save()

        return Response(data={"status": "success"})
