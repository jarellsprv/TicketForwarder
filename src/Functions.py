from Config import  CONFIG
from Logger import logger
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email, os, pickle

def process_email(msg):
    for filter_word in CONFIG["FilerWords"]:
        if filter_word in msg.get_payload(decode=True).decode(errors="ignore"):
            logger.info("Found email with filtered words!")
            create_doc(msg)

def check_inbox(mail):
    mail.select("INBOX")

    search_query = ' '.join(f'TEXT "{word}"' for word in CONFIG["FilerWords"])
    search_query = f'({search_query})'

    status, data = mail.search(None, 'UNSEEN', search_query)
    mail_ids = data[0].split()

    for id in mail_ids:
        status, msg_data = mail.fetch(id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        logger.info(f"Processing email ID {id.decode()}")
        create_doc(msg)


def create_doc(ticket_details):

    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/documents'
    ]

    TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.pickle')
    CREDS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                              f"data/input/{CONFIG['GoogleDriveCredentailFileName']}.json")

    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token_file:
            pickle.dump(creds, token_file)

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    file_metadata = {
        'name': 'Forwarded Emails',
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [CONFIG["GoogleDriveFolderId"]]
    }

    file = drive_service.files().create(body=file_metadata).execute()
    file_id = file.get('id')
    logger.suc(f"Document created! File ID: {file_id}")

    sender = ticket_details.get("From", "Unknown Sender")
    logger.info(f"Email from: {sender}")

    if ticket_details.is_multipart():
        text = ""
        for part in ticket_details.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode(errors="ignore")
    else:
        text = ticket_details.get_payload(decode=True).decode(errors="ignore")

    text_to_insert = f"From: {sender}\n\n{text}"

    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': text_to_insert
            }
        }
    ]

    docs_service.documents().batchUpdate(documentId=file_id, body={'requests': requests}).execute()
    logger.suc("Text added to document!")

    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'commenter'}
    ).execute()

    link = f"https://docs.google.com/document/d/{file_id}/edit"
    logger.suc(f"Commentable link: {link}")

