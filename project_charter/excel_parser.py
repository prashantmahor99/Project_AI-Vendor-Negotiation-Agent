import pandas as pd
import re


def extract_excel_quote(file_path):

    try:

        df = pd.read_excel(
            file_path
        )

        text = df.astype(
            str
        ).to_string()

        prices = re.findall(
            r"\d+(?:,\d+)*(?:\.\d+)?",
            text
        )

        price = None

        if prices:

            values = []

            for p in prices:

                try:
                    values.append(
                        float(
                            p.replace(",", "")
                        )
                    )
                except:
                    pass

            if values:
                price = max(values)

        return {

            "file": file_path,
            "price": price
        }

    except Exception as e:

        return {

            "file": file_path,
            "error": str(e)
        }