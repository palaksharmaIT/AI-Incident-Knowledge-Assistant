from retrieval import retrieve_incidents


def build_context(query):

    # Retrieve similar historical incidents
    results = retrieve_incidents(
        query,
        top_k=5,
        score_threshold=0.7
    )

    if not results:
        return None

    context_parts = []

    for document, score in results:

        context = f"""
Incident ID: {document.metadata["incident_id"]}
Category: {document.metadata["category"]}
Severity: {document.metadata["severity"]}
Service: {document.metadata["service"]}
Similarity Distance: {score}

{document.page_content}
"""

        context_parts.append(context.strip())

    return "\n\n--------------------------\n\n".join(
        context_parts
    )


if __name__ == "__main__":

    query = input(
        "\nEnter incident description:\n> "
    )

    context = build_context(query)

    print("\n================================")
    print("          RAG CONTEXT")
    print("================================")

    if context:
        print(context)
    else:
        print(
            "No sufficiently similar historical "
            "incidents were found."
        )