import os
import pandas as pd


def rank_quotes(quotes):

    valid_quotes = []

    for q in quotes:

        price = q.get("price")

        if price is not None:

            valid_quotes.append(q)

    valid_quotes.sort(
        key=lambda x: x["price"]
    )

    return valid_quotes


def best_quote(quotes):

    ranked = rank_quotes(quotes)

    if ranked:

        return ranked[0]

    return None


def create_comparison_sheet(quotes):

    df = pd.DataFrame(quotes)

    os.makedirs(
        "reports",
        exist_ok=True
    )

    file_path = (
        "reports/quotation_comparison.xlsx"
    )

    df.to_excel(
        file_path,
        index=False
    )

    return file_path