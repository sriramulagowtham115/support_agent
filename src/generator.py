def generate_adaptive_response(

        user_query,

        persona,

        context_chunks

):

    """
    Generate persona-aware response
    using retrieved context.
    """


    # No context found

    if len(context_chunks) == 0:

        return (

            "Sorry, I could not "

            "find relevant "

            "information in "

            "the knowledge base."

        )


    answer = ""


    # ----------------------------

    # Persona Style

    # ----------------------------

    if persona == "Technical Expert":

        answer += (

            "### Technical Analysis\n\n"

        )


    elif persona == "Frustrated User":

        answer += (

            "I understand this "

            "can be frustrating.\n\n"

            "Please try the "

            "following:\n\n"

        )


    else:

        answer += (

            "### Business Summary\n\n"

        )


    # ----------------------------

    # Add Context

    # ----------------------------

    for chunk in context_chunks:


        answer += (

            f"**Source:** "

            f"{chunk['source']}\n\n"

        )


        answer += (

            chunk["text"]

        )


        answer += "\n\n"


    return answer



# ----------------------------

# TEST

# ----------------------------

if __name__ == "__main__":


    query = """

How do I fix

401 Unauthorized?

"""


    persona = (

        "Technical Expert"

    )


    context = [

        {

            "source":

            "api_troubleshooting.md",


            "text":

            """

401 Unauthorized

Possible reasons:

1. Invalid API Key

2. Missing Authorization Header

3. Expired Bearer Token

Verify your API key and token.

""",


            "score":

            0.89

        }

    ]


    result = (

        generate_adaptive_response(

            query,

            persona,

            context

        )

    )


    print(result)