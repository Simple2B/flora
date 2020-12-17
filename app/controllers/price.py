from flask import current_app as app
from app.models import Bid
from sqlalchemy import inspect


def calculate_subtotal(bid_id, tbd_choices=[], tbd_name=None, on_tbd=True):
    PERCENT_PERMIT_FEE = float(app.config["PERCENT_PERMIT_FEE"])
    PERCENT_GENERAL_CONDITION = float(app.config["PERCENT_GENERAL_CONDITION"])
    PERCENT_OVERHEAD = float(app.config["PERCENT_OVERHEAD"])
    PERCENT_INSURANCE_TAX = float(app.config["PERCENT_INSURANCE_TAX"])
    PERCENT_PROFIT = float(app.config["PERCENT_PROFIT"])
    PERCENT_BOND = float(app.config["PERCENT_BOND"])

    bid = Bid.query.get(bid_id)
    # bid.subtotal
    subtotal = 0.0

    if tbd_name:
        if tbd_name == 'permit':
            if on_tbd:
                bid.permit_filling_fee = 0.0
            else:
                bid.permit_filling_fee = round((PERCENT_PERMIT_FEE * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.permit_filling_fee
        elif tbd_name == 'general':
            if on_tbd:
                bid.general_conditions = 0.0
            else:
                bid.general_conditions = round((PERCENT_GENERAL_CONDITION * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.general_conditions
        elif tbd_name == 'overhead':
            if on_tbd:
                bid.overhead = 0.0
            else:
                bid.overhead = round((PERCENT_OVERHEAD * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.overhead
        elif tbd_name == 'insurance':
            if on_tbd:
                bid.insurance_tax = 0.0
            else:
                bid.insurance_tax = round((PERCENT_INSURANCE_TAX * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.insurance_tax
        elif tbd_name == 'profit':
            if on_tbd:
                bid.profit = 0.0
            else:
                bid.profit = round((PERCENT_PROFIT * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.profit
        elif tbd_name == 'bond':
            if on_tbd:
                bid.bond = 0.0
            else:
                bid.bond = round((PERCENT_BOND * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.bond
        bid.save()
    else:
        dictionary_bid_attrs = inspect(bid).dict
        if not tbd_choices:
            tbd_choices = {i for i in dictionary_bid_attrs if dictionary_bid_attrs[i] == 0}

        for link in bid.link_work_items:
            link.link_subtotal = 0.0
            for line in link.work_item_lines:
                subtotal += line.price * line.quantity
                link.link_subtotal += round((line.price * line.quantity), 2)

        subtotal = round(subtotal, 2)
        was_change = False
        if bid.subtotal != subtotal:
            bid.subtotal = subtotal
            was_change = True

        if "permit" in tbd_choices or "permit_filling_fee" in tbd_choices:
            permit_filling_fee = 0.0
            bid.permit_filling_fee = 0.0
            was_change = True
        else:
            permit_filling_fee = round((PERCENT_PERMIT_FEE * subtotal) / 100, 2)
            if bid.permit_filling_fee != permit_filling_fee:
                bid.permit_filling_fee = permit_filling_fee
                was_change = True
        if "general" in tbd_choices or "general_conditions" in tbd_choices:
            general_conditions = 0.0
            bid.general_conditions = 0.0
            was_change = True
        else:
            general_conditions = round((PERCENT_GENERAL_CONDITION * subtotal) / 100, 2)
            if bid.general_conditions != general_conditions:
                bid.general_conditions = general_conditions
                was_change = True
        if "overhead" in tbd_choices:
            overhead = 0.0
            bid.overhead = 0.0
            was_change = True
        else:
            overhead = round((PERCENT_OVERHEAD * subtotal) / 100, 2)
            if bid.overhead != overhead:
                bid.overhead = overhead
                was_change = True
        if "insurance" in tbd_choices or "insurance_tax" in tbd_choices:
            insurance_tax = 0.0
            bid.insurance_tax = 0.0
            was_change = True
        else:
            insurance_tax = round((PERCENT_INSURANCE_TAX * subtotal) / 100, 2)
            if bid.insurance_tax != insurance_tax:
                bid.insurance_tax = insurance_tax
                was_change = True
        if "profit" in tbd_choices:
            profit = 0.0
            bid.profit = 0.0
            was_change = True
        else:
            profit = round((PERCENT_PROFIT * subtotal) / 100, 2)
            if bid.profit != profit:
                bid.profit = profit
                was_change = True
        if "bond" in tbd_choices:
            bond = 0.0
            bid.bond = 0.0
            was_change = True
        else:
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


# work mostly with JS

def check_bid_tbd(bid_id, tbd_name):
    bid = Bid.query.get(bid_id)
    switch = {
        "permit": lambda: bid.permit_filling_fee,
        "general": lambda: bid.general_conditions,
        "overhead": lambda: bid.overhead,
        "insurance": lambda: bid.insurance_tax,
        "profit": lambda: bid.profit,
        "bond": lambda: bid.bond
    }

    def default_case():
        raise Exception('No case found!')

    return switch.get(tbd_name, default_case)()
