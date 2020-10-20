import os


def read_environment_variable(variable_name: str) -> str:
    return os.environ.get(variable_name)


def get_configuration_variables() -> dict:
    variables = {
        "SMTPAddress": str,
        "SMTPPort": int,
        "RedisAddress": str,
        "RedisPort": int,
        "SMTPUser": str,
        "SMTPPassword": str,
        "RedisPassword": str,
        "NexmoUser": str,
        "NexmoPassword": str,
        "SMSFrom": str,
        "EmailFrom": str
    }
    for variable in variables.keys():
        value = read_environment_variable(variable)
        if value is not None:
            if variables[variable] == int:
                if value.isnumeric():
                    variables[variable] = int(value)
                else:
                    print(f"Variable \"{variable}\" need to be numeric")
                    exit(-1)
            elif variables[variable] == str:
                if len(value):
                    variables[variable] = value
                else:
                    print(f"Variable \"{variable}\" can't be empty")
                    exit(-1)
        else:
            print(f"Variable \"{variable}\" is required")
            exit(-1)
    return variables
