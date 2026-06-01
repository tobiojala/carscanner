from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, Field


class LinkIntakeRequest(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=100)


class LinkIntakeItem(BaseModel):
    url: str
    source: str
    link_type: str
    source_listing_id: str | None
    seller_country: str | None
    notes: list[str]


class LinkIntakeResponse(BaseModel):
    items: list[LinkIntakeItem]


def _detect_source(hostname: str) -> str:
    if "mobile.de" in hostname:
        return "mobile.de"
    if "autoscout24" in hostname:
        return "AutoScout24"
    if "blocket" in hostname:
        return "Blocket"
    if "bytbil" in hostname:
        return "Bytbil"
    return "unknown"


def _detect_link_type(path: str, query_params: dict[str, list[str]]) -> str:
    lower_path = path.lower()
    if "search" in lower_path or "search" in query_params or "issearchrequest" in query_params:
        return "search"
    if "details" in lower_path or "id" in query_params:
        return "listing"
    if any(segment in lower_path for segment in ["/annons", "/objekt", "/bil/"]):
        return "listing"
    return "unknown"


def _source_listing_id(source: str, path: str, query_params: dict[str, list[str]]) -> str | None:
    if source == "mobile.de" and query_params.get("id"):
        return query_params["id"][0]
    if source == "AutoScout24" and query_params.get("id"):
        return query_params["id"][0]

    path_parts = [part for part in path.split("/") if part]
    if path_parts and any(char.isdigit() for char in path_parts[-1]):
        return path_parts[-1]
    return None


def _seller_country(source: str, query_params: dict[str, list[str]]) -> str | None:
    # mobile.de search URLs often omit country unless explicitly filtered. The
    # MVP starts with Germany, so leave this as a hint rather than a hard value.
    country_values = query_params.get("cn") or query_params.get("country")
    if country_values:
        return country_values[0].upper()
    if source in {"mobile.de", "AutoScout24"}:
        return "DE?"
    if source in {"Blocket", "Bytbil"}:
        return "SE"
    return None


def parse_marketplace_link(url: str) -> LinkIntakeItem:
    parsed = urlparse(url.strip())
    hostname = (parsed.hostname or "").lower()
    query_params = {key.lower(): value for key, value in parse_qs(parsed.query).items()}
    source = _detect_source(hostname)
    link_type = _detect_link_type(parsed.path, query_params)
    notes: list[str] = []

    if source == "unknown":
        notes.append("Unknown marketplace. Keep it as a reference link.")
    if link_type == "search":
        notes.append("Search URL: use it to find candidates, then open an individual listing for manual input.")
    elif link_type == "listing":
        notes.append("Listing URL: suitable for manual input after copying price, mileage, year, and trim.")
    else:
        notes.append("Could not tell if this is a search or listing URL.")

    if source == "mobile.de" and query_params.get("ms"):
        notes.append("mobile.de model filter detected; verify brand/model manually before saving.")
    if query_params.get("dam") == ["false"] or query_params.get("damaged") == ["false"]:
        notes.append("Damage filter appears to exclude damaged vehicles.")

    return LinkIntakeItem(
        url=url.strip(),
        source=source,
        link_type=link_type,
        source_listing_id=_source_listing_id(source, parsed.path, query_params),
        seller_country=_seller_country(source, query_params),
        notes=notes,
    )


def preview_links(payload: LinkIntakeRequest) -> LinkIntakeResponse:
    return LinkIntakeResponse(
        items=[parse_marketplace_link(url) for url in payload.urls if url.strip()]
    )
