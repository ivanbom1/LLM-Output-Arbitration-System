from enum import Enum
from pydantic import BaseModel, Field

class Dimension(str, Enum):
    ACCURACY = "accuracy"
    LOGIC = "logic"
    COMPLETENESS = "completeness"
    
class Severity(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
class Issue(BaseModel):
    quote: str = Field(..., description="Problem part from the original output")
    problem: str = Field(..., description="What's the issue")
    Severity: Severity
    