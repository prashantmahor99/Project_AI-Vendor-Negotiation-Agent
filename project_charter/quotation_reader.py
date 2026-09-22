import os

from pdf_parser import extract_pdf_quote
from excel_parser import extract_excel_quote
from body_quotes import load_quotes

QUOTATION_FOLDER = "quotations"


def read_all_quotes():

    if not os.path.exists(QUOTATION_FOLDER):
        return []

    quotes = {}

    # -------------------------------
    # PDF / Excel Quotes
    # -------------------------------

    for file in os.listdir(QUOTATION_FOLDER):

        path = os.path.join(QUOTATION_FOLDER, file)

        if file.lower().endswith(".pdf"):
            quote = extract_pdf_quote(path)

        elif file.lower().endswith((".xlsx", ".xls")):
            quote = extract_excel_quote(path)

        else:
            continue

        if not quote:
            continue

        price = quote.get("price")

        if price in (None, "", 0):
            continue

        vendor = quote.get("vendor")

        if not vendor:
            vendor = os.path.splitext(file)[0].split("_quote")[0]

        quotes[vendor.lower()] = {
            "vendor": vendor,
            "price": float(price),
            "file": file
        }

    # -------------------------------
    # Email Body Quotes
    # -------------------------------

    body_quotes = load_quotes()

    print("\nBody Quotes :", body_quotes)

    for q in body_quotes:

        vendor = q.get("vendor", "").strip()

        price = q.get("price")

        if not vendor:
            continue

        if price in (None, "", 0):
            continue

        quotes[vendor.lower()] = {
            "vendor": vendor,
            "price": float(price),
            "file": "Email Body"
        }

    results = list(quotes.values())

    results.sort(key=lambda x: x["price"])

    print("\nFinal Quotes :", results)

    return results

    results = list(quotes.values())

    print("="*60)
    print("READ_ALL_QUOTES RESULT")
    print(results)
    print("="*60)

    results.sort(key=lambda x: x["vendor"].lower())

    return results    