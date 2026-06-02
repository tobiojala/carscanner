from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import (
    ActualOutcomeUpdate, DealCalculateRequest,
    DealDetailRead, DealOpportunityRead, DealStatusUpdate,
)
from app.services.listing_service import (
    calculate_deal, get_deal_detail, list_opportunities,
    update_actual_outcome, update_deal_status,
)

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("", response_model=list[DealOpportunityRead])
def get_opportunities(
    model: str | None = None, min_profit_sek: float | None = None,
    min_confidence: int | None = None, source: str | None = None,
    seller_type: str | None = None, fuel_type: str | None = None,
    transmission: str | None = None, status_filter: str | None = None,
    db: Session = Depends(get_db),
):
    return list_opportunities(
        db, model=model, min_profit_sek=min_profit_sek,
        min_confidence=min_confidence, source=source,
        seller_type=seller_type, fuel_type=fuel_type,
        transmission=transmission, status_filter=status_filter,
    )

@router.post("/calculate", response_model=DealOpportunityRead)
def post_deal_calculation(payload: DealCalculateRequest, db: Session = Depends(get_db)):
    return calculate_deal(db, payload)

@router.get("/{deal_id}", response_model=DealDetailRead)
def get_deal_detail_endpoint(deal_id: int, db: Session = Depends(get_db)):
    return get_deal_detail(db, deal_id)

@router.patch("/{deal_id}/status", response_model=DealOpportunityRead)
def patch_deal_status(deal_id: int, payload: DealStatusUpdate, db: Session = Depends(get_db)):
    return update_deal_status(db, deal_id, payload)

@router.patch("/{deal_id}/actual-outcome", response_model=DealDetailRead)
def patch_actual_outcome(deal_id: int, payload: ActualOutcomeUpdate, db: Session = Depends(get_db)):
    return update_actual_outcome(db, deal_id, payload)
