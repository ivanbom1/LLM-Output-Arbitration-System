from pydantic import BaseModel, Field

from schema import Dimension, SeverityLevel


class ConfirmendIssue(BaseModel):
    source_critic: Dimension
    problem: str = Field(..., description="What's wrong from the adjudicator's perspective")
    severity: SeverityLevel
    evidence: str = Field(..., description="The adjudicator's reasoning for issue confirmation")
    
class DismissedFlag(BaseModel):
    source_critic: Dimension
    original_problem: str = Field(..., description="What the critic originally flagged")
    reasoning: str = Field(..., description="Why the adjudicator overruled it")
    
class AdjudicationResult(BaseModel):
    confirmed_issues: list[ConfirmendIssue]
    dismissed_flags: list[DismissedFlag]
    
class Verdict(BaseModel):
    overall_score: int = Field(..., ge=1, le=10)
    confidence: float = Field(..., ge=0, le=1)
    confirmed_issues: list[ConfirmendIssue]
    dismissed_flags: list[DismissedFlag]
    summary: str = Field(..., description="One paragraph plain-language assessment")
    