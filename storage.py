from pydantic import BaseModel, Field
from typing import Optional, Literal

class EquipmentSurvey(BaseModel):
    equipment_id: str = Field(..., description="Unique equipment tag or name")
    condition: Literal["Excellent", "Good", "Fair", "Poor"] = Field(
        "Good", description="Condition of the equipment"
    )
    location: Optional[str] = Field(None, description="Where the equipment is located")
    needs_maintenance: bool = Field(False, description="Does the equipment need maintenance?")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes about the equipment")

    image_filename: Optional[str] = Field(
        None,
        description="Saved filename of the uploaded item image"
    )

    class Config:
        schema_extra = {
            "example": {
                "equipment_id": "Laptop-123",
                "condition": "Good",
                "location": "Lab A",
                "needs_maintenance": False,
                "notes": "Works fine",
                "image_filename": "Laptop-123_2025-02-14T19-22-33.jpg"
            }
        }

import json
from pathlib import Path

DATAFILE = Path("data/equipment.ndjson")
DATAFILE.parent.mkdir(exist_ok=True)

def append_record(record: dict):
    with open(DATAFILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def load_all_records():
    if not DATAFILE.exists():
        return []
    with open(DATAFILE, "r") as f:
        return [json.loads(line) for line in f]
