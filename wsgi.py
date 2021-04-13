#!/user/bin/env python
import os
import click

from app import create_app, db, models, forms
from app.models import User
from app.controllers import populate_db_by_test_data, bid_generation
from app.logger import log

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "1234")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
ADMIN_POSITION = os.environ.get("ADMIN_POSITION", "administrator")
ADMIN_PHONE = os.environ.get("ADMIN_PHONE", "0987654321")
ADMIN_TYPE = os.environ.get("ADMIN_TYPE", "admin")

WORK_ITEM_NAME = os.environ.get("WORK_ITEM_NAME", "TESTCLARIFICATION")
WORK_ITEM_CODE = os.environ.get("WORK_ITEM_CODE", "99.99")

# WORK_ITEM_GROUP_NAME = os.environ.get("WORK_ITEM_GROUP_NAME", "TEST_WORK_ITEM_GROUP_NAME")


EXCLUSION_TITLE = os.environ.get("EXCLUSION_TITLE", "TESTEXCLUSION")
EXCLUSION_DESCRIPTION = os.environ.get("EXCLUSION_DESCRIPTION", "some exclusion")

CLARIFICATION_NOTE = os.environ.get("CLARIFICATION_NOTE", "TESTWORKITEM")
CLARIFICATION_DESCRIPTION = os.environ.get(
    "CLARIFICATION_DESCRIPTION", "some clarification"
)

log.set_level(log.DEBUG)
app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, forms=forms)


def fill_db():
    user = User(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        position=ADMIN_POSITION,
        phone=ADMIN_PHONE,
        user_type=ADMIN_TYPE,
        activated=True,
    )

    user.password = ADMIN_PASSWORD
    user.save(commit=False)

    if app.config['GENERATE_TEST_DATA']:
        log(log.INFO, "Generete test data [%s]", app.config['GENERATE_TEST_DATA'])
        populate_db_by_test_data()
        bid_generation()
    db.session.commit()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def reset_db():
    db.drop_all()
    db.create_all()
    fill_db()


@app.cli.command()
def update_bids():
    """Gets new bids from ProCore system"""
    from app.controllers import update_bids
    update_bids()


if __name__ == "__main__":
    app.run()
