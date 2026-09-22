import time

from rfq_manager import create_rfq
from outlook_sender import send_rfq_email
from outlook_monitor import scan_inbox_for_rfq
from quotation_reader import read_all_quotes

from reports.comparison_generator import generate_comparison
from reports.excel_report import generate_excel_report

from ai_negotiation_agent import start_negotiation

from data_manager import get_vendors
from body_quotes import clear_quotes
import os

WAIT_TIME = 30          # seconds
MIN_QUOTES = 3
MAX_ROUNDS = 3

# STOP_PROCUREMENT = False

def start_procurement(
        
        product,
        quantity,
        specification,
        budget,
        status_callback=None,
        log_callback=None
):
    global STOP_PROCUREMENT
    STOP_PROCUREMENT = False

    def status(text):
        print(text)
        if status_callback:
            status_callback(text)

    def log(text):
        print(text)
        if log_callback:
            log_callback(text)

    # -----------------------------------
    # STEP 1 : Clear Old Quotes
    # -----------------------------------

    clear_quotes()

    status("Creating RFQ...")
    log("Creating RFQ")

    rfq = create_rfq(
        product,
        quantity,
        specification,
        budget
    )

    # -----------------------------------
    # STEP 2 : Send RFQ
    # -----------------------------------

    status("Sending RFQ To Vendors...")

    vendors = get_vendors()

    for vendor in vendors:

        send_rfq_email(
            vendor["email"],
            vendor["name"],
            rfq
        )

        log(f"Mail Sent -> {vendor['name']}")

    status("RFQ Sent Successfully")

    # -----------------------------------
    # STEP 3 : Wait For Quotations
    # -----------------------------------

    status("Waiting For Vendor Quotations...")

    total_quotes = 0

    while total_quotes < MIN_QUOTES:

        scan_inbox_for_rfq()

        quotes = read_all_quotes()

        print("=" * 50)
        print("QUOTES =", quotes)
        print("=" * 50)

        total_quotes = len(quotes)

        status(f"Quotations Received : {total_quotes}/{MIN_QUOTES}")

        if total_quotes >= MIN_QUOTES:
            break

        time.sleep(WAIT_TIME)

    log(f"{total_quotes} Quotations Received")

    # -----------------------------------
    # STEP 4 : Initial Comparison
    # -----------------------------------

    status("Generating Initial Comparison...")

    quotes = read_all_quotes()

    comparison = generate_comparison(quotes)

    print("=" * 50)
    print("COMPARISON =", comparison)
    print("=" * 50)

    if len(comparison) == 0:
        raise Exception("No quotations found for comparison.")

    generate_excel_report(comparison)

    log("Initial Comparison Generated")

    # -----------------------------------
    # STEP 5 : Budget Check
    # -----------------------------------

    budget = str(budget).strip()

    if budget == "":
        budget = 0

    budget = float(budget)

    lowest_price = comparison[0]["price"]

    if lowest_price in ("", None):
        raise Exception("Lowest price is empty.")

    lowest_price = float(lowest_price)

    print(f"Lowest Price = {lowest_price}")
    print(f"Budget = {budget}")

    if lowest_price <= budget:

        status("Budget Achieved. Negotiation Not Required.")

        report = generate_excel_report(comparison)

        log("Budget Already Achieved")

        status("Procurement Completed")

        return report

    # -----------------------------------
    # STEP 6 : AI Negotiation
    # -----------------------------------

    STOP_PROCUREMENT = False

    status("Starting AI Negotiation...")

    round_no = 1

    while not STOP_PROCUREMENT:

        status(f"Negotiation Round {round_no}")

        result = start_negotiation(
            rfq["rfq_id"],
            round_no
        )

        log(result)

        status("Waiting For Vendor Replies...")

        last_price = lowest_price

        while not STOP_PROCUREMENT:

            scan_inbox_for_rfq()

            quotes = read_all_quotes()

            comparison = generate_comparison(quotes)

            if len(comparison):

                generate_excel_report(comparison)

                current_lowest = float(comparison[0]["price"])

                if current_lowest < last_price:

                    log(f"New Lowest Price : ₹{current_lowest}")

                    last_price = current_lowest

                    # Budget Achieved
                    if current_lowest <= budget:

                        status("✅ Budget Achieved")

                        log("Negotiation Stopped Automatically")

                        STOP_PROCUREMENT = True

                        break

            time.sleep(10)

        if STOP_PROCUREMENT:
            break

        # break
    # round_no += 1

    # if round_no > MAX_ROUNDS:

    #     status("Maximum Negotiation Rounds Completed")

    #     break

    # -----------------------------------
    # STEP 7 : Final Report
    # -----------------------------------

    status("Generating Final Report...")

    report = generate_excel_report(comparison)

    status("Procurement Completed")

    log(f"Winner : {comparison[0]['vendor']}")
    log(f"Lowest Price : ₹{comparison[0]['price']}")
    log("Final Excel Report Generated")


    print(report)
    print(os.path.abspath(report))
    print(os.path.exists(report))

    os.startfile(report)

    return report

def stop_procurement():

    global STOP_PROCUREMENT

    STOP_PROCUREMENT = True

    print("🛑 Stop Requested")

