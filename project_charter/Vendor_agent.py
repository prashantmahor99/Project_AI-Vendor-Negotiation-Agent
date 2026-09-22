import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Outlook Mail
try:
    import win32com.client
except:
    win32com = None

DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)

VENDOR_FILE = os.path.join(DATA_FOLDER, "vendors.json")
REQ_FILE = os.path.join(DATA_FOLDER, "requirement.json")


# -------------------------
# JSON Utilities
# -------------------------

def load_vendors():

    if not os.path.exists(VENDOR_FILE):
        return []

    with open(VENDOR_FILE, "r") as f:
        return json.load(f)


def save_vendors(vendors):

    with open(VENDOR_FILE, "w") as f:
        json.dump(vendors, f, indent=4)


# -------------------------
# Add Vendor
# -------------------------

def add_vendor():

    name = vendor_name.get().strip()
    email = vendor_email.get().strip()

    if not name or not email:
        messagebox.showerror(
            "Error",
            "Enter vendor details"
        )
        return

    vendors = load_vendors()

    vendors.append({
        "name": name,
        "email": email
    })

    save_vendors(vendors)

    vendor_name.delete(0, tk.END)
    vendor_email.delete(0, tk.END)

    refresh_vendor_list()

    messagebox.showinfo(
        "Success",
        "Vendor Added"
    )


# -------------------------
# Vendor List
# -------------------------

def refresh_vendor_list():

    vendor_list.delete(0, tk.END)

    vendors = load_vendors()

    for v in vendors:
        vendor_list.insert(
            tk.END,
            f"{v['name']} - {v['email']}"
        )


# -------------------------
# Save Requirement
# -------------------------

def save_requirement():

    data = {

        "product": product_entry.get(),
        "quantity": quantity_entry.get(),
        "specification": spec_text.get(
            "1.0",
            tk.END
        ),
        "budget": budget_entry.get()
    }

    with open(REQ_FILE, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo(
        "Saved",
        "Requirement Saved"
    )


# -------------------------
# RFQ Mail Sender
# -------------------------

def send_rfq():

    if win32com is None:
        messagebox.showerror(
            "Error",
            "pywin32 not installed"
        )
        return

    if not os.path.exists(REQ_FILE):
        messagebox.showerror(
            "Error",
            "Save requirement first"
        )
        return

    with open(REQ_FILE, "r") as f:
        req = json.load(f)

    vendors = load_vendors()

    if len(vendors) == 0:
        messagebox.showerror(
            "Error",
            "No vendors available"
        )
        return

    outlook = win32com.client.Dispatch(
        "Outlook.Application"
    )

    count = 0

    for vendor in vendors:

        body = f"""
Dear {vendor['name']},

Please provide your quotation.

Product : {req['product']}
Quantity : {req['quantity']}
Specification : {req['specification']}
Budget : {req['budget']}

Please share your best commercial offer.

Regards
Procurement Team
"""

        mail = outlook.CreateItem(0)

        mail.To = vendor["email"]
        mail.Subject = f"RFQ - {req['product']}"
        mail.Body = body

        mail.Send()

        count += 1

    messagebox.showinfo(
        "Success",
        f"RFQ sent to {count} vendors"
    )


# -------------------------
# UI
# -------------------------

root = tk.Tk()

root.title(
    "Vendor RFQ Automation Tool"
)

root.geometry("850x650")


# Requirement Frame

req_frame = ttk.LabelFrame(
    root,
    text="Requirement"
)

req_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

ttk.Label(
    req_frame,
    text="Product"
).grid(row=0, column=0)

product_entry = ttk.Entry(
    req_frame,
    width=40
)

product_entry.grid(row=0, column=1)

ttk.Label(
    req_frame,
    text="Quantity"
).grid(row=1, column=0)

quantity_entry = ttk.Entry(
    req_frame,
    width=20
)

quantity_entry.grid(row=1, column=1)

ttk.Label(
    req_frame,
    text="Budget"
).grid(row=2, column=0)

budget_entry = ttk.Entry(
    req_frame,
    width=20
)

budget_entry.grid(row=2, column=1)

ttk.Label(
    req_frame,
    text="Specification"
).grid(row=3, column=0)

spec_text = tk.Text(
    req_frame,
    height=6,
    width=50
)

spec_text.grid(
    row=3,
    column=1,
    pady=5
)

ttk.Button(
    req_frame,
    text="Save Requirement",
    command=save_requirement
).grid(
    row=4,
    column=1,
    pady=5
)

# Vendor Frame

vendor_frame = ttk.LabelFrame(
    root,
    text="Vendors"
)

vendor_frame.pack(
    fill="both",
    padx=10,
    pady=10
)

ttk.Label(
    vendor_frame,
    text="Vendor Name"
).grid(row=0, column=0)

vendor_name = ttk.Entry(
    vendor_frame,
    width=40
)

vendor_name.grid(
    row=0,
    column=1
)

ttk.Label(
    vendor_frame,
    text="Vendor Email"
).grid(row=1, column=0)

vendor_email = ttk.Entry(
    vendor_frame,
    width=40
)

vendor_email.grid(
    row=1,
    column=1
)

ttk.Button(
    vendor_frame,
    text="Add Vendor",
    command=add_vendor
).grid(
    row=2,
    column=1,
    pady=5
)

vendor_list = tk.Listbox(
    vendor_frame,
    width=80,
    height=10
)

vendor_list.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)

# RFQ Button

ttk.Button(
    root,
    text="Send RFQ To All Vendors",
    command=send_rfq
).pack(
    pady=20
)

refresh_vendor_list()

root.mainloop()