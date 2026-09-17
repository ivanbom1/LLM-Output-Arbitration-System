import os
from dotenv import load_dotenv
 
load_dotenv()

# Two evaluation-scale presets, for comparing via the drift test in the future

SCALE_5 = {"max_score": 5, "disagreement_gap": 2}
SCALE_10 = {"max_score": 10, "disagreement_gap": 3}

# Switch instance which will be implemented later for testing (hardcoded for now)
ACTIVE_SCALE = SCALE_5