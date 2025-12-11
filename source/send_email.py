import os
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ssl._create_default_https_context = ssl._create_unverified_context

def notify_by_email(email_added):
     
    message = Mail(
        from_email='exodus@edson-rodrigues.site',
        to_emails='er3303992@gmail.com',
        subject='Early Adopters Database',
        html_content=f'<strong>New email added to the Early Adopters Database: {email_added}</strong>'
    )

    try:
        sg = SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY')
        )

        response = sg.send(message)

        return { 
            "status_code": response.status_code,
            "body": response.body,
            "headers": response.headers
        }

    except Exception as e:
        print("SendGrid error:", e)
        return {"error": str(e)}