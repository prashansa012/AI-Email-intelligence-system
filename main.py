from fastapi import FastAPI
from fastapi import HTTPException

from auth.gmail_auth import authenticate_gmail

from services.gmail_service import fetch_emails

from services.email_ai import analyze_email

from services.database import Base
from services.database import engine
from services.database import SessionLocal

from services.email_repository import Email
from services.email_repository import save_email

from exporters.excel_exporter import save_to_excel


app = FastAPI(
    title="AI Email Intelligence API",
    description="AI-powered Gmail email classification and analysis system"
)


# Create PostgreSQL tables
Base.metadata.create_all(
    bind=engine
)


@app.get("/")
def home():

    return {
        "message": "AI Email Intelligence API is running"
    }


@app.post("/sync-emails")
def sync_emails():

    service = authenticate_gmail()

    emails = fetch_emails(
        service,
        max_results=3
    )

    processed = 0

    processed_emails = []

    for email in emails:

        ai_result = analyze_email(
            email["subject"],
            email["body"]
        )

        save_email(
            email,
            ai_result
        )

        email_with_ai = email.copy()

        email_with_ai.update(
            ai_result
        )

        processed_emails.append(
            email_with_ai
        )

        processed += 1

    save_to_excel(
        processed_emails,
        "emails_processed.xlsx"
    )

    return {
        "message": "Emails processed successfully",
        "count": processed
    }

@app.get("/emails")
def get_emails():

    db = SessionLocal()

    try:

        emails = db.query(
            Email
        ).all()

        return emails

    finally:

        db.close()


@app.get("/emails/{email_id}")
def get_email(email_id: int):

    db = SessionLocal()

    try:

        email = db.query(
            Email
        ).filter(
            Email.id == email_id
        ).first()

        if not email:

            raise HTTPException(
                status_code=404,
                detail="Email not found"
            )

        return email

    finally:

        db.close()


@app.get("/emails/category/{category}")
def get_emails_by_category(
    category: str
):

    db = SessionLocal()

    try:

        emails = db.query(
            Email
        ).filter(
            Email.category == category
        ).all()

        return emails

    finally:

        db.close()