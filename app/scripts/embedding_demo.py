from app.services.embedding_service import (create_embedding, cosine_similarity)

text_1 = (
    "Create a P2 incident when certificate expiry "
    "is below seven days."
)

text_2 = (
    "Raise a priority two incident if the SSL "
    "certificate expires within one week."
)

text_3 = (
    "Employees can apply for annual leave through "
    "the HR portal."
)

embedding_1 = create_embedding(text_1)
embedding_2 = create_embedding(text_2)
embedding_3 = create_embedding(text_3)

print(len(embedding_1))
print(embedding_1[:5])

similarity_1_2 = cosine_similarity(
    embedding_1,
    embedding_2,
)

similarity_1_3 = cosine_similarity(
    embedding_1,
    embedding_3,
)

print(f"Certificate vs similar certificate statement: {similarity_1_2}")
print(f"Certificate vs leave-policy statement: {similarity_1_3}")