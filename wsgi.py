#!/user/bin/env python
import os
import click

from app import create_app, db, models, forms
from app.models import User

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '1234')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@admin.com')

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
    user = User(username=ADMIN_USERNAME, email=ADMIN_EMAIL, activated=True)
    user.password = ADMIN_PASSWORD
    user.save()


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == '__main__':
    app.run()
