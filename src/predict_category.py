import joblib

from database import SessionLocal, Incident


# Load trained ML model
model = joblib.load(
    "models/incident_classifier.pkl"
)


session = SessionLocal()


# Get the latest open incident
incident = (
    session.query(Incident)
    .filter_by(status="Open")
    .order_by(Incident.id.desc())
    .first()
)


if not incident:
    print("No open incidents found.")
else:

    # Combine incident information
    text = (
        incident.title + " "
        + incident.description
    )

    # Predict category
    predicted_category = model.predict([text])[0]

    # Update database
    incident.category = predicted_category

    session.commit()

    print("Category predicted successfully.")
    print("Incident:", incident.incident_id)
    print("Predicted Category:", predicted_category)


session.close()