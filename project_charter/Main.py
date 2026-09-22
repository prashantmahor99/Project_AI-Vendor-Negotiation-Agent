import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from data_manager import (
    save_vendor,
    get_vendors
)


import threading
import os
from procurement_workflow import start_procurement
import procurement_workflow



root = tk.Tk()

root.title(
    "Vendor Negotiator"
)

root.geometry("900x700")

# -------------------------
# Vendor Section
# -------------------------

vendor_frame = ttk.LabelFrame(
    root,
    text="Vendor Management"
)

vendor_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

ttk.Label(
    vendor_frame,
    text="Vendor Name"
).grid(
    row=0,
    column=0
)

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
    text="Email"
).grid(
    row=1,
    column=0
)

vendor_email = ttk.Entry(
    vendor_frame,
    width=40
)

vendor_email.grid(
    row=1,
    column=1
)

vendor_list = tk.Listbox(
    vendor_frame,
    width=80,
    height=6
)

vendor_list.grid(
    row=3,
    column=0,
    columnspan=2
)


def refresh_vendors():

    vendor_list.delete(
        0,
        tk.END
    )

    for vendor in get_vendors():

        vendor_list.insert(
            tk.END,
            f"{vendor['name']} "
            f"({vendor['email']})"
        )


def add_vendor():

    name = vendor_name.get()

    email = vendor_email.get()

    save_vendor({

        "name": name,
        "email": email
    })

    refresh_vendors()

    vendor_name.delete(
        0,
        tk.END
    )

    vendor_email.delete(
        0,
        tk.END
    )


ttk.Button(
    vendor_frame,
    text="Add Vendor",
    command=add_vendor
).grid(
    row=2,
    column=1
)

# -------------------------
# RFQ Section
# -------------------------

rfq_frame = ttk.LabelFrame(
    root,
    text="Create RFQ"
)

rfq_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

ttk.Label(
    rfq_frame,
    text="Product"
).grid(
    row=0,
    column=0
)

product_entry = ttk.Entry(
    rfq_frame,
    width=40
)

product_entry.grid(
    row=0,
    column=1
)

ttk.Label(
    rfq_frame,
    text="Quantity"
).grid(
    row=1,
    column=0
)

quantity_entry = ttk.Entry(
    rfq_frame,
    width=20
)

quantity_entry.grid(
    row=1,
    column=1
)

ttk.Label(
    rfq_frame,
    text="Budget"
).grid(
    row=2,
    column=0
)

budget_entry = ttk.Entry(
    rfq_frame,
    width=20
)

budget_entry.grid(
    row=2,
    column=1
)

ttk.Label(
    rfq_frame,
    text="Specification"
).grid(
    row=3,
    column=0
)

spec_text = tk.Text(
    rfq_frame,
    height=6,
    width=50
)

spec_text.grid(
    row=3,
    column=1
)


workflow_thread = None
final_report = None


def run_workflow():

    global final_report

    try:

        final_report = start_procurement(

            product_entry.get(),

            quantity_entry.get(),

            spec_text.get("1.0", tk.END),

            budget_entry.get(),

            status_callback=update_status,

            log_callback=update_log

        )

    except Exception as e:

        import traceback

        error = traceback.format_exc()

        print(error)

        update_status("❌ ERROR")

        update_log(error)

        messagebox.showerror(
            "Workflow Error",
            str(e)
        )


def start_workflow():

    global workflow_thread

    workflow_thread = threading.Thread(
        target=run_workflow,
        daemon=True
    )

    workflow_thread.start()

    messagebox.showinfo(
        "Started",
        "Procurement Started."
    )


def stop_workflow():

    procurement_workflow.stop_procurement()

    update_status("🛑 Procurement Stop Requested...")

    messagebox.showinfo(

        "Stopped",

        "Procurement will stop after current operation."

    )

def open_report():

    global final_report

    if final_report and os.path.exists(final_report):

        report_path = os.path.abspath(final_report)

        print(report_path)

        os.startfile(report_path)

    else:

        messagebox.showwarning(

            "Report",

            "Final report not generated."

        )


refresh_vendors()

  
def clear_all_vendors():

    if messagebox.askyesno(

        "Confirm",

        "Delete all vendors?"

    ):

        from data_manager import clear_vendors

        clear_vendors()

        refresh_vendors()

        messagebox.showinfo(

            "Success",

            "All vendors deleted."

        )

ttk.Button(

    vendor_frame,

    text="🗑 Clear Vendors",

    command=clear_all_vendors

).grid(

    row=2,

    column=0,

    padx=5,

    pady=5
)
ttk.Button(

    root,

    text="▶ Start Procurement",

    command=start_workflow

).pack(pady=8)


ttk.Button(

    root,

    text="⏹ Stop Procurement",

    command=stop_workflow

).pack(pady=8)


ttk.Button(

    root,

    text="📋 Live Status",

    command=lambda: messagebox.showinfo(
        "Status",
        "Workflow Running..."
    )

).pack(pady=8)


ttk.Button(

    root,

    text="📄 Open Final Report",

    command=open_report

).pack(pady=8)

   

status_box = tk.Text(
    root,
    height=10,
    width=100
)

status_box.pack(pady=10)

def update_status(text):

    status_box.insert(
        tk.END,
        text + "\n"
    )

    status_box.see(tk.END)

def update_log(text):

    status_box.insert(
        tk.END,
        "[LOG] " + text + "\n"
    )

    status_box.see(tk.END) 


root.mainloop()