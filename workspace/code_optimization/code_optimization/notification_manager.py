import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class NotificationManager:
    """
    A class used to notify the user

    ...

    Attributes
    ----------
    sender_email : str
        The sender's email address
    sender_password : str
        The sender's email password
    receiver_email : str
        The receiver's email address

    Methods
    -------
    notify_user(message: str):
        Sends a notification to the user with the given message
    """

    def __init__(self, sender_email: str, sender_password: str, receiver_email: str):
        """
        Constructs all the necessary attributes for the NotificationManager object.

        Parameters:
            sender_email (str): The sender's email address
            sender_password (str): The sender's email password
            receiver_email (str): The receiver's email address
        """

        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def notify_user(self, message: str):
        """
        Sends a notification to the user with the given message

        Parameters:
        message (str): The message to be sent to the user

        Returns:
        None
        """

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = "Code Optimization and Hardening Notification"

        # Attach the message to the multipart message
        msg.attach(MIMEText(message, 'plain'))

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to the server and send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls(context=context)  # Secure the connection
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()
