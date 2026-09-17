from enum import Enum
from pydantic import BaseModel, Field

class Dimension(str, Enum): # Specifies which exact critique produced a report 
    ACCURACY = "accuracy"
    LOGIC = "logic"
    COMPLETENESS = "completeness"
    
class SeverityLevel(int, Enum): # Classification of an Issue. Each one has a different level depended on the specific problem
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
class Issue(BaseModel): #Issue Object, has a problematic part reference, explanation and class of the issue
    quote: str = Field(..., description="Problem part from the original output") 
    problem: str = Field(..., description="What's the issue")
    Severity: SeverityLevel

class CritiqueReportForm(BaseModel): 
    dimension: Dimension
    eval_score: int = Field(...,  ge=1, le=5)
    issues: list[Issue]
    confidence: float = Field(..., ge=0, le=1)