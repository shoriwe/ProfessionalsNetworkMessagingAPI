import email.mime.text
import re
import smtplib

import flask

from messaging import api_key_validation

email_blueprint = flask.Blueprint("Email", "email")


def is_valid_email_address(email_address: str) -> bool:
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address) is not None


def prepare_email_message(from_: str, to_: str, subject: str, message: str) -> str:
    mime_message = email.mime.text.MIMEText(message, "html")
    mime_message["Subject"] = subject
    mime_message["From"] = from_
    mime_message["To"] = to_
    return mime_message.as_string()


def send_email(email_address: str, subject: str, message: str, current_app: flask.Flask):
    connection = smtplib.SMTP_SSL(current_app.config["SMTPAddress"], current_app.config["SMTPPort"])
    connection.login(current_app.config["SMTPUser"], current_app.config["SMTPPassword"])
    connection.sendmail(current_app.config["EmailFrom"],
                        email_address,
                        prepare_email_message(current_app.config["EmailFrom"], email_address, subject, message))
    connection.close()


@email_blueprint.route("/send/email", methods=("POST",))
def send_sms():
    form = flask.request.form
    if api_key_validation.is_api_key_valid(form.get("APIKey"), flask.current_app):
        subject = form.get("Subject")
        if subject is not None:
            message = form.get("Message")
            if message is not None:
                email_address = form.get("EmailAddress")
                if email_address is not None:
                    if is_valid_email_address(email_address):
                        send_email(email_address, subject, message, flask.current_app)
                    return {"Error": "The email address supplied is invalid"}
                return {"Error": "No email address supplied"}
            return {"Error": "No message supplied"}
        return {"Error": "No subject supplied"}
    return {"Error": "Invalid APIKey"}
