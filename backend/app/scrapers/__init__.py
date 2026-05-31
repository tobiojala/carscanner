"""Placeholder importer and scraper adapter package.

Real marketplace scraping is intentionally out of scope for Phase 2.
"""

from app.scrapers.adapters import (
    AutoScout24Adapter,
    BlocketAdapter,
    BytbilAdapter,
    MarketplaceAdapter,
    MobileDeAdapter,
    NormalizedListing,
    RawListing,
    RawListingDetail,
    SearchQuery,
)

__all__ = [
    "AutoScout24Adapter",
    "BlocketAdapter",
    "BytbilAdapter",
    "MarketplaceAdapter",
    "MobileDeAdapter",
    "NormalizedListing",
    "RawListing",
    "RawListingDetail",
    "SearchQuery",
]
