from services.database import SessionLocal
from services.database import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean


class Email(Base):

    __tablename__ = "emails"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    gmail_message_id = Column(
        String(255),
        unique=True,
        index=True
    )

    thread_id = Column(
        String(255)
    )

    sender = Column(
        String(500)
    )

    receiver = Column(
        String(500)
    )

    subject = Column(
        Text
    )

    body = Column(
        Text
    )

    received_at = Column(
        String(255)
    )

    labels = Column(
        Text
    )

    category = Column(
        String(100)
    )

    summary = Column(
        Text
    )

    priority = Column(
        String(50)
    )

    action_required = Column(
        Boolean
    )


def save_email(email_data, ai_data):

    db = SessionLocal()

    try:

        # Check if email already exists
        existing = db.query(
            Email
        ).filter(
            Email.gmail_message_id
            == email_data["gmail_message_id"]
        ).first()

        if existing:

            return existing

        email = Email(

            gmail_message_id=
            email_data["gmail_message_id"],

            thread_id=
            email_data.get("thread_id"),

            sender=
            email_data["sender"],

            receiver=
            email_data["receiver"],

            subject=
            email_data["subject"],

            body=
            email_data["body"],

            received_at=
            email_data["date"],

            labels=
            email_data.get("labels", ""),

            category=
            ai_data["category"],

            summary=
            ai_data["summary"],

            priority=
            ai_data["priority"],

            action_required=
            ai_data["action_required"]
        )

        db.add(email)

        db.commit()

        db.refresh(email)

        return email

    finally:

        db.close()