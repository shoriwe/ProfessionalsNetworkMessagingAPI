import flask
import redis


def is_api_key_valid(api_key: str, current_app: flask.Flask) -> bool:
    connection = redis.Redis(current_app.config["RedisAddress"],
                             current_app.config["RedisPort"],
                             6,
                             current_app.config["RedisPassword"])
    found = connection.exists(api_key)
    connection.close()
    return found
