import pdfplumber
import re


def extract_pdf_quote(pdf_file):

    try:

        text = ""

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

        price = None

        prices = re.findall(
            r"\d+(?:,\d+)*(?:\.\d+)?",
            text
        )

        if prices:

            numeric_prices = []

            for p in prices:

                try:
                    numeric_prices.append(
                        float(
                            p.replace(",", "")
                        )
                    )
                except:
                    pass

            if numeric_prices:
                price = max(numeric_prices)

        return {
            "file": pdf_file,
            "price": price,
            "content": text[:1000]
        }

    except Exception as e:

        return {
            "file": pdf_file,
            "error": str(e)
        }