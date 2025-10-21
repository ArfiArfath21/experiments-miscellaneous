import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import bot_template, user_template, css
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.llms import HuggingFaceHub
import datetime
from audiorecorder import audiorecorder
from langchain.llms import self_hosted_hugging_face

# self_hosted_hugging_face()

from transformers import pipeline
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "API TOKEN HERE"
import openai
# api_key = ""
open_ai_base = "https://llm.ask.psbodhi.ai/chat-13b-v1/v1"
open_ai_key="EMPTY"
model = "askbodhi/chat-13B-v1.0"
llm = ChatOpenAI(openai_api_base=open_ai_base, 
                 openai_api_key=open_ai_key, 
                 model=model)#,
                #  max_tokens = 100)

def get_pdf_text(pdf_files):
    
    text = ""
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_chunk_text(text):
    
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len
    )

    chunks = text_splitter.split_text(text)

    return chunks


def get_vector_store(data):
    
    # For OpenAI Embeddings
    # embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    # For Huggingface Embeddings
    embeddings = HuggingFaceInstructEmbeddings(model_name = "/Users/arfsyed/Documents/Development/eats/eats-recommendation-with-network-1/model_t5")
    # vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    vectorstore = FAISS.from_documents(data, embedding = embeddings)
    return vectorstore


def get_conversation_chain(vector_store):
    
    # OpenAI Model
    # llm = ChatOpenAI(openai_api_key=api_key, openai_api_base=api_base, model=model)

    # HuggingFace Model
    # model_name = "Xenova/LaMini-Flan-T5-783M"
    # model_name = "google/flan-t5-xxl" # WORKING
    # model_name = "NousResearch/Llama-2-13b-hf" # NO RESULTS
    # model_name = "bigscience/T0pp"
    # llm = HuggingFaceHub(repo_id=model_name, model_kwargs={"temperature":0.5, "max_tokens":100})
    # llm = HuggingFaceHub("/Users/arfsyed/Downloads/langchain-chatbot-multiple-PDF-master/topp_model/T0pp")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain

def handle_user_input(question):

    response = st.session_state.conversation({'question':question})
    print(response)
    print("&&"*10)
    print(st.session_state.chat_history)
    print("=-"*10)
    st.session_state.chat_history = response['chat_history']
    print(st.session_state.chat_history)
    print("**"*10)

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title='Chat with Your own PDFs', page_icon=':books:')
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header('Chat with Your own PDFs :books:')
    question = st.text_input("Ask anything to your PDF: ")
    # audio = audiorecorder("Record", "Stop")

    if question:
        handle_user_input(question)
    # elif audio:
    #     print("in here")
    #     audio.export("audio.wav", format="wav")
    #     audio_file= open("audio.wav", "rb")
    #     os.system("rm -f audio.wav")
    #     transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en")
    #     question = transcript["text"]
    #     handle_user_input(question)


    with st.sidebar:
        st.subheader("Upload your Documents Here: ")
        pdf_files = st.file_uploader("Choose your PDF Files and Press OK", type=['pdf'], accept_multiple_files=True)

        if st.button("OK"):
            with st.spinner("Processing your PDFs..."):

                # Get PDF Text
                raw_text = get_pdf_text(pdf_files)
                # Get Text Chunks
                text_chunks = get_chunk_text(raw_text)
                
                # Create Vector Store
                # for csv data
                data = CSVLoader(file_path="/Users/arfsyed/Documents/Development/Hackathon/input_files/lakmeindia-products.csv", 
                                encoding="utf-8",csv_args={'delimiter': ','}).load()
                # vector_store = get_vector_store(text_chunks)
                vector_store = get_vector_store(data)
                before = datetime.datetime.now()
                print(datetime.datetime.now() - before)
                st.write("DONE")
                # Create conversation chain
                st.session_state.conversation =  get_conversation_chain(vector_store)


if __name__ == '__main__':
    main()
