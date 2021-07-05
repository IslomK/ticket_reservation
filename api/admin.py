from django.contrib import admin
from api import models

admin.site.register(models.User)
admin.site.register(models.Reservation)
admin.site.register(models.Ticket)
admin.site.register(models.Event)
admin.site.register(models.Transaction)