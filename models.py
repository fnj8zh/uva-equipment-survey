from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, Literal

class EquipmentSurvey(BaseModel):
    equipment_id: str = Field(..., description="Unique equipment tag or name")
    item_rented: str
    condition: Literal["Excellent", "Good", "Fair", "Poor"] = "Good"
    location: Optional[str] = None
    needs_maintenance: bool = False
    return_date: Optional[date] = None
    usage_purpose: Optional[str] = None
    notes: Optional[str] = None
    image_filename: Optional[str] = None