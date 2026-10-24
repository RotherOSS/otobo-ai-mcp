
import rest


def do_unlink_ticket( ticket_id: int, linked_ticket_id: int, link_type: str, sid: str = None, bearer: str = None ) -> dict:

    data = rest.delete_operation(
        "Ticket/" + str(ticket_id) + "/Link/Ticket/" + link_type + "/" + str(linked_ticket_id),
        {},
        sid    = sid,
        bearer = bearer,
    )

    return data

