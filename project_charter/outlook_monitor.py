from body_quotes import save_quote
import win32com.client
import pythoncom
import pywintypes
import time
import re
import os




DOWNLOAD_FOLDER = "quotations"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ----------------------------------------------------
# Remove Reply History
# ----------------------------------------------------

def clean_body(body):

    if not body:
        return ""

    stop_words = [
        "On ",
        "From:",
        "-----Original Message-----",
        "________________________________",
        # "CAUTION:",
        # "Sent:",
        # "Subject:",
        # "To:",
        # "Cc:"
    ]

    text = body

    for word in stop_words:

        pos = text.find(word)

        if pos != -1:
            text = text[:pos]

    return text.strip()


# ----------------------------------------------------
# Extract Price
# ----------------------------------------------------

def extract_price_from_body(body):

    if not body:
        return None

    body = clean_body(body)

    print("\nSearching Price...")
    print("--------------------------------")

    patterns = [

        r"unit\s*price\s*[:=\-]?\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"quoted\s*price\s*[:=\-]?\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"final\s*price\s*[:=\-]?\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"price\s*[:=\-]?\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"₹\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)",

        r"inr\s*(\d+(?:,\d+)*(?:\.\d+)?)"

    ]

    for line in body.splitlines():

        line = line.strip()

        if not line:
            continue

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                value = match.group(1).replace(",", "")

                try:

                    price = float(value)

                    print("Price Found :", price)

                    return price

                except:
                    pass

    print("No Price Found")

    return None


# ----------------------------------------------------
# Scan Inbox
# ----------------------------------------------------

def scan_inbox_for_rfq():

    pythoncom.CoInitialize()

    try:

        print("=" * 60)
        print("Scanning Outlook Inbox")
        print("=" * 60)

        # Retry Outlook Connection
        outlook = None

        for _ in range(5):

            try:
                outlook = win32com.client.Dispatch("Outlook.Application")
                break

            except pywintypes.com_error:
                print("Waiting Outlook...")
                time.sleep(2)

        if outlook is None:
            print("Unable to connect Outlook")
            return []

        namespace = outlook.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6)

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        downloaded = []

        total = min(messages.Count, 100)

        print(f"Checking Latest {total} Emails\n")

        for i in range(1, total + 1):

            try:

                msg = messages.Item(i)

            except pywintypes.com_error:

                continue

            try:

                if not msg.UnRead:
                    continue

                subject = str(msg.Subject or "").strip()
                

                subject_upper = subject.upper()

                while subject_upper.startswith(("RE:", "FW:", "FWD:")):
                    subject_upper = subject_upper.split(":", 1)[1].strip()

                if "RFQ-" not in subject_upper:

                    continue

                body = str(msg.Body or "")

                print("\nRFQ MAIL FOUND")

                print(subject)

                print("=" * 80)
                print("BODY START")
                print(body)
                print("BODY END")
                print("=" * 80)

                

                try:
                    vendor = str(msg.SenderEmailAddress).lower().strip()
                except:
                    vendor = str(msg.SenderName).lower().strip()

                vendor = vendor.replace("@", "_").replace(".", "_")

                attachment_count = msg.Attachments.Count

                print("Vendor :", vendor)
                print("Attachments :", attachment_count)

                print("Vendor =", vendor)

                # ---------------- BODY ----------------

                if attachment_count == 0:

                    print("Attachment nahi mila.")
                    
                    print("Price Extract Kar Raha Hu...")

                   
                    price = extract_price_from_body(body)

                    body = clean_body(body)

                    print("\nAFTER CLEAN BODY")
                    print("--------------------------------")
                    print(body)
                    print("--------------------------------")

                    if price is not None:

                        print("Saving Quote...")

                        save_quote(vendor, price)

                        downloaded.append({
                            "vendor": vendor,
                            "price": price,
                            "source": "Body"
                        })

                        print("Price Saved :", price)

                    else:

                        print("No Price Found")

                    msg.UnRead = False
                    msg.Save()

                    continue

                # ---------------- ATTACHMENTS ----------------

                for j in range(1, attachment_count + 1):

                    attachment = msg.Attachments.Item(j)

                    filename = f"{vendor}_{attachment.FileName}"

                    if not filename.lower().endswith(
                        (".pdf", ".xls", ".xlsx")
                    ):
                        continue

                    save_path = os.path.join(
                        DOWNLOAD_FOLDER,
                        filename
                    )

                    if not os.path.exists(save_path):

                        attachment.SaveAsFile(
                            os.path.abspath(save_path)
                        )

                        print("Downloaded :", filename)

                    downloaded.append({
                        "vendor": vendor,
                        "file": save_path,
                        "source": "Attachment"
                    })

                msg.UnRead = False
                msg.Save()

            except Exception as e:

                print("Mail Error :", e)

                continue

        print("=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print("New Quotations :", len(downloaded))
        print("=" * 60)

        return downloaded

    finally:

        pythoncom.CoUninitialize()