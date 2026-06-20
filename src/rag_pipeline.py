import os

from dotenv import load_dotenv

from google import genai

import chromadb

from pypdf import PdfReader

from src.config import (

    CHUNK_SIZE,

    CHUNK_OVERLAP,

    TOP_K

)

load_dotenv()


# --------------------------------

# Custom Text Splitter

# --------------------------------

class RecursiveCharacterTextSplitter:


    def __init__(

            self,

            chunk_size=400,

            chunk_overlap=40

    ):

        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap


    def split_text(

            self,

            text

    ):

        if not text:

            return []


        text = text.replace(

            "\r\n",

            "\n"

        )


        chunks = []

        start = 0


        while start < len(text):


            end = min(

                start +

                self.chunk_size,

                len(text)

            )


            chunk = (

                text[start:end]

                .strip()

            )


            if chunk:

                chunks.append(

                    chunk

                )


            start = (

                end -

                self.chunk_overlap

            )


            if start < 0:

                start = 0


            if end == len(text):

                break


        return chunks



# --------------------------------

# RAG Pipeline

# --------------------------------

class LocalRAGPipeline:


    def __init__(

            self,

            db_dir="./chroma_db"

    ):


        self.client = genai.Client(

            api_key=os.getenv(

                "GEMINI_API_KEY"

            )

        )


        self.chroma_client = (

            chromadb.PersistentClient(

                path=db_dir

            )

        )


        self.collection = (

            self.chroma_client

            .get_or_create_collection(

                name="support_kb"

            )

        )


    # --------------------------------

    # Embeddings

    # --------------------------------

    def get_embedding(

            self,

            text

    ):


        response = (

            self.client.models

            .embed_content(

                model="gemini-embedding-001",

                contents=text

            )

        )


        return (

            response

            .embeddings[0]

            .values

        )


    # --------------------------------

    # Read txt/md

    # --------------------------------

    def read_text_file(

            self,

            filepath

    ):


        with open(

                filepath,

                "r",

                encoding="utf-8"

        ) as f:


            return f.read()


    # --------------------------------

    # Read PDF

    # --------------------------------

    def read_pdf(

            self,

            filepath

    ):


        if (

            os.path.getsize(

                filepath

            ) == 0

        ):


            print(

                f"Skipping "

                f"{filepath}"

            )


            return ""


        reader = PdfReader(

            filepath

        )


        text = ""


        for page in reader.pages:


            extracted = (

                page.extract_text()

            )


            if extracted:

                text += (

                    extracted +

                    "\n"

                )


        return text


    # --------------------------------

    # Ingest Document

    # --------------------------------

    def ingest_document(

            self,

            doc_name,

            content

    ):


        if content.strip() == "":

            return


        splitter = (

            RecursiveCharacterTextSplitter(

                chunk_size=CHUNK_SIZE,

                chunk_overlap=CHUNK_OVERLAP

            )

        )


        chunks = (

            splitter

            .split_text(

                content

            )

        )


        for idx, chunk in enumerate(

                chunks

        ):


            embedding = (

                self.get_embedding(

                    chunk

                )

            )


            chunk_id = (

                f"{doc_name}"

                f"_chunk_{idx}"

            )


            try:


                self.collection.add(

                    ids=[

                        chunk_id

                    ],

                    embeddings=[

                        embedding

                    ],

                    metadatas=[

                        {

                            "source":

                            doc_name,

                            "chunk_index":

                            idx

                        }

                    ],

                    documents=[

                        chunk

                    ]

                )


            except:

                pass


    # --------------------------------

    # Ingest Folder

    # --------------------------------

    def ingest_folder(

            self,

            folder="data"

    ):


        files = os.listdir(

            folder

        )


        for file in files:


            filepath = (

                os.path.join(

                    folder,

                    file

                )

            )


            print(

                "Loading:",

                file

            )


            text = ""


            if (

                file.endswith(

                    ".txt"

                )

                or

                file.endswith(

                    ".md"

                )

            ):


                text = (

                    self

                    .read_text_file(

                        filepath

                    )

                )


            elif file.endswith(

                    ".pdf"

            ):


                text = (

                    self

                    .read_pdf(

                        filepath

                    )

                )


            self.ingest_document(

                file,

                text

            )


        print(

            "Knowledge Base Loaded"

        )


    # --------------------------------

    # Retrieve Context

    # --------------------------------

    def retrieve_context(

            self,

            query,

            top_k=TOP_K

    ):


        query_vector = (

            self.get_embedding(

                query

            )

        )


        results = (

            self.collection.query(

                query_embeddings=[

                    query_vector

                ],

                n_results=top_k

            )

        )


        retrieved_items = []


        if (

            results

            and

            results["documents"]

        ):


            for i in range(

                len(

                    results["documents"][0]

                )

            ):


                distance = 0


                if (

                    results

                    .get(

                        "distances"

                    )

                ):


                    distance = (

                        results

                        ["distances"]

                        [0][i]

                    )


                score = round(

                    1 -

                    distance,

                    3

                )


                retrieved_items.append(

                    {

                        "text":

                        results

                        ["documents"]

                        [0][i],


                        "source":

                        results

                        ["metadatas"]

                        [0][i]

                        ["source"],


                        "score":

                        score

                    }

                )


        return retrieved_items