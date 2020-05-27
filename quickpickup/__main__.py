# System imports
import logging.config

# 3rd party
import waitress

# Package imports
from . import api


def main():
    """ Run the webserver using waitress. """
    waitress.serve(api.app, listen="0.0.0.0:8080")


def configure_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "%(asctime)s [%(levelname)s] [%(name)s] %(module)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "root": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
    )


if __name__ == "__main__":
    configure_logging()
    main()
