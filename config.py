import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Fallback default if a per-critic model isn't set.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

GROQ_MODEL_ACCURACY = os.environ.get("GROQ_MODEL_ACCURACY", GROQ_MODEL) # key existance check. override to GROQ_MODEL if unset
GROQ_MODEL_LOGIC = os.environ.get("GROQ_MODEL_LOGIC", GROQ_MODEL)
GROQ_MODEL_COMPLETENESS = os.environ.get("GROQ_MODEL_COMPLETENESS", GROQ_MODEL)