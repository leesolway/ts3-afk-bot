"""
This module contains utility functions and classes that are used throughout the application.

These may include functions for data manipulation, error handling, logging, and any other
functionality that doesn't fit neatly into one of the main classes or modules.
"""

import logging
import os
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
        logging.error(
            "Required configuration is missing: '{var_name}' is not set.",
            var_name=var_name,
        )
        sys.exit(1)
    if value is not None:
        try:
            return var_type(value)
        except ValueError:
            logging.error(
                "Environment variable '%s' must be of type %s.",
                var_name,
                var_type.__name__,
            )
            sys.exit(1)
    return value
