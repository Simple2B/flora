from app import db
from app.models import User, WorkItem, Exclusion, Clarification, Bid


def populate_db_by_test_data():
    for i in range(10):
        user = User(
                username=f"user_{i}",
                email=f"user_{i}@email.com",
                position="QA",
                phone=f"+0987654{321 + i}",
                user_type=User.Type.user,
                activated=True,
            )
        user.password = f"pa$$w0rd{i}"
        db.session.add(user)
        db.session.add(
            WorkItem(
                name=f"Work Item {i}",
                code=f"{i}.{i%8}",
            )
        )
        db.session.add(
            Exclusion(
                title=f"Exclusion {i}",
                description=(
                    "Consequat nostrud ullamco officia incididunt officia dolore voluptate pariatur."
                    " Ea aliqua dolore esse elit labore ullamco fugiat consequat ut."
                    " Eu aliquip velit reprehenderit ea nulla sunt pariatur mollit."
                ),
            )
        )
        db.session.add(
            Clarification(
                note=f"Clarification Note {i}",
                description=(
                    "Consequat nostrud ullamco officia incididunt officia dolore voluptate pariatur."
                    " Ea aliqua dolore esse elit labore ullamco fugiat consequat ut."
                    " Eu aliquip velit reprehenderit ea nulla sunt pariatur mollit."
                ),
            )
        )

    Bid(
        procore_bid_id=105,
        title="bidding 5",
        client="Procore (Test Companies)",
        status=Bid.Status.b_draft
    ).save()

    db.session.commit()
