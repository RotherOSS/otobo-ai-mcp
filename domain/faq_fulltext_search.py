
import otobo
import rest


def do_faq_fulltext_search( search_term: str, limit: int, sid: str = None, bearer: str = None) -> list[dict]:

    payload = {
        'Fulltext'     : search_term,
        "Limit"        : limit
    }

    data = rest.get_operation(
        "FAQ",
        payload,
        sid    = sid,
        bearer = bearer,
    )

    data = data.get("faq") or []

    if isinstance(data,dict):
        data = [ data ]

    for item in data:

        if item.get("faq_id") is not None:
            item["url"] = otobo.settings.faq_url(item["faq_id"])

    return data

