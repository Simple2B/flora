from app.models import Bid, WorkItemLine
from app.logger import log


def calculate_link_subtotal(bid_id, line_id=None):
    bid = Bid.query.get(bid_id)
    if line_id:
        # calculdate work item line and link subtotal
        work_item_line = WorkItemLine.query.get(line_id)
        if not bid:
            log(log.WARNING, "No bid with [id:%d] found!", bid_id)
            return None
        link_work_item = work_item_line.link_work_item
        line_subtotal = round((work_item_line.price * work_item_line.quantity), 2)
        if work_item_line.tbd:
            bid.subtotal = round(bid.subtotal - line_subtotal, 2)
            bid_subtotal = bid.subtotal
            link_work_item.link_subtotal = round(
                link_work_item.link_subtotal - line_subtotal, 2
            )
        else:
            bid.subtotal = round(bid.subtotal + line_subtotal, 2)
            bid_subtotal = bid.subtotal
            link_work_item.link_subtotal = round(
                link_work_item.link_subtotal + line_subtotal, 2
            )
        bid.permit_filling_fee = (
            round((bid.percent_permit_fee * bid_subtotal) / 100, 2)
            if not bid.permit_filling_fee_tbd
            else 0.0
        )
        bid.general_conditions = (
            round((bid.percent_general_condition * bid_subtotal) / 100, 2)
            if not bid.general_conditions_tbd
            else 0.0
        )
        bid.overhead = (
            round((bid.percent_overhead * bid_subtotal) / 100, 2)
            if not bid.overhead_tbd
            else 0.0
        )
        bid.insurance_tax = (
            round((bid.percent_insurance_tax * bid_subtotal) / 100, 2)
            if not bid.insurance_tax_tbd
            else 0.0
        )
        bid.profit = (
            round((bid.percent_profit * bid_subtotal) / 100, 2)
            if not bid.profit_tbd
            else 0.0
        )
        bid.bond = (
            round((bid.percent_bond * bid_subtotal) / 100, 2)
            if not bid.bond_tbd
            else 0.0
        )
        bid.grand_subtotal = round(
            bid_subtotal
            + bid.permit_filling_fee
            + bid.general_conditions
            + bid.overhead
            + bid.insurance_tax
            + bid.profit
            + bid.bond,
            2
        )

        link_work_item.save()
        bid.save()
        return dict(
            subtotal=bid_subtotal,
            grandSubtotal=bid.grand_subtotal,
            linkWorkItemID=f"{link_work_item.id}",
            linkWorkItemSubtotal=f"{link_work_item.link_subtotal}",
            bidParamValues=dict(
                permit=str(bid.permit_filling_fee),
                general=str(bid.general_conditions),
                overhead=str(bid.overhead),
                insurance=str(bid.insurance_tax),
                profit=str(bid.profit),
                bond=str(bid.bond),
            ),
        )

    bid_subtotal = 0.0
    for link in bid.link_work_items:
        link.link_subtotal = 0.0
        for line in link.work_item_lines:
            if line.tbd:
                continue
            bid_subtotal += line.price * line.quantity
            link.link_subtotal += line.price * line.quantity
        link.link_subtotal = round(link.link_subtotal, 2)
    bid_subtotal = round(bid_subtotal, 2)
    return bid_subtotal


