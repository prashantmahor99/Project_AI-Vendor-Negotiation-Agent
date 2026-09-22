import json
import os

TRACKER_FILE = (
    "data/negotiation_rounds.json"
)


def load_rounds():

    if not os.path.exists(
        TRACKER_FILE
    ):
        return {}

    with open(
        TRACKER_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_rounds(data):

    with open(
        TRACKER_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def get_round(vendor):

    data = load_rounds()

    return data.get(
        vendor,
        0
    )


def increment_round(vendor):

    data = load_rounds()

    current = data.get(
        vendor,
        0
    )

    data[vendor] = current + 1

    save_rounds(data)

    return current + 1