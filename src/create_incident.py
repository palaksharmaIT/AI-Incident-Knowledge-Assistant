from database import SessionLocal, Incident


session = SessionLocal()

incident = Incident(
    incident_id="INC021",
    title="Payment API Failure",
    description="Payment requests are failing with HTTP 500 errors",
    severity="High",
    service="Payment API",
    status="Open"
)

session.add(incident)
session.commit()

print("New incident created successfully.")
print("Incident ID:", incident.incident_id)

session.close()