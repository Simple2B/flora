from sqlalchemy import inspect
from app.models import Bid


def calculate_subtotal(bid_id, tbd_choices=[], tbd_name='', on_tbd=True):
    bid = Bid.query.get(bid_id)

    percent_permit_fee = bid.percent_permit_fee
    percent_general_condition = bid.percent_general_condition
    percent_overhead = bid.percent_overhead
    percent_insurance_tax = bid.percent_insurance_tax
    percent_profit = bid.percent_profit
    percent_bond = bid.percent_bond

    if tbd_name:
        if tbd_name == 'permit':
            if on_tbd:
                bid.permit_filling_fee = 0.0
                bid.permit_filling_fee_tbd = True
            else:
                bid.permit_filling_fee = round((percent_permit_fee * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.permit_filling_fee
        elif tbd_name == 'general':
            if on_tbd:
                bid.general_conditions = 0.0
                bid.general_conditions_tbd = True
            else:
                bid.general_conditions = round((percent_general_condition * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.general_conditions
        elif tbd_name == 'overhead':
            if on_tbd:
                bid.overhead = 0.0
                bid.overhead_tbd = True
            else:
                bid.overhead = round((percent_overhead * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.overhead
        elif tbd_name == 'insurance':
            if on_tbd:
                bid.insurance_tax = 0.0
                bid.insurance_tax_tbd = True
            else:
                bid.insurance_tax = round((percent_insurance_tax * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.insurance_tax
        elif tbd_name == 'profit':
            if on_tbd:
                bid.profit = 0.0
                bid.profit_tbd = True
            else:
                bid.profit = round((percent_profit * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.profit
        elif tbd_name == 'bond':
            if on_tbd:
                bid.bond = 0.0
                bid.bond_tbd = True
            else:
                bid.bond = round((percent_bond * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.bond
        bid.save()

    else:
        # bid.subtotal
        subtotal = 0.0

        dictionary_bid_attrs = inspect(bid).dict
        if not tbd_choices:
            tbd_choices = {i for i in dictionary_bid_attrs if dictionary_bid_attrs[i] == 0}

        for link in bid.link_work_items:
            link.link_subtotal = 0.0
            for line in link.work_item_lines:
                if line.tbd:
                    continue
                else:
                    subtotal += line.price * line.quantity
                    link.link_subtotal += line.price * line.quantity
            link.link_subtotal = round(link.link_subtotal, 2)

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
            permit_filling_fee = round((percent_permit_fee * subtotal) / 100, 2)
            if bid.permit_filling_fee != permit_filling_fee:
                bid.permit_filling_fee = permit_filling_fee
                was_change = True
        if "general" in tbd_choices or "general_conditions" in tbd_choices:
            general_conditions = 0.0
            bid.general_conditions = 0.0
            was_change = True
        else:
            general_conditions = round((percent_general_condition * subtotal) / 100, 2)
            if bid.general_conditions != general_conditions:
                bid.general_conditions = general_conditions
                was_change = True
        if "overhead" in tbd_choices:
            overhead = 0.0
            bid.overhead = 0.0
            was_change = True
        else:
            overhead = round((percent_overhead * subtotal) / 100, 2)
            if bid.overhead != overhead:
                bid.overhead = overhead
                was_change = True
        if "insurance" in tbd_choices or "insurance_tax" in tbd_choices:
            insurance_tax = 0.0
            bid.insurance_tax = 0.0
            was_change = True
        else:
            insurance_tax = round((percent_insurance_tax * subtotal) / 100, 2)
            if bid.insurance_tax != insurance_tax:
                bid.insurance_tax = insurance_tax
                was_change = True
        if "profit" in tbd_choices:
            profit = 0.0
            bid.profit = 0.0
            was_change = True
        else:
            profit = round((percent_profit * subtotal) / 100, 2)
            if bid.profit != profit:
                bid.profit = profit
                was_change = True
        if "bond" in tbd_choices:
            bond = 0.0
            bid.bond = 0.0
            was_change = True
        else:
            bond = round((percent_bond * subtotal) / 100, 2)
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


def calculate_alternate_total(bid_id):
    bid = Bid.query.get(bid_id)
    alternate_total = 0
    for alternate in bid.alternates:
        if alternate.tbd is True:
            continue
        else:
            alternate_total += (alternate.price * alternate.quantity)
    return round(alternate_total, 2)


# work mostly with JS

def check_bid_tbd(bid_id, tbd_name):
    bid = Bid.query.get(bid_id)
    switch = {
        "permit": lambda: bid.permit_filling_fee_tbd,
        "general": lambda: bid.general_conditions_tbd,
        "overhead": lambda: bid.overhead_tbd,
        "insurance": lambda: bid.insurance_tax_tbd,
        "profit": lambda: bid.profit_tbd,
        "bond": lambda: bid.bond_tbd
    }

    def default_case():
        return 'No case found!'

    bid_tbd = switch.get(tbd_name, default_case)()

    if not bid_tbd and bid_tbd != 'No case found!':
        calculate_subtotal(bid_id, tbd_name=tbd_name, on_tbd=False)

    return bid_tbd
