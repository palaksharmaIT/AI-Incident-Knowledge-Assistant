from database import SessionLocal, Incident
from rag import build_context


session = SessionLocal()

incident = (
    session.query(Incident)
    .filter_by(status="Open")
    .order_by(Incident.id.desc())
    .first()
)

if not incident:
    print("No open incidents found.")

else:
    query = (
        incident.title + " "
        + incident.description
    )

    print("\n================================")
    print("       INCIDENT RETRIEVAL")
    print("================================")

    print("Incident:", incident.incident_id)
    print("Category:", incident.category)

    context = build_context(query)

    if context:
        print("\n===== SIMILAR HISTORICAL INCIDENTS =====")
        print(context)
    else:
        print("\nNo similar historical incidents found.")


session.close()