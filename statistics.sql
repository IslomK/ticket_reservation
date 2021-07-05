select api_event.name, sum(ar.quantity) from api_event
left join api_ticket a on api_event.id = a.event_id
left outer join api_reservation ar on a.id = ar.ticket_id
where ar.status = 'paid'
group by api_event.name;

select a.ticket_type, COALESCE(sum(ar.quantity), 0) as sold_amount from api_event
left join api_ticket a on api_event.id = a.event_id
left outer join api_reservation ar on a.id = ar.ticket_id
where ar.status = 'paid'
group by a.ticket_type;
