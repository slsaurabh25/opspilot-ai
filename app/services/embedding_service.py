import math
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def create_embedding(text: str) -> list[float]:
    # 1. Reject blank text.
    if not text.strip():
        raise ValueError("Text cannot be blank.")

    # 2. Call client.embeddings.create(...)
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    # 3. Extract the first embedding from response.data
    return response.data[0].embedding

    # 4. Return the embedding vector.



def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    # Calculate:
    #
    # dot product
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    # magnitude of A
    # magnitude of B
    magnitude_a = math.sqrt(sum(a ** 2 for a in vector_a))
    magnitude_b = math.sqrt(sum(b ** 2 for b in vector_b))
    similarity = dot_product / (magnitude_a * magnitude_b)
    return similarity