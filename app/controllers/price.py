from flask import current_app as app
from app.models import Bid


def calculate_subtotal(bid_id):
    PERCENT_PERMIT_FEE = float(app.config["PERCENT_PERMIT_FEE"])
    PERCENT_GENERAL_CONDITION = float(app.config["PERCENT_GENERAL_CONDITION"])
    PERCENT_OVERHEAD = float(app.config["PERCENT_OVERHEAD"])
    PERCENT_INSURANCE_TAX = float(app.config["PERCENT_INSURANCE_TAX"])
    PERCENT_PROFIT = float(app.config["PERCENT_PROFIT"])
    PERCENT_BOND = float(app.config["PERCENT_BOND"])

    bid = Bid.query.get(bid_id)
    # bid.subtotal
    subtotal = 0.0
    for link in bid.link_work_items:
        for line in link.work_item_lines:
            subtotal += line.price * line.quantity

    subtotal = round(subtotal, 2)
    was_change = False
    if bid.subtotal != subtotal:
        bid.subtotal = subtotal
        was_change = True

    permit_filling_fee = round((PERCENT_PERMIT_FEE * subtotal) / 100, 2)
    if bid.permit_filling_fee != permit_filling_fee:
        bid.permit_filling_fee = permit_filling_fee
        was_change = True

    general_conditions = round((PERCENT_GENERAL_CONDITION * subtotal) / 100, 2)
    if bid.general_conditions != general_conditions:
        bid.general_conditions = general_conditions
        was_change = True

    overhead = round((PERCENT_OVERHEAD * subtotal) / 100, 2)
    if bid.overhead != overhead:
        bid.overhead = overhead
        was_change = True

    insurance_tax = round((PERCENT_INSURANCE_TAX * subtotal) / 100, 2)
    if bid.insurance_tax != insurance_tax:
        bid.insurance_tax = insurance_tax
        was_change = True

    profit = round((PERCENT_PROFIT * subtotal) / 100, 2)
    if bid.profit != profit:
        bid.profit = profit
        was_change = True

    bond = round((PERCENT_BOND * subtotal) / 100, 2)
    if bid.bond != bond:
        bid.bond = bond
        was_change = True

    grand_subtotal = round(
        subtotal
        + permit_filling_fee
        + general_conditions
        + overhead
        + insurance_tax
        + profit
        + bond,
        2,
    )
    if bid.grand_subtotal != grand_subtotal:
        bid.grand_subtotal = grand_subtotal
        was_change = True

    if was_change:
        bid.save()
