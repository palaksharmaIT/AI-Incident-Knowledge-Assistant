from sentence_transformers import SentenceTransformer

from langchain_community.vectorstores import FAISS


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

    def __call__(self, text):
        return self.embed_query(text)


# Create embedding object
embeddings = LocalEmbeddings()


# Load FAISS index
vectorstore = FAISS.load_local(
    "vectorstore/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


def retrieve_incidents(
    query,
    top_k=5,
    score_threshold=0.7
):

    results = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )

    filtered_results = []

    for document, score in results:

        print("\nIncident:", document.metadata["incident_id"])
        print("Category:", document.metadata["category"])
        print("Distance:", score)

        # Lower FAISS distance = more similar
        if score <= score_threshold:
            filtered_results.append(
                (document, score)
            )

    # Rank by similarity
    filtered_results.sort(
        key=lambda x: x[1]
    )

    return filtered_results


if __name__ == "__main__":

    query = input("\nEnter incident description: ")

    results = retrieve_incidents(
        query,
        top_k=5,
        score_threshold=0.7
    )

    print("\n===== RETRIEVED INCIDENTS =====")

    for document, score in results:

        print("\n--------------------------")

        print(
            "Incident ID:",
            document.metadata["incident_id"]
        )

        print(
            "Category:",
            document.metadata["category"]
        )

        print(
            "Severity:",
            document.metadata["severity"]
        )

        print(
            "Service:",
            document.metadata["service"]
        )

        print(
            "Distance:",
            score
        )

        print("\nContent:")
        print(document.page_content)