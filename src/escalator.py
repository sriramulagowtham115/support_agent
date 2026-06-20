import json

from src.config import (

    CONFIDENCE_THRESHOLD,

    SENSITIVE_KEYWORDS

)


# --------------------------------

# Sensitive Topic Check

# --------------------------------

def contains_sensitive_topic(

        user_query: str

):

    query = user_query.lower()


    for keyword in SENSITIVE_KEYWORDS:


        if keyword in query:


            return True


    return False


# --------------------------------

# Low Confidence Check

# --------------------------------

def is_low_confidence(

        user_query,

        context_chunks

):


    # Greetings like Hello, Hi

    if len(

            context_chunks

    ) == 0:


        if len(

                user_query

                .split()

        ) <= 2:


            return False


        return True


    best_score = max(

        [

            c["score"]

            for c in context_chunks

        ]

    )


    return (

        best_score

        <

        CONFIDENCE_THRESHOLD

    )


# --------------------------------

# Repeated Frustration

# --------------------------------

def repeated_frustration(

        frustration_count

):


    if frustration_count >= 3:


        return True


    return False


# --------------------------------

# Master Escalation Checker

# --------------------------------

def should_escalate(

        user_query,

        context_chunks,

        frustration_count=0

):


    # Billing / Refund

    if contains_sensitive_topic(

            user_query

    ):


        return True


    # Low Retrieval Confidence

    if is_low_confidence(

            user_query,

            context_chunks

    ):


        return True


    # Repeated frustration

    if repeated_frustration(

            frustration_count

    ):


        return True


    return False


# --------------------------------

# Human Handoff JSON

# --------------------------------

def generate_handoff_json(

        user_query,

        persona,

        context_chunks

):


    handoff = {


        "persona":

        persona,


        "detected_issue":

        user_query,


        "retrieved_sources":

        [

            c["source"]

            for c in context_chunks

        ],


        "confidence_score":

        max(

            [

                c["score"]

                for c in context_chunks

            ],

            default=0

        ),


        "recommended_action":

        """

Review logs

Verify billing/payment records

Contact customer directly

"""

    }


    return json.dumps(

        handoff,

        indent=4

    )



# --------------------------------

# TEST

# --------------------------------

if __name__ == "__main__":


    query = """

I was charged twice.

I want refund immediately.

"""


    context = [

        {

            "source":

            "billing_policy.txt",


            "score":

            0.85

        }

    ]


    print(

        should_escalate(

            query,

            context

        )

    )


    print(

        generate_handoff_json(

            query,

            "Frustrated User",

            context

        )

    )