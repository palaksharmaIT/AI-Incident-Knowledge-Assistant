import pandas as pd

from database import SessionLocal, Incident


# Load historical incidents
df = pd.read_csv("data/incidents.csv")

session = SessionLocal()

added = 0
skipped = 0

for _, row in df.iterrows():

    # Check if incident already exists
    existing = session.query(Incident).filter_by(
        incident_id=row["incident_id"]
    ).first()

    if existing:
        skipped += 1
        continue

    incident = Incident(
        incident_id=row["incident_id"],
        title=row["title"],
        description=row["description"],
        severity=row["severity"],
        service=row["service"],
        category=row["category"],
        root_cause=row["root_cause"],
        resolution=row["resolution"],
        status="Resolved"
    )

    session.add(incident)
    added += 1


session.commit()
session.close()

print(f"Incidents added: {added}")
print(f"Incidents skipped: {skipped}")
print("Database seeding completed.")