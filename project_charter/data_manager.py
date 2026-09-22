import json
import os

# -------------------------------
# Data Folder
# -------------------------------

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

VENDOR_FILE = os.path.join(DATA_DIR, "vendors.json")
RFQ_FILE = os.path.join(DATA_DIR, "rfqs.json")


# -------------------------------
# Common JSON Functions
# -------------------------------

def load_json(file_path):

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file_path, data):

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# -------------------------------
# Vendor Functions
# -------------------------------

def get_vendors():

    return load_json(VENDOR_FILE)


def save_vendor(vendor):

    vendors = get_vendors()

    # Duplicate Email Check
    for v in vendors:

        if v["email"].strip().lower() == vendor["email"].strip().lower():

            print("Vendor already exists.")

            return

    vendors.append(vendor)

    save_json(VENDOR_FILE, vendors)


def clear_vendors():

    save_json(VENDOR_FILE, [])


# -------------------------------
# RFQ Functions
# -------------------------------

def get_rfqs():

    return load_json(RFQ_FILE)


def save_rfq(rfq):

    rfqs = get_rfqs()

    rfqs.append(rfq)

    save_json(RFQ_FILE, rfqs)


def clear_rfqs():

    save_json(RFQ_FILE, [])