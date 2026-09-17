import instructor
from openai import OpenAI
from config import GROQ_API_KEY

groq_client = instructor.from_openai(
    OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY),
    mode=instructor.Mode.JSON,
)