from app import db
from app.models import User, WorkItem, Exclusion, Clarification, Bid, WorkItemGroup
from app.models import WorkItemLine, ClarificationLink, ExclusionLink, LinkWorkItem


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
                title=f"Exclusion {i}"
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

    # bid save()
    bid = Bid(
        procore_bid_id=105,
        title="bidding 5",
        client="Procore (Test Companies)",
        status=Bid.Status.b_draft
    ).save()

    for i in range(2):
        bid = Bid(
            procore_bid_id=106+i,
            title="bidding i",
            client="Procore (Test Companies)",
            status=Bid.Status.c_submitted
        ).save()

    for i in range(2):
        bid = Bid(
            procore_bid_id=108+i,
            title=f"bidding {3+i}",
            client="Procore (Test Companies)",
            status=Bid.Status.d_archived
        ).save()
    # end bid save()
    work_item = WorkItem.query.first()
    link_wi = LinkWorkItem(bid_id=bid.id, work_item_id=work_item.id).save()
    WorkItemLine(
        note="Work Item line 1 note",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        price=56.56,
        unit='item',
        quantity=5,
        link_work_items_id=link_wi.id
    ).save()

    WorkItemLine(
        note="Work Item line 2 note",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        price=78.78,
        unit='item',
        quantity=2,
        link_work_items_id=link_wi.id
    ).save()

    ######################################
    # Add Group1
    work_item_group = WorkItemGroup(
        bid_id=bid.id,
        name="Group1"
    ).save()
    link_wi = LinkWorkItem(bid_id=bid.id, work_item_id=work_item.id, work_item_group=work_item_group).save()
    WorkItemLine(
        note="Work Item line 1 in group1 ",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        price=56.56,
        unit='item',
        quantity=5,
        link_work_items_id=link_wi.id
    ).save()

    WorkItemLine(
        note="Work Item line 2 in group1",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        price=78.78,
        unit='item',
        quantity=2,
        link_work_items_id=link_wi.id
    ).save()
    ######################################

    clarifications = Clarification.query.all()
    ClarificationLink(
        bid_id=bid.id,
        clarification_id=clarifications[0].id
    ).save()

    ClarificationLink(
        bid_id=bid.id,
        clarification_id=clarifications[1].id
    ).save()

    exclusion = Exclusion.query.all()
    ExclusionLink(
        bid_id=bid.id,
        exclusion_id=exclusion[0].id
    ).save()

    ExclusionLink(
        bid_id=bid.id,
        exclusion_id=exclusion[1].id
    ).save()

    db.session.commit()
