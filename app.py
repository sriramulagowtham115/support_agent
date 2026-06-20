import streamlit as st

from dotenv import load_dotenv

from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response
from src.escalator import (

    should_escalate,

    generate_handoff_json

)


# --------------------------------

# Load Environment Variables

# --------------------------------

load_dotenv()


# --------------------------------

# Streamlit Configuration

# --------------------------------

st.set_page_config(

    page_title="Persona Adaptive Support Agent",

    page_icon="🤖",

    layout="wide"

)


# --------------------------------

# Title

# --------------------------------

st.title(

    "🤖 Persona Adaptive Customer Support Agent"

)


st.write(

    """

This AI assistant:

✅ Detects customer persona

✅ Retrieves answers using RAG

✅ Adapts response style

✅ Escalates sensitive issues

"""

)


# --------------------------------

# Load Pipeline

# --------------------------------

@st.cache_resource

def load_pipeline():

    pipeline = LocalRAGPipeline()


    # Load docs only once

    if (

        pipeline.collection

        .count()

        == 0

    ):

        pipeline.ingest_folder(

            "data"

        )


    return pipeline


pipeline = load_pipeline()


st.write(

    f"Documents in DB: "

    f"{pipeline.collection.count()}"

)


# --------------------------------

# User Input

# --------------------------------

user_query = st.text_area(

    "Ask your support question",

    height=120

)


# --------------------------------

# Submit

# --------------------------------

if st.button("Submit"):


    if user_query.strip() == "":


        st.warning(

            "Please enter a question."

        )


    else:


        # ------------------------

        # Persona Detection

        # ------------------------

        with st.spinner(

            "Detecting Persona..."

        ):


            persona_result = (

                classify_customer_persona(

                    user_query

                )

            )


        persona = (

            persona_result

            ["persona"]

        )


        confidence = (

            persona_result

            ["confidence"]

        )


        reasoning = (

            persona_result

            ["reasoning"]

        )


        st.subheader(

            "Detected Persona"

        )


        st.write(

            f"**Persona:** "

            f"{persona}"

        )


        st.write(

            f"**Confidence:** "

            f"{confidence}"

        )


        st.write(

            f"**Reasoning:** "

            f"{reasoning}"

        )


        st.divider()


        # ------------------------

        # RAG Retrieval

        # ------------------------

        with st.spinner(

            "Searching Knowledge Base..."

        ):


            context_chunks = (

                pipeline

                .retrieve_context(

                    user_query

                )

            )


        st.subheader(

            "Retrieved Context"

        )


        if (

            len(

                context_chunks

            )

            == 0

        ):


            st.warning(

                "No matching "

                "documents found."

            )


        else:


            for chunk in (

                    context_chunks

            ):


                st.write(

                    f"📄 Source: "

                    f"{chunk['source']}"

                )


                st.write(

                    f"Similarity "

                    f"Score: "

                    f"{chunk['score']}"

                )


                st.info(

                    chunk["text"]

                )


                st.write("---")


        # ------------------------

        # Escalation

        # ------------------------

        escalate = (

            should_escalate(

                user_query,

                context_chunks

            )

        )


        if escalate:


            st.error(

                "⚠ Escalated "

                "to Human Agent"

            )


            handoff = (

                generate_handoff_json(

                    user_query,

                    persona,

                    context_chunks

                )

            )


            st.subheader(

                "Human Handoff"

            )


            st.code(

                handoff,

                language="json"

            )


        else:


            # ------------------------

            # Response Generation

            # ------------------------

            with st.spinner(

                "Generating "

                "Response..."

            ):


                answer = (

                    generate_adaptive_response(

                        user_query,

                        persona,

                        context_chunks

                    )

                )


            st.subheader(

                "AI Response"

            )


            st.success(

                answer

            )
