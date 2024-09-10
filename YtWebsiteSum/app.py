import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from dotenv import load_dotenv
import os

load_dotenv()

#Stremlit app
st.set_page_config(page_title="Langchain summarize YT video or website.")
st.title("Summarize yt video or text from website.")
st.subheader("Summarize URL")

# get key and url to be summarized
with st.sidebar:
    open_ai_key = st.text_input("OpenAI key", value="", type="password")

generic_url=st.text_input("URL", label_visibility="collapsed")

llm=ChatOpenAI(api_key=open_ai_key, model="gpt-4o-mini")

prompt_temlate = """
Provide summary of the following content in 300 words: 
Content: {text}
"""

prompt = PromptTemplate(template=prompt_temlate, input_variables=["text"])


if st.button("Summarize the content from URL"):
    ## Validate inputs
    if not open_ai_key.strip()or not generic_url.strip():
        st.error("Please provide the information")
    elif not validators.url(generic_url):
        st.error("Please enter valid url. It can be youtube or website url.")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website data or yt video
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url],ssl_verify=False)
                    
                docs=loader.load()
                docs

                #Chain for summ
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                out_put_summary=chain.run(docs)

                st.success(out_put_summary)
        except Exception as e:
            st.exception(f"Exception",{e})