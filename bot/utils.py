import os
import logging
import sys

def get_env_var(var_name, default=None, var_type=str, required=True):
    """
    Fetches an environment variable, ensuring it meets the specified requirements.

    :param var_name: Name of the environment variable.
    :param default: Default value to return if the variable is not set. Ignored if required is True.
    :param var_type: Expected type of the environment variable. Attempts to convert to this type.
    :param required: If True, the program will exit if the variable is not set or conversion fails.
    :return: Value of the environment variable (or the default value).
    """
    value = os.getenv(var_name, default)
    if value is None and required:
        logging.error(f"Required configuration is missing: '{var_name}' is not set.")
        sys.exit(1)
    if value is not None:
        try:
            return var_type(value)
        except ValueError:
            logging.error(f"Environment variable '{var_name}' must be of type {var_type.__name__}.")
            sys.exit(1)
    return value