import pandas as pd


def save_to_excel(emails, filename="emails_raw.xlsx"):

    if not emails:

        print("No emails to save.")

        return

    df = pd.DataFrame(emails)

    df.to_excel(
        filename,
        index=False
    )

    print(
        f"Emails saved to {filename}"
    )