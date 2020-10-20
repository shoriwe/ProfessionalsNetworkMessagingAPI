import flask
import nexmo
import setup_environment
import messaging.email_sending
import messaging.sms_sending


app = flask.Flask(__name__)


def configure():
    variables = setup_environment.get_configuration_variables()
    app.register_blueprint(messaging.sms_sending.sms_blueprint)
    app.register_blueprint(messaging.email_sending.email_blueprint)

    app.config["NexmoClient"] = nexmo.Client(variables["NexmoUser"], variables["NexmoPassword"])
    app.config["RedisAddress"] = variables["RedisAddress"]
    app.config["RedisPort"] = variables["RedisPort"]
    app.config["RedisPassword"] = variables["RedisPassword"]

    app.config["SMSFrom"] = variables["SMSFrom"]
    app.config["EmailFrom"] = variables["EmailFrom"]

    app.config["SMTPUser"] = variables["SMTPUser"]
    app.config["SMTPPassword"] = variables["SMTPPassword"]

    app.config["SMTPAddress"] = variables["SMTPAddress"]
    app.config["SMTPPort"] = variables["SMTPPort"]
