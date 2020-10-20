import re

import flask

from messaging import contants, api_key_validation

sms_blueprint = flask.Blueprint("SMS", "sms")


def is_valid_country_code(country_code: str) -> bool:
    return country_code in contants.phone_country_codes


def is_valid_phone_number(phone_number: str) -> bool:
    return re.match(r"^\d{10}$", phone_number) is not None


@sms_blueprint.route("/send/sms", methods=("POST",))
def send_sms():
    form = flask.request.form
    if api_key_validation.is_api_key_valid(form.get("APIKey"), flask.current_app):
        message = form.get("Message")
        if message:
            country_code = form.get("CountryCode")
            if country_code is not None:
                phone_number = form.get("PhoneNumber")
                if phone_number is not None:
                    if is_valid_country_code(country_code) and is_valid_phone_number(phone_number):
                        flask.current_app.config["NexmoClient"].send_message({
                            "from": flask.current_app.config["SMSFrom"],
                            "to": (country_code + phone_number)[1:],
                            "text": message + "\n",
                        })
                        return {"Success": "Message was sent successfully"}
                    return {"Error": "Invalid country code or phone number"}
                return {"Error": "No phone number  supplied"}
            return {"Error": "No country code supplied"}
        return {"Error": "No message supplied"}
    return {"Error": "Invalid APIKey"}
