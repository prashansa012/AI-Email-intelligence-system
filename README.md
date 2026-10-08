# AI Email Intelligence System

An AI-powered Gmail email intelligence system that securely retrieves emails using the Gmail API, analyzes them using a locally hosted LLM, categorizes emails, generates summaries, identifies priority and action requirements, and stores the processed information in PostgreSQL.

## Features

* Gmail API integration with OAuth 2.0 authentication
* Retrieve email subject, sender, receiver, date, body and labels
* Local LLM-based email classification using Llama 3.2
* Automatic email categorization
* AI-generated email summaries
* Priority detection
* Action-required detection
* PostgreSQL storage for structured email data
* FastAPI REST APIs for email synchronization and retrieval
* Category-based email filtering
* Excel export of processed email data
* Runs locally without requiring paid LLM API credits

## AI Email Categories

The system classifies emails into one of the following categories:

* Job
* Finance
* Shopping
* Travel
* Education
* Social
* Promotions
* Personal
* Important
* Other

## System Architecture

```text
Gmail
   |
   v
Gmail API + OAuth 2.0
   |
   v
Email Extraction
   |
   v
Local LLM - Llama 3.2
   |
   +--> Category
   +--> Summary
   +--> Priority
   +--> Action Required
   |
   v
PostgreSQL
   |
   v
FastAPI REST API
   |
   +--> Retrieve Emails
   +--> Retrieve Email by ID
   +--> Filter by Category
   |
   v
Excel Export
```

## Technologies Used

* Python
* Gmail API
* OAuth 2.0
* Llama 3.2
* Ollama
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pandas
* OpenPyXL
* Requests
* python-dotenv

## Project Structure

```text
mail_data_scraper_AI/
│
├── auth/
│   └── gmail_auth.py
│
├── services/
│   ├── gmail_service.py
│   ├── email_ai.py
│   ├── database.py
│   └── email_repository.py
│
├── exporters/
│   └── excel_exporter.py
│
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd mail_data_scraper_AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gmail API

Create a Google Cloud project and enable the Gmail API.

Create OAuth credentials for a desktop application and download the credentials file.

Save it in the project root as:

```text
credentials.json
```

The credentials file is intentionally excluded from GitHub.

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:3b

DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/email_ai_db
```

### 5. Install and run Ollama

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running locally.

The application uses:

```text
http://localhost:11434/api/generate
```

### 6. Create the PostgreSQL database

Create a database named:

```sql
CREATE DATABASE email_ai_db;
```

Update the PostgreSQL connection string in `.env`.

### 7. Run the FastAPI application

```bash
uvicorn main:app --reload
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Home

```http
GET /
```

Checks whether the API is running.

### Synchronize Emails

```http
POST /sync-emails
```

Authenticates with Gmail, retrieves emails, analyzes them using the local LLM, stores the results in PostgreSQL and exports processed data to Excel.

### Get All Emails

```http
GET /emails
```

Returns processed emails stored in PostgreSQL.

### Get Email by ID

```http
GET /emails/{email_id}
```

Returns a specific processed email.

### Get Emails by Category

```http
GET /emails/category/{category}
```

Example:

```text
GET /emails/category/Education
```

## AI Output

For each email, the system generates structured information such as:

```json
{
    "category": "Job",
    "summary": "Interview invitation for an AI/ML Engineer position.",
    "priority": "High",
    "action_required": true
}
```

## Security

Sensitive files are excluded from version control:

```text
.env
credentials.json
token.json
```

The application is intended to run locally and requires the user's explicit Gmail OAuth authorization to access email data.

## Future Improvements

* Improved HTML email cleaning
* Better handling of long emails
* Semantic email search
* Duplicate detection
* Attachment metadata extraction
* Dashboard for email analytics
* Background email synchronization
* More advanced LLM-based insights
