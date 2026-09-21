from typing import TypedDict, Optional, Annotated
from schema import CritiqueReportForm
from verdict_schema import AdjudicationResult, Verdict
import operator


class ArbitrationState(TypedDict):
    question: str
    output_text: str
    accuracy_report: Optional[CritiqueReportForm]
    logic_report: Optional[CritiqueReportForm]
    completeness_report: Optional[CritiqueReportForm]
    disagreements: Annotated[list, operator.add] # add list concat to avoid disagreements overwriting 
    
    # Raw output of the adjudicate node: resolved conflicts, confirmed/dismissed flags, reasoning per disagreement.
    adjudication: Optional[AdjudicationResult]
 
    # Final polished output of synthesize_verdict is what the API actually returns to the person using the system.
    verdict: Optional[Verdict]