from pydantic import BaseModel
from typing import List, Optional

class Attribute(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None
    glossary_term: Optional[str] = None

class Port(BaseModel):
    name: str
    attributes: List[Attribute]

class DataProduct(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    owner: str
    input_ports: List[Port]
    output_ports: List[Port]
    # Add any other required fields here