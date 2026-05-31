from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import DashboardSummary, ListingRead
from app.services.listing_service import get_dashboard_summary, list_opportunities

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/listings", response_model=list[ListingRead])
def get_listings(db: Session = Depends(get_db)) -> list[ListingRead]:
    return list_opportunities(db)


@router.get("/opportunities", response_model=list[ListingRead])
def get_opportunities(db: Session = Depends(get_db)) -> list[ListingRead]:
    return list_opportunities(db)


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)) -> DashboardSummary:
    return get_dashboard_summary(db)
