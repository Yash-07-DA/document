import streamlit as st
from openai import OpenAI

st.title("📄 Document question answering")

st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "You need an OpenAI API key."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

else:

    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)",
        type=("txt", "md")
    )

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        document = uploaded_file.read().decode()

        prompt = f"""
Here is a document:

{document}

----------------

Question: {question}
"""

        try:

            stream = client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
                stream=True,
            )

            def stream_text():
                for event in stream:
                    if event.type == "response.output_text.delta":
                        yield event.delta
                    elif event.type == "response.error":
                        yield f"Error: {event.error}"

            st.write_stream(stream_text)

        except Exception as e:
            st.error(str(e))
