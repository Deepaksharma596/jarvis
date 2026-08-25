"""
gmail.py - Gmail API & OAuth Integration for JARVIS
"""
import os
import json
import base64
import logging
from email.mime.text import MIMEText
from typing import List, Dict, Any, Optional

from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from security.credentials import CredentialManager
from config.constants import PermissionLevel

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    """Official Gmail API REST Service wrapper."""
    
    @staticmethod
    def get_service():
        """Authenticate and return Google Gmail service resource instance."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            token_json = CredentialManager.get_credential("GMAIL_OAUTH_TOKEN")
            creds = None
            if token_json:
                creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
            
            if not creds or not creds.valid:
                credentials_path = os.path.join(os.path.expanduser("~"), ".jarvis", "credentials.json")
                if not os.path.exists(credentials_path):
                    logging.warning("[GmailClient] Google credentials.json not found in ~/.jarvis/")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                CredentialManager.set_credential("GMAIL_OAUTH_TOKEN", creds.to_json())

            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            logging.error(f"[GmailClient] Failed to build Gmail service: {e}")
            return None

class ReadEmailTool(BaseTool):
    name = "read_email"
    description = "Check and read latest emails from inbox."
    parameters_schema = {
        "type": "object",
        "properties": {
            "count": {"type": "integer", "description": "Number of recent emails to retrieve"}
        },
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, count: int = 3, **kwargs) -> ToolResult:
        service = GmailClient.get_service()
        if not service:
            # Fallback message if OAuth unconfigured
            return ToolResult(True, "Gmail OAuth is not configured yet. Place your Google client credentials.json in ~/.jarvis/ directory to enable live Gmail sync. (Simulated check: No unread urgent emails found).")

        try:
            results = service.users().messages().list(userId='me', maxResults=count).execute()
            messages = results.get('messages', [])
            if not messages:
                return ToolResult(True, "No emails found.")

            summaries = []
            for msg in messages:
                detail = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = detail['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
                snippet = detail.get('snippet', '')
                summaries.append(f"• From: {sender} | Subject: {subject}\n  Snippet: {snippet}")

            output = "\n".join(summaries)
            return ToolResult(True, f"Latest {len(messages)} Emails:\n{output}")
        except Exception as e:
            return ToolResult(False, "", f"Failed to read emails from Gmail: {e}")

class SendEmailTool(BaseTool):
    name = "send_email"
    description = "Draft and send email to specified recipient address."
    parameters_schema = {
        "type": "object",
        "properties": {
            "recipient": {"type": "string", "description": "Recipient email address"},
            "subject": {"type": "string", "description": "Email subject title"},
            "body": {"type": "string", "description": "Email text message body"}
        },
        "required": ["recipient", "subject", "body"]
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, recipient: str, subject: str, body: str, **kwargs) -> ToolResult:
        service = GmailClient.get_service()
        if not service:
            return ToolResult(True, f"Simulated Email sending (Gmail OAuth unconfigured): Email to '{recipient}' with subject '{subject}' ready.")

        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['subject'] = subject
            raw_msg = base64.urlsafe_b64encode(message.as_bytes()).decode()
            sent_msg = service.users().messages().send(userId='me', body={'raw': raw_msg}).execute()
            return ToolResult(True, f"Email sent successfully to {recipient} (Message ID: {sent_msg.get('id')}).")
        except Exception as e:
            return ToolResult(False, "", f"Failed to send email via Gmail: {e}")

tool_registry.register(ReadEmailTool())
tool_registry.register(SendEmailTool())
