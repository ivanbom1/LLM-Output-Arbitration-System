from typing import TypedDict, Optional
from schema import CritiqueReportForm


class ArbitrationState(TypedDict):
    question: str
    output_text: str
    accuracy_report: Optional[CritiqueReportForm]
    logic_report: Optional[CritiqueReportForm]
    completeness_report: Optional[CritiqueReportForm]
    disagreements: Optional[list]
    
    # Raw output of the adjudicate node: resolved conflicts, confirmed/dismissed flags, reasoning per disagreement.
    adjudication: Optional[dict]
 
    # Final polished output of synthesize_verdict is what the API actually returns to the person using the system.
    verdict: Optional[dict]