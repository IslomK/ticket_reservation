from django.urls import path
from api import views

urlpatterns = [
    path('events/', views.EventView.as_view({"get": "list"}), name='event_list'),
    path('events/<int:pk>/', views.EventView.as_view({"get": "retrieve"}), name='event_detail'),
    path('tickets/', views.TicketView.as_view(), name='ticket_list'),
    path('reservations/', views.ReservationView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/', views.ReservationView.as_view(), name='reservation_detail'),
    path('reservations/<int:pk>/pay/', views.PaymentView.as_view(), name='payment_view'),
]