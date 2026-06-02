from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import (
    CostAssumptionRead, CostAssumptionUpdate,
    DashboardSummary, ModelResearchRead, ModelResearchUpdate,
)
from app.services.listing_service import (
    get_dashboard_summary, get_settings, list_model_research,
    update_model_research, update_settings,
)

router = APIRouter(tags=["admin"])

@router.get("/settings", response_model=CostAssumptionRead)
def get_cost_settings(db: Session = Depends(get_db)):
    return get_settings(db)

@router.patch("/settings", response_model=CostAssumptionRead)
def patch_cost_settings(payload: CostAssumptionUpdate, db: Session = Depends(get_db)):
    return update_settings(db, payload)

@router.get("/model-research", response_model=list[ModelResearchRead])
def get_model_research(db: Session = Depends(get_db)):
    return list_model_research(db)

@router.patch("/model-research/{research_id}", response_model=ModelResearchRead)
def patch_model_research(research_id: int, payload: ModelResearchUpdate, db: Session = Depends(get_db)):
    return update_model_research(db, research_id, payload)

@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
