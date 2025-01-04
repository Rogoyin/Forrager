
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64

def Authenticate_Gmail() -> 'googleapiclient.discovery.Resource': # type: ignore
    
    """
    Authenticates and creates a service object to interact with the Gmail API.

    Returns:
        googleapiclient.discovery.Resource: The service object for Gmail API.
    """

    # Define the scope for the API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    Creds = None
    # Check if token.json exists and is valid
    if os.path.exists('A:/Descargas/token.json'):
        Creds = Credentials.from_authorized_user_file('A:/Descargas/token.json', SCOPES)

    # If no credentials are available or the credentials are invalid, ask the user to log in
    if not Creds or not Creds.valid:
        if Creds and Creds.expired and Creds.refresh_token:
            Creds.refresh(Request())
        else:
            # Use the credentials.json for the OAuth flow
            Flow = InstalledAppFlow.from_client_secrets_file(
                'A:/Descargas/credentials.json', SCOPES)  # Change 'credentials.json' to the correct file path
            Creds = Flow.run_local_server(port=0)

        # Save the credentials for the next time the script is run
        with open('A:/Descargas/token.json', 'w') as Token:
            Token.write(Creds.to_json())
    
    # Build the Gmail service.
    Service = build('gmail', 'v1', credentials=Creds)
    return Service

def Send_Email(Service: 'googleapiclient.discovery.Resource', Drive_Service: 'googleapiclient.discovery.Resource',  # type: ignore
               Sender: str, To: str, Subject: str, Body: str, File_Paths: list = []) -> None:
    
    """
    Sends an email using the Gmail API, with multiple optional attachments.
    Handles large files (>25 MB) by uploading them to Google Drive and adding download links in the email body.

    Args:
        Service (googleapiclient.discovery.Resource): The Gmail API service object.
        Drive_Service (googleapiclient.discovery.Resource): The Google Drive API service object.
        Sender (str): The email address of the sender.
        To (str): The email address of the recipient.
        Subject (str): The subject of the email.
        Body (str): The body content of the email.
        File_Paths (list, optional): A list of file paths to be attached. Default is None.
        
    """

    try:
        # Create the email message.
        Message = MIMEMultipart()
        Message['to'] = To
        Message['subject'] = Subject
        Msg = MIMEText(Body)
        Message.attach(Msg)

        # List to store Google Drive links for large files.
        Large_File_Links = []

        # Attach files or upload large files to Drive.
        if len(File_Paths) > 0:
            for File_Path in File_Paths:
                File_Size = os.path.getsize(File_Path)
                if File_Size > 25 * 1024 * 1024:  # File size exceeds 25 MB.
                    print(f"File '{os.path.basename(File_Path)}' exceeds 25 MB. Uploading to Google Drive...")
                    
                    # Upload file to Google Drive.
                    File_Metadata = {'name': os.path.basename(File_Path)}
                    Media = MediaFileUpload(File_Path, mimetype='application/octet-stream')
                    Uploaded_File = Drive_Service.files().create(body=File_Metadata, media_body=Media, fields='id, webViewLink').execute()
                    
                    # Get the link and add it to the email body.
                    File_Link = Uploaded_File.get('webViewLink')
                    Large_File_Links.append(f"{os.path.basename(File_Path)}: {File_Link}")
                else:
                    # Attach files smaller than 25 MB.
                    with open(File_Path, 'rb') as Attachment:
                        Part = MIMEBase('application', 'octet-stream')
                        Part.set_payload(Attachment.read())
                        encoders.encode_base64(Part)
                        Part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(File_Path)}')
                        Message.attach(Part)

        # Add links for large files to the email body.
        if Large_File_Links:
            Body += "\n\nLinks to large files:\n" + "\n".join(Large_File_Links)
            Message.attach(MIMEText(Body, 'plain'))

        # Convert the message to raw format.
        Raw_Message = base64.urlsafe_b64encode(Message.as_bytes()).decode('utf-8')

        # Send the message.
        Send_Message = Service.users().messages().send(userId="me", body={'raw': Raw_Message}).execute()
        print(f'Message sent: {Send_Message["id"]}')
    except HttpError as Error:
        print(f'An error occurred: {Error}')

def Authenticate_Drive():

    # Autenticar en Drive.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/drive.file']
    
    Creds = None
    if os.path.exists('A:/Descargas/token.json'):
        Creds = Credentials.from_authorized_user_file('A:/Descargas/token.json', SCOPES)
    if not Creds or not Creds.valid:
        if Creds and Creds.expired and Creds.refresh_token:
            Creds.refresh(Request())
        else:
            Flow = InstalledAppFlow.from_client_secrets_file('A:/Descargas/credentials.json', SCOPES)
            Creds = Flow.run_local_server(port=0)
        with open('A:/Descargas/token.json', 'w') as Token:
            Token.write(Creds.to_json())
    return build('drive', 'v3', credentials=Creds)

