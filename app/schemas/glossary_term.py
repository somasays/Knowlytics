from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class GlossaryTerm(BaseModel):
    term: str
    definition: str
    domain: str
    category: str
    owner: str
    steward: Optional[str] = None
    status: str
    created_date: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    last_updated: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    version: int
    attributes: Optional[dict] = None
    relationships: Optional[List[dict]] = None
    usage_examples: Optional[List[str]] = None
    notes: Optional[str] = None