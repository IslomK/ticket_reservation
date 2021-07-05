##Ticket reservation system MVP.

Little bit about the system. 

There are events model. Each event have its name and the date when it should be. 
In addition to this, event has multiple type of tickets - VIP, Premium, Regular. Tickets were separated from events, so by this way different type of the tickets can be created with different price and quantity. 

Client reserves a ticket, which has a particular event (foreign key relationship). After reservation was created, its status is NOT_PAID, and after this it should be paid by client. If no payment was made, status automatically changes to CANCELLED. Payment made through the payment gateway presented by 3rd authority. When payment is successfully made, transaction is created with corresponding details.

###Get events list
```
GET /v1/events/
```

Response

```
{[
    {
        "id": 1,
        "name": "big event",
        "datetime": "2015-12-12 15:00",
        "ticket_types": {
            "premium": "true",
            "regular": "false",
            "vip": "false"
        },
        
    },
]}
```

###Get event detail

```
GET /v1/event/<int:event_id>/
```

Response:
```
{
    "id": 1,
    "name": "big event",
    "datetime": "2015-12-12 15:00",
    "ticket_types": {
        "premium": "true",
        "regular": "false",
        "vip": "false"
    }
}
```

###Get tickets list 
```
GET /v1/tickets/
```

Query params to filter:
* price_from
* price_to
* ticket_type
* event_id
* available

Response:
```
{[
    "quantity": 300,
    "ticket_type": "VIP",
    "price": 300,
    "available": True,
    "event": {
        "id": 1,
        "name": "Big event",
        "date": "2015-12-12 15:00"
    },
]}
```

###Get reservations list
```
GET /v1/reservations/
```

Query params to filter:
* event_id 
* ticket_id 
* client_id 

Response:
```
{[
    {
        "id": 12,
        "created_at": "2015-12-12 15:00"
        "ticket": {
            "id": 1,
            "type": "VIP",
            "price": 300
        },
        "client": {
            "id": 22,
            "first_name": "Islom",
            "last_name": "Karimov"
        },
        "status": "NOT_PAID",
        "total_price": 12220
    }

]}
```

###Create reservation

```
POST /v1/reservations/
```

Data to be passed in the body:
* `ticket_id` - int
* `client_id` - int
* `quantity` - int

Response:
```
{
    "status": "success"
}
```

###Payment

```
POST /v1/reservations/<int:id>/pay/
```
Data to be passed in the body:
* `total_cost` - int
* `currency` - char 

Response:

```
{
    "status": "success"
}
```

###Get reservation detail
```
GET /v1/reservation/<int:id>/
```

Response:

```
{
        "id": 12,
        "created_at": "2015-12-12 15:00"
        "ticket": {
            "id": 1,
            "type": "VIP",
            "price": 300
        },
        "client": {
            "id": 22,
            "first_name": "Islom",
            "last_name": "Karimov"
        },
        "status": "NOT_PAID",
        "total_price": 12220
}
```

##Tests

All the tests are created in the `api.tests` module.
In order to run the tests:

```
python manage.py test api.tests --keepdb 
```

Reservation status changes after 15 minutes of its creation - if during this time it is not paid, it goes cancelled. The cancellation is done with CELERY TASKS.

In order to run tasks, first of all redis should be installed.
```
sudo apt-get install redis-server
celery -A monterail worker
```
