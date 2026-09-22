import json
import os

FILE = "body_quotes.json"


def load_quotes():

    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


def save_quote(vendor, price):

    quotes = load_quotes()

    updated = False

    # Same vendor already exists?
    for q in quotes:

        if q["vendor"].strip().lower() == vendor.strip().lower():

            q["price"] = price
            q["source"] = "Email Body"

            updated = True
            break

    # New vendor
    if not updated:

        quotes.append({

            "vendor": vendor,

            "price": price,

            "source": "Email Body"

        })

    with open(FILE, "w", encoding="utf-8") as f:

        json.dump(

            quotes,

            f,

            indent=4
        )


def clear_quotes():

    with open(FILE, "w", encoding="utf-8") as f:

        json.dump([], f, indent=4)