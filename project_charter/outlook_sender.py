import win32com.client
import pythoncom


def send_rfq_email(vendor_email, vendor_name, rfq):

    pythoncom.CoInitialize()

    outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)

    mail.To = vendor_email

    mail.Subject = (
        f"{rfq['rfq_id']} | "
        f"{rfq['product']}"
    )

    mail.Body = f"""
Dear {vendor_name},

Please share your quotation.

RFQ Number:
{rfq['rfq_id']}

Product:
{rfq['product']}

Quantity:
{rfq['quantity']}

Specification:
{rfq['specification']}

Budget:
{rfq['budget']}

Regards,
Procurement Team
"""

    mail.Send()


# -------------------------------------------------------
# Negotiation Mail
# -------------------------------------------------------

def send_negotiation_email(
        email,
        vendor_name,
        target_price,
        rfq_number
):

    outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)

    mail.To = email

    mail.Subject = f"{rfq_number} | Price Revision"

    mail.Body = f"""
Dear {vendor_name},

Thank you for your quotation.

We request you to review your commercial offer and provide your best possible pricing.

Target Price:
₹{target_price}

Kindly reply to this email with your revised quotation.

Regards,
Procurement Team
"""

    mail.Send()