def calculate_subtotal(bid_id, tbd_choices=[], tbd_name="", on_tbd=True):
    bid = Bid.query.get(bid_id)

    percent_permit_fee = bid.percent_permit_fee
    percent_general_condition = bid.percent_general_condition
    percent_overhead = bid.percent_overhead
    percent_insurance_tax = bid.percent_insurance_tax
    percent_profit = bid.percent_profit
    percent_bond = bid.percent_bond

    if tbd_name:
        if tbd_name == "permit":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.permit_filling_fee
                bid.permit_filling_fee = 0.0
                bid.permit_filling_fee_tbd = True
            else:
                bid.permit_filling_fee = round(
                    (percent_permit_fee * bid.subtotal) / 100, 2
                )
                bid.grand_subtotal = bid.grand_subtotal + bid.permit_filling_fee
                bid.permit_filling_fee_tbd = False
        elif tbd_name == "general":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.general_conditions
                bid.general_conditions = 0.0
                bid.general_conditions_tbd = True
            else:
                bid.general_conditions = round(
                    (percent_general_condition * bid.subtotal) / 100, 2
                )
                bid.grand_subtotal = bid.grand_subtotal + bid.general_conditions
                bid.general_conditions_tbd = False
        elif tbd_name == "overhead":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.overhead
                bid.overhead = 0.0
                bid.overhead_tbd = True
            else:
                bid.overhead = round((percent_overhead * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.overhead
                bid.overhead_tbd = False
        elif tbd_name == "insurance":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.insurance_tax
                bid.insurance_tax = 0.0
                bid.insurance_tax_tbd = True
            else:
                bid.insurance_tax = round(
                    (percent_insurance_tax * bid.subtotal) / 100, 2
                )
                bid.grand_subtotal = bid.grand_subtotal + bid.insurance_tax
                bid.insurance_tax_tbd = False
        elif tbd_name == "profit":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.profit
                bid.profit = 0.0
                bid.profit_tbd = True
            else:
                bid.profit = round((percent_profit * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.profit
                bid.profit_tbd = False
        elif tbd_name == "bond":
            if on_tbd:
                bid.grand_subtotal = bid.grand_subtotal - bid.bond
                bid.bond = 0.0
                bid.bond_tbd = True
            else:
                bid.bond = round((percent_bond * bid.subtotal) / 100, 2)
                bid.grand_subtotal = bid.grand_subtotal + bid.bond
                bid.bond_tbd = False
        bid.save()

    else:
        # bid.subtotal
        subtotal = calculate_link_subtotal(bid_id)

        was_change = False
        if bid.subtotal != subtotal:
            bid.subtotal = subtotal
            was_change = True

        if bid.permit_filling_fee_tbd:
            permit_filling_fee = 0.0
            bid.permit_filling_fee = 0.0
            was_change = True
        else:
            permit_filling_fee = round((percent_permit_fee * subtotal) / 100, 2)
            if bid.permit_filling_fee != permit_filling_fee:
                bid.permit_filling_fee = permit_filling_fee
                was_change = True
        if bid.general_conditions_tbd:
            general_conditions = 0.0
            bid.general_conditions = 0.0
            was_change = True
        else:
            general_conditions = round((percent_general_condition * subtotal) / 100, 2)
            if bid.general_conditions != general_conditions:
                bid.general_conditions = general_conditions
                was_change = True
        if bid.overhead_tbd:
            overhead = 0.0
            bid.overhead = 0.0
            was_change = True
        else:
            overhead = round((percent_overhead * subtotal) / 100, 2)
            if bid.overhead != overhead:
                bid.overhead = overhead
                was_change = True
        if bid.insurance_tax_tbd:
            insurance_tax = 0.0
            bid.insurance_tax = 0.0
            was_change = True
        else:
            insurance_tax = round((percent_insurance_tax * subtotal) / 100, 2)
            if bid.insurance_tax != insurance_tax:
                bid.insurance_tax = insurance_tax
                was_change = True
        if bid.profit_tbd:
            profit = 0.0
            bid.profit = 0.0
            was_change = True
        else:
            profit = round((percent_profit * subtotal) / 100, 2)
            if bid.profit != profit:
                bid.profit = profit
                was_change = True
        if bid.bond_tbd:
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
        if alternate.tbd:
            continue
        alternate_total += alternate.price * alternate.quantity
    return round(alternate_total, 2)


# work mostly with JS


def check_bid_tbd(bid_id, tbd_name):
    log(log.DEBUG, "check_bid_tbd() tbd_name:[%s] bid_id:[%d]", tbd_name, bid_id)
    bid = Bid.query.get(bid_id)
    switch = {
        "permit": bid.permit_filling_fee_tbd,
        "general": bid.general_conditions_tbd,
        "overhead": bid.overhead_tbd,
        "insurance": bid.insurance_tax_tbd,
        "profit": bid.profit_tbd,
        "bond": bid.bond_tbd,
    }

    if tbd_name not in switch:
        log(log.ERROR, "check_bid_tbd() tbd_name:[%s] unknown", tbd_name)
        return "No case found!"

    return switch[tbd_name]
