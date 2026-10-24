
import rest


def collect_source_ids(raw, source_ids: dict) -> None:

    if isinstance(raw, dict):
        raw = [ raw ]

    for item in raw:
        metadata = item.get("metadata") or {}
        if metadata.get("source_id") is not None:
            source_ids[metadata["source_id"]] = 1


def do_find_similar_tickets( ticket_id: int, article_id: int | None, sid: str = None, bearer: str = None ) -> dict:

    payload = {}

    if article_id is not None:
        payload["ArticleID"] = article_id

    source_ids = {}

    for collection in ("ticket_pairs", "ticket_chunks"):
        raw = rest.get_operation(
            "Ticket/" + str(ticket_id) + "/Embeddings/" + collection,
            payload,
            sid    = sid,
            bearer = bearer,
        )
        collect_source_ids(raw, source_ids)

    return { "similar_tickets" : list(source_ids) }

