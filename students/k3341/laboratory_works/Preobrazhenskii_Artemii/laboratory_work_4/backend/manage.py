#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", default=None)

    if sys.argv[1] == "test":
        if settings_module:
            print(
                "Ignoring config('DJANGO_SETTINGS_MODULE') because it's test. "
                "Using 'brvjeoCloud.settings.test'"
            )
        os.environ["DJANGO_SETTINGS_MODULE"] = "brvjeoCloud.settings.test"
    else:
        if settings_module is None:
            print(
                "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
                "Remember to create .env file at project root. "
                "Check README for more info."
            )
            sys.exit(1)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
