from datetime import datetime
from data_manager import save_rfq


def create_rfq(product,
               quantity,
               specification,
               budget):

    rfq_id = (
        f"RFQ-"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    rfq = {

        "rfq_id": rfq_id,
        "product": product,
        "quantity": quantity,
        "specification": specification,
        "budget": budget,
        "status": "OPEN"
    }

    save_rfq(rfq)

    return rfq