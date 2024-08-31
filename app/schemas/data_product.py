from pydantic import BaseModel, Field
from typing import List, Optional

class Attribute(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None
    glossary_term: Optional[str] = None

class Port(BaseModel):
    name: str
    attributes: List[Attribute]

class DataLineage(BaseModel):
    upstream_sources: List[str] = Field(..., description="List of upstream data product IDs")
    downstream_targets: List[str] = Field(..., description="List of downstream data product IDs")

class DataProduct(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    owner: str
    input_ports: List[Port]
    output_ports: List[Port]
    lineage: DataLineage
    # Add any other required fields here