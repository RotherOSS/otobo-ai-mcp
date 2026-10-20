
import rest


def do_transfer_ticket(ticket_id: int, destination_queue: str, sid: str = None, bearer:str = None) -> dict:

    payload = {
        'Ticket' : {
            "Queue" : destination_queue
        }
    }

    data = rest.put_operation(
        "Ticket/" + str(ticket_id),
        payload,
        sid    = sid,
        bearer = bearer,
    )

    return data

