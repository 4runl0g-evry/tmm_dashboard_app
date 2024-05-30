import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain.llms import HuggingFaceHub
from util import *

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def display_checkbox_get_updated_list_chat_pdf(checkbox_dicts,suffix):
    # print(checkbox_dicts)
    # main_checkboxes = [st.checkbox(label=":blue-background[Select All / Deselect All]",key={suffix})]
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    # # Display individual checkboxes based on the states
    for checkbox_dict in checkbox_dicts:
        for key in checkbox_dict:
            checkbox_dict[key] = st.checkbox(key, checkbox_dict[key])
    df = pd.DataFrame.from_dict(checkbox_dict, orient='index',columns=['AREAS'])
    df.reset_index(inplace=True)
    df.columns = ['AREAS','CHECK']
    df["MAJOR"] = suffix
    desired_order = ['CHECK','MAJOR','AREAS']
    df_reordered = df[desired_order]
    # print(df_reordered)
    return df_reordered

def show_major_expander_chat_pdf():
        st.write("Current Metrics Data. Click 'Update' button to SelectAll")
    # if button_clicked:
        list = [{'Impact Analysis of enhancment/defect/CR/feature O': False, 
                'Grooming/Working Sessions with BA O': False, 
                'Querylog/Clarification log Updation O': False, 
                'Define Testing Entry/ExitCriteria O': False, 
                'Freeze Requirement and Acceptance Criteria O': False}]
        with st.expander(label="Risk Management",expanded=True):
            col1, col2 = st.columns([8,2])
            with col1:
                updated_df = display_checkbox_get_updated_list_chat_pdf(list, "Risk Management")
                # updated_unchecked_df = get_updated_uncheckbox_df(updated_df)
                df_percent = calculate_percentage(updated_df)
            with col2:
                st.write(generate_color_bar(df_percent, "small"), unsafe_allow_html=True)

def show_major_expander_chat_pdf_post_update():
    # if button_clicked:
        list = [{'Impact Analysis of enhancment/defect/CR/feature U': True, 
                'Grooming/Working Sessions with BA U': True, 
                'Querylog/Clarification log Updation U': True, 
                'Define Testing Entry/ExitCriteria U': True, 
                'Freeze Requirement and Acceptance Criteria U': True}]
        with st.expander(label="Risk Management",expanded=True):
            col1, col2 = st.columns([8,2])
            with col1:
                updated_df = display_checkbox_get_updated_list_chat_pdf(list, "Risk Management UP")
                # updated_unchecked_df = get_updated_uncheckbox_df(updated_df)
                df_percent = calculate_percentage(updated_df)
            with col2:
                st.write(generate_color_bar(df_percent, "small"), unsafe_allow_html=True)
    
def update_action():
    st.spinner("Updating Assessment Metrics...")

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.chat_message("user").write(message.content)
            # st.write(user_template.replace(
            #     "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.chat_message("assistant").write(message.content)
            # st.write(bot_template.replace(
            #     "{{MSG}}", message.content), unsafe_allow_html=True)
    if st.button("Update"):
        update_action()
        show_major_expander_chat_pdf_post_update()
    else:
        show_major_expander_chat_pdf()

def chat_with_pdf():
    load_dotenv()
    # st.set_page_config(page_title="Chat with multiple PDFs",
    #                    page_icon=":books:")
    # st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.subheader("Chat with Multiple PDFs :books:")
    # with st.sidebar:
    # st.subheader("Your documents")
    pdf_docs = st.file_uploader(
            "Upload requiremnets PDFs here and click on 'Scan PDF'", accept_multiple_files=True)
    if st.button(':green[Scan all PDFs]'):
        with st.spinner("Scanning :coffee:"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # create vector store
                vectorstore = get_vectorstore(text_chunks)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                st.write("Scan completed :white_check_mark:")

    user_question = st.text_input("Ask a question about uploaded PDFs:")
    if user_question:
        handle_userinput(user_question)

    
    