from __future__ import absolute_import, unicode_literals


import datetime
import logging

from celery import Task
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from api.models import Reservation
from monterail.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_reservation_status(self: Task, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except ObjectDoesNotExist:
        logger.error("Reservation with given id not found - {}".format(reservation_id))
        raise NotFound()

    datediff = datetime.datetime.now(datetime.timezone.utc) - reservation.created_at
    if datediff.seconds >= 900:
        reservation.status = Reservation.CANCELLED
        reservation.save()
