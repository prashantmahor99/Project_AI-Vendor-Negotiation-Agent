# reports/comparison_generator.py

def generate_comparison(quotes):
    """
    quotes = [
        {
            "vendor": "ABC",
            "price": 25000,
            "file": "abc.pdf"
        }
    ]
    """

    valid_quotes = []

    for q in quotes:

        try:

            price = float(
                str(q.get("price", 0))
                .replace(",", "")
                .replace("₹", "")
                .strip()
            )

            valid_quotes.append({

                "vendor": q.get("vendor", "Unknown"),

                "price": price,

                "file": q.get("file", "")

            })

        except:

            continue

    # Lowest price first
    valid_quotes.sort(
        key=lambda x: x["price"]
    )

    # L1 L2 L3...
    for index, item in enumerate(valid_quotes):

        item["rank"] = f"L{index+1}"

    return valid_quotes