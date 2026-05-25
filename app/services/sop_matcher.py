SOPS = {
    "pricing": {
        "keywords": ["price", "pricing", "quote", "cost"],
        "response": "Thank you for your pricing enquiry. Our team will contact you shortly.",
    },
    "booking": {
        "keywords": ["book", "appointment", "schedule"],
        "response": "We can help schedule your appointment.",
    },
    "complaint": {
        "keywords": ["complaint", "issue", "angry", "bad"],
        "response": "We are sorry for the inconvenience caused.",
    },
    "support": {
        "keywords": ["help", "support"],
        "response": "Our support team will assist you shortly.",
    },
    "after_hours": {
        "keywords": ["tomorrow", "later"],
        "response": "Our team will reconnect during working hours.",
    },
}


def match_sop(message: str):

    message = message.lower()

    for sop_name, sop_data in SOPS.items():

        for keyword in sop_data["keywords"]:

            if keyword in message:

                return {
                    "matched": True,
                    "sop": sop_name,
                    "response": sop_data["response"],
                }

    return {"matched": False}
