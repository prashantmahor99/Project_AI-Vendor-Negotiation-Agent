from quotation_reader import read_all_quotes
from negotiation_engine import rank_quotes
from outlook_sender import send_negotiation_email
from data_manager import get_vendors

MAX_ROUNDS = 3


def start_negotiation(rfq_number, round_no=1):

    # -----------------------------
    # Read Latest Quotations
    # -----------------------------

    quotes = read_all_quotes()

    ranked = rank_quotes(quotes)

    if len(ranked) < 2:

        return "Need minimum 2 quotations."

    # -----------------------------
    # Lowest Vendor
    # -----------------------------

    lowest_vendor = ranked[0]["vendor"]

    lowest_price = float(ranked[0]["price"])

    print(f"\nCurrent L1 : {lowest_vendor}")
    print(f"Lowest Price : ₹{lowest_price}")

    # Ask vendors to beat current L1
    target_price = round(lowest_price - 1, 2)

    vendors = get_vendors()

    messages = []

    # -----------------------------
    # Send Negotiation Mail
    # -----------------------------

    for vendor in vendors:

        vendor_name = vendor["name"].strip().lower()

        # Skip current L1 vendor
        if vendor_name == lowest_vendor.strip().lower():

            print(f"Skipping L1 Vendor : {vendor['name']}")

            continue

        try:

            send_negotiation_email(

                vendor["email"],

                vendor["name"],

                target_price,

                rfq_number

            )

            print(

                f"Negotiation Mail Sent -> {vendor['name']}"

            )

            messages.append(

                f"✔ {vendor['name']}"

            )

        except Exception as e:

            print(e)

            messages.append(

                f"❌ {vendor['name']} Failed"

            )

    # -----------------------------
    # Result
    # -----------------------------

    if len(messages) == 0:

        return "No vendor available for negotiation."

    result = (
    "\nNegotiation Emails Sent\n\n"
    + "\n".join(messages)
    + f"\n\nTarget Price : ₹{target_price}"
)

    return result