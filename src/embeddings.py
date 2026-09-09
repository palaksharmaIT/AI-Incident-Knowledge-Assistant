import pandas as pd

from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


# Load processed incidents
df = pd.read_csv("data/processed_incidents.csv")


# Create documents
documents = []

for _, row in df.iterrows():

    content = f"""
Title: {row['title']}

Description: {row['description']}

Root Cause: {row['root_cause']}

Resolution: {row['resolution']}

Severity: {row['severity']}

Service: {row['service']}

Category: {row['category']}
"""

    document = Document(
        page_content=content.strip(),
        metadata={
            "incident_id": row["incident_id"],
            "category": row["category"],
            "severity": row["severity"],
            "service": row["service"]
        }
    )

    documents.append(document)


# Load local embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


class LocalEmbeddings:

    def embed_documents(self, texts):
        return embedding_model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text):
        return embedding_model.encode(
            text,
            normalize_embeddings=True
        ).tolist()


embeddings = LocalEmbeddings()


# Create FAISS vector store
vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# Save FAISS index
vectorstore.save_local(
    "vectorstore/faiss_index"
)


print("Local embeddings created successfully.")
print("Documents embedded:", len(documents))
print("FAISS index saved.")