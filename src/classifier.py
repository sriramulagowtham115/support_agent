def classify_customer_persona(user_message):

    msg = user_message.lower()


    technical_keywords = [

        "api",

        "token",

        "401",

        "database",

        "header",

        "authorization",

        "config",

        "error",

        "logs",

        "bearer"

    ]


    business_keywords = [

        "timeline",

        "business",

        "roi",

        "uptime",

        "operational",

        "revenue",

        "deadline"

    ]


    frustrated_keywords = [

        "not working",

        "urgent",

        "nothing",

        "frustrated",

        "immediately",

        "angry",

        "hour",

        "problem",

        "issue"

    ]


    if any(

        word in msg

        for word in technical_keywords

    ):

        return {

            "persona":

            "Technical Expert",

            "confidence":

            0.95,

            "reasoning":

            "Technical keywords detected."

        }


    elif any(

        word in msg

        for word in business_keywords

    ):

        return {

            "persona":

            "Business Executive",

            "confidence":

            0.95,

            "reasoning":

            "Business-related keywords detected."

        }


    elif any(

        word in msg

        for word in frustrated_keywords

    ):

        return {

            "persona":

            "Frustrated User",

            "confidence":

            0.95,

            "reasoning":

            "Emotional or urgent language detected."

        }


    else:

        return {

            "persona":

            "Technical Expert",

            "confidence":

            0.50,

            "reasoning":

            "Default classification."

        }



# ----------------------------
# TEST
# ----------------------------

if __name__ == "__main__":

    msg = """

Our production API returns

401 Unauthorized.

Please check logs.

"""

    result = classify_customer_persona(msg)

    print(result)