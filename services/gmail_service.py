import base64


def get_header(headers, name):

    for header in headers:

        if header["name"].lower() == name.lower():

            return header["value"]

    return ""


def decode_body(data):

    if not data:
        return ""

    try:

        decoded = base64.urlsafe_b64decode(data)

        return decoded.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:

        return ""


def extract_body(payload):

    body = ""

    # Multipart email
    if "parts" in payload:

        for part in payload["parts"]:

            mime_type = part.get("mimeType", "")

            # Plain text
            if mime_type == "text/plain":

                data = part.get("body", {}).get("data")

                if data:

                    body = decode_body(data)

                    if body:
                        return body

            # HTML email
            elif mime_type == "text/html":

                data = part.get("body", {}).get("data")

                if data and not body:

                    body = decode_body(data)

            # Nested parts
            elif "parts" in part:

                nested_body = extract_body(part)

                if nested_body:

                    return nested_body

    else:

        data = payload.get(
            "body",
            {}
        ).get("data")

        if data:

            body = decode_body(data)

    return body


def fetch_emails(service, max_results=20):

    response = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = response.get(
        "messages",
        []
    )

    emails = []

    for message in messages:

        message_id = message["id"]

        email_data = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        payload = email_data.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        sender = get_header(
            headers,
            "From"
        )

        receiver = get_header(
            headers,
            "To"
        )

        subject = get_header(
            headers,
            "Subject"
        )

        date = get_header(
            headers,
            "Date"
        )

        body = extract_body(payload)

        labels = email_data.get(
            "labelIds",
            []
        )

        email = {

            "gmail_message_id": message_id,

            "thread_id": email_data.get(
                "threadId"
            ),

            "sender": sender,

            "receiver": receiver,

            "subject": subject,

            "date": date,

            "body": body,

            "labels": ",".join(labels)

        }

        emails.append(email)

    return emails