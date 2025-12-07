import email

def parse_email(raw_email):
    """
    Parses raw email string into an email.message.EmailMessage object
    """
    # Return empty fields if row is not a string

    if not isinstance(raw_email, str):
        return {
            "subject": '', "sender": '', "date": '', 
            "to": '', "cc": '', "bcc": '', 
            "body": '', "headers": ''
        }
    
    msg = email.message_from_string(raw_email)
    raw_headers = str(msg.items())
    
    body_content = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":

                body_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                
    else: 
        body_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    
    return {
       "subject": msg.get("Subject", ''),
        "sender": msg.get("From", ''),
        "date": msg.get("Date", ''), 
        "to": msg.get("To", ''), 
        "cc": msg.get("Cc", ''), 
        "bcc": msg.get("Bcc", ''), 
        "body": body_content,
        "headers": raw_headers
    }