from pydantic import BaseModel
from typing import Optional

class PantryItemCreate(BaseModel):
    name: str
    quantity: Optional[float] = 1
    unit: Optional[str] = None
    purchase_date: Optional[str] = None
    estimated_expiry_date: Optional[str] = None
    image_ref: Optional[str] = None
    barcode: Optional[str] = None
