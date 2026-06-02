from fastapi import APIRouter, Body, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CsvImportResponse, ListingCreate, ListingRead, ListingUpdate
from app.services.listing_service import (
    create_listing, delete_listing, get_listing,
    import_listings_csv, list_listings, update_listing,
)

router = APIRouter(prefix="/listings", tags=["listings"])

@router.get("", response_model=list[ListingRead])
def get_listings(db: Session = Depends(get_db)):
    return list_listings(db)

@router.post("", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def post_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    return create_listing(db, payload)

@router.post("/import-csv", response_model=CsvImportResponse)
def post_csv(csv_text: str = Body(media_type="text/csv"), db: Session = Depends(get_db)):
    return import_listings_csv(db, csv_text)

@router.get("/{listing_id}", response_model=ListingRead)
def get_listing_detail(listing_id: int, db: Session = Depends(get_db)):
    return get_listing(db, listing_id)

@router.patch("/{listing_id}", response_model=ListingRead)
def patch_listing(listing_id: int, payload: ListingUpdate, db: Session = Depends(get_db)):
    return update_listing(db, listing_id, payload)

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing_endpoint(listing_id: int, db: Session = Depends(get_db)):
    delete_listing(db, listing_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
