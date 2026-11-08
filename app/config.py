import os


class Config:
    """Application settings, read from environment variables.

    os.environ[...] is used on purpose: if a setting is missing,
    the app refuses to start instead of running half-configured.
    """

    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
