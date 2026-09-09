from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime


DATABASE_URL = "sqlite:///data/incidents.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()


class Incident(Base):

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    incident_id = Column(
        String(20),
        unique=True,
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    severity = Column(
        String(50),
        nullable=False
    )

    service = Column(
        String(100),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=True
    )

    root_cause = Column(
        Text,
        nullable=True
    )

    resolution = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        default="Open"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )


# Create database tables
Base.metadata.create_all(engine)


print("Database initialized successfully.")