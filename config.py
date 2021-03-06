import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Flora"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "bdb9a7da402bf4f386c75a4f7b273706ba619afeebef602ba151d95f707df928d3fc1e2ccf56419a6e8f76"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    GENERATE_TEST_DATA = int(os.environ.get('GENERATE_TEST_DATA', '0'))

    # Permit/Filling Fee: 8%
    PERCENT_PERMIT_FEE = float(os.environ.get("PERCENT_PERMIT_FEE", '8'))
    # General Conditions: 5%
    PERCENT_GENERAL_CONDITION = float(os.environ.get("PERCENT_GENERAL_CONDITION", '5'))
    # Overhead: 5%
    PERCENT_OVERHEAD = float(os.environ.get("PERCENT_OVERHEAD", '5'))
    # Insurance/Tax: 5%
    PERCENT_INSURANCE_TAX = float(os.environ.get("PERCENT_INSURANCE_TAX", '5'))
    # Profit: 5%
    PERCENT_PROFIT = float(os.environ.get("PERCENT_PROFIT", '5'))
    # Bond: 5%
    PERCENT_BOND = float(os.environ.get("PERCENT_BOND", '5'))

    PROCORE_API_CLIENT_ID = os.environ.get("PROCORE_API_CLIENT_ID", '')
    PROCORE_API_CLIENT_SECRET = os.environ.get("PROCORE_API_CLIENT_SECRET", '')
    PROCORE_API_REDIRECT_URI = os.environ.get("PROCORE_API_REDIRECT_URI", '')
    PROCORE_API_OAUTH_URL = os.environ.get("PROCORE_API_OAUTH_URL", '')
    PROCORE_API_BASE_URL = os.environ.get("PROCORE_API_BASE_URL", '')
    PROCORE_API_COMPANY_ID = os.environ.get("PROCORE_API_COMPANY_ID", '')

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(base_dir, "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(base_dir, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
