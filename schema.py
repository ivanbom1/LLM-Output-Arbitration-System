from enum import Enum
from pydantic import BaseModel, Field
from eval_options import ACTIVE_SCALE

class Dimension(str, Enum): # Specifies which exact critique produced a report 
    ACCURACY = "accuracy"
    LOGIC = "logic"
    COMPLETENESS = "completeness"
    
class SeverityLevel(int, Enum): # Classification of an Issue. Each one has a different level depended on the specific problem
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Issue(BaseModel): #Issue Object, has a problematic part reference, explanation and class of the issue
    quote: str = Field(..., description="Exact snippet from the original output")
    problem: str = Field(..., description="What's wrong with it")
    severity: SeverityLevel
    missing_aspect: str | None = Field(
        None,
        description="For completeness gaps only: the part of the question that went unanswered. "
                    "Leave null for accuracy/logic issues, which quote the output directly instead.",
    )

class CritiqueReportForm(BaseModel): 
    dimension: Dimension
    score: int = Field(..., ge=1, le=ACTIVE_SCALE["max_score"])
    issues: list[Issue]
    confidence: float = Field(..., ge=0, le=1)