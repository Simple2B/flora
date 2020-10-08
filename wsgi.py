#!/user/bin/env python
import os
import click

from app import create_app, db, models, forms
from app.models import User, WorkItem, Exclusion, Clarification, Bid, WorkItemGroup
from app.controllers import populate_db_by_test_data

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

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    user = User(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        position=ADMIN_POSITION,
        phone=ADMIN_PHONE,
        user_type=ADMIN_TYPE,
        activated=True,
    )

    user.password = ADMIN_PASSWORD
    user.save()
    work_item = WorkItem(
        name=WORK_ITEM_NAME,
        code=WORK_ITEM_CODE,
    )
    work_item.save()

    exclusion = Exclusion(title=EXCLUSION_TITLE, description=EXCLUSION_DESCRIPTION)
    exclusion.save()

    clarification = Clarification(
        note=CLARIFICATION_NOTE, description=CLARIFICATION_DESCRIPTION
    )
    clarification.save()

    for i in range(8):
        bid = Bid()
        bid.save()

    if app.config['GENERATE_TEST_DATA']:
        populate_db_by_test_data()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
