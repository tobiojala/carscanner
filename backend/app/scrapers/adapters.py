from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    brand: str | None = None
    model: str | None = None
    seller_country: str = "DE"
    source: str | None = None
    max_results: int = Field(default=25, ge=1, le=100)


class RawListing(BaseModel):
    source: str
    source_listing_id: str
    listing_url: str | None = None
    payload: dict[str, Any]


class NormalizedListing(BaseModel):
    source: str
    source_listing_id: str
    listing_url: str | None = None
    seller_country: str = "DE"
    seller_type: str = "dealer"
    brand: str
    model: str
    variant: str | None = None
    trim: str | None = None
    year: int
    mileage_km: int
    fuel_type: str | None = None
    transmission: str | None = None
    price_eur: float
    currency: str = "EUR"


class RawListingDetail(RawListing):
    description: str | None = None
    image_urls: list[str] = Field(default_factory=list)


class MarketplaceAdapter(ABC):
    source_name: str

    @abstractmethod
    def search_listings(self, query: SearchQuery) -> list[RawListing]:
        raise NotImplementedError

    @abstractmethod
    def parse_listing(self, raw: RawListing) -> NormalizedListing:
        raise NotImplementedError

    @abstractmethod
    def get_listing_detail(self, url: str) -> RawListingDetail:
        raise NotImplementedError


class MockMarketplaceAdapter(MarketplaceAdapter):
    def __init__(self, source_name: str) -> None:
        self.source_name = source_name

    def search_listings(self, query: SearchQuery) -> list[RawListing]:
        return []

    def parse_listing(self, raw: RawListing) -> NormalizedListing:
        return NormalizedListing(**raw.payload)

    def get_listing_detail(self, url: str) -> RawListingDetail:
        return RawListingDetail(
            source=self.source_name,
            source_listing_id="mock-detail",
            listing_url=url,
            payload={},
            description="Mock adapter detail placeholder. Real scraping is Phase 3.",
            image_urls=[],
        )


class MobileDeAdapter(MockMarketplaceAdapter):
    def __init__(self) -> None:
        super().__init__("mobile.de")


class AutoScout24Adapter(MockMarketplaceAdapter):
    def __init__(self) -> None:
        super().__init__("AutoScout24")


class BlocketAdapter(MockMarketplaceAdapter):
    def __init__(self) -> None:
        super().__init__("Blocket")


class BytbilAdapter(MockMarketplaceAdapter):
    def __init__(self) -> None:
        super().__init__("Bytbil")
