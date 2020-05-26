import logging
import waitress

from .api import app


def main():
    """ Run the webserver using waitress. """
    waitress.serve(app, listen="0.0.0.0:8080")


def configure_logging():
    logging.dictConfig(
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
