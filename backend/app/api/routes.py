from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import (
    ComparableCreate,
    ComparableRead,
    ModelResearchUpdate,
    ModelResearchRead,
    DealStatusUpdate,
    CostAssumptionUpdate,
    CostAssumptionRead,
    DashboardSummary,
    DealCalculateRequest,
    DealDetailRead,
    DealOpportunityRead,
    ListingCreate,
    ListingRead,
    ListingUpdate,
)
from app.services.listing_service import (
    calculate_deal,
    create_comparable,
    create_listing,
    delete_listing,
    get_dashboard_summary,
    get_deal_detail,
    get_listing,
    update_settings,
    update_model_research,
    update_deal_status,
    list_model_research,
    get_settings,
    list_comparables,
    list_listings,
    list_opportunities,
    update_listing,
)

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/listings", response_model=list[ListingRead])
def get_listings(db: Session = Depends(get_db)) -> list[ListingRead]:
    return list_listings(db)


@router.post("/listings", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def post_listing(payload: ListingCreate, db: Session = Depends(get_db)) -> ListingRead:
    return create_listing(db, payload)


@router.get("/listings/{listing_id}", response_model=ListingRead)
def get_listing_detail(listing_id: int, db: Session = Depends(get_db)) -> ListingRead:
    return get_listing(db, listing_id)


@router.patch("/listings/{listing_id}", response_model=ListingRead)
def patch_listing(
    listing_id: int,
    payload: ListingUpdate,
    db: Session = Depends(get_db),
) -> ListingRead:
    return update_listing(db, listing_id, payload)


@router.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing_endpoint(listing_id: int, db: Session = Depends(get_db)) -> Response:
    delete_listing(db, listing_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/comparables", response_model=list[ComparableRead])
def get_comparables(db: Session = Depends(get_db)) -> list[ComparableRead]:
    return list_comparables(db)


@router.post(
    "/comparables",
    response_model=ComparableRead,
    status_code=status.HTTP_201_CREATED,
)
def post_comparable(
    payload: ComparableCreate,
    db: Session = Depends(get_db),
) -> ComparableRead:
    return create_comparable(db, payload)


@router.get("/opportunities", response_model=list[DealOpportunityRead])
def get_opportunities(
    model: str | None = None,
    min_profit_sek: float | None = None,
    min_confidence: int | None = None,
    source: str | None = None,
    seller_type: str | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
) -> list[DealOpportunityRead]:
    return list_opportunities(
        db,
        model=model,
        min_profit_sek=min_profit_sek,
        min_confidence=min_confidence,
        source=source,
        seller_type=seller_type,
        fuel_type=fuel_type,
        transmission=transmission,
        status_filter=status_filter,
    )


@router.post("/deals/calculate", response_model=DealOpportunityRead)
def post_deal_calculation(
    payload: DealCalculateRequest,
    db: Session = Depends(get_db),
) -> DealOpportunityRead:
    return calculate_deal(db, payload)


@router.get("/deals/{deal_id}", response_model=DealDetailRead)
def get_deal_detail_endpoint(
    deal_id: int,
    db: Session = Depends(get_db),
) -> DealDetailRead:
    return get_deal_detail(db, deal_id)


@router.patch("/deals/{deal_id}/status", response_model=DealOpportunityRead)
def patch_deal_status(
    deal_id: int,
    payload: DealStatusUpdate,
    db: Session = Depends(get_db),
) -> DealOpportunityRead:
    return update_deal_status(db, deal_id, payload)


@router.get("/settings", response_model=CostAssumptionRead)
def get_cost_settings(db: Session = Depends(get_db)) -> CostAssumptionRead:
    return get_settings(db)


@router.patch("/settings", response_model=CostAssumptionRead)
def patch_cost_settings(
    payload: CostAssumptionUpdate,
    db: Session = Depends(get_db),
) -> CostAssumptionRead:
    return update_settings(db, payload)


@router.get("/model-research", response_model=list[ModelResearchRead])
def get_model_research(db: Session = Depends(get_db)) -> list[ModelResearchRead]:
    return list_model_research(db)


@router.patch("/model-research/{research_id}", response_model=ModelResearchRead)
def patch_model_research(
    research_id: int,
    payload: ModelResearchUpdate,
    db: Session = Depends(get_db),
) -> ModelResearchRead:
    return update_model_research(db, research_id, payload)


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)) -> DashboardSummary:
    return get_dashboard_summary(db)
