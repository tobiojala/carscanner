from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ComparableCreate, ComparableRead
from app.services.listing_service import create_comparable, list_comparables

router = APIRouter(prefix="/comparables", tags=["comparables"])

@router.get("", response_model=list[ComparableRead])
def get_comparables(db: Session = Depends(get_db)):
    return list_comparables(db)

@router.post("", response_model=ComparableRead, status_code=status.HTTP_201_CREATED)
def post_comparable(payload: ComparableCreate, db: Session = Depends(get_db)):
    return create_comparable(db, payload)
