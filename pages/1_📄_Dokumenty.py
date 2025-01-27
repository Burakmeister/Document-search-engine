import streamlit as st
from datetime import datetime
import service.document_service as document_service
import os
import functions

@st.dialog("Wykryto zmiany, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut)")
def vote():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tak"):
            st.session_state.vote = True
            st.rerun()
    with col2:
        if st.button("Nie"):
            st.session_state.vote = False
            st.rerun()

if 'doc_service' not in st.session_state:
    st.session_state['doc_service'] = document_service.DocumentService()

if 'mod_service' not in st.session_state:
    if st.session_state.doc_service.are_changes_in_files():
        if 'vote' not in st.session_state:
            vote()
        else:
            match st.session_state.vote:
                case True:
                    with st.spinner('Loading model...'):
                        st.session_state.mod_service = functions.get_updated_model_service(st.session_state.doc_service)
                        st.session_state.vote = False
                case False:
                    st.session_state.mod_service = functions.get_model_service(st.session_state.doc_service)
    else:
        st.session_state.mod_service = functions.get_model_service(st.session_state.doc_service)

def prev_page():
    if st.session_state.last_doc_id>30:
        st.session_state.last_doc_id-=30

def prev_disabled():
    if st.session_state.last_doc_id==30:
        return True
    return False

def next_disabled():
    if (st.session_state.last_doc_id+30)>len(docs_dict):
        return True
    return False

def next_page():
    if st.session_state.last_doc_id<30*len(docs_dict)//30:
        st.session_state.last_doc_id+=30

def open_doc(doc_name):
    os.startfile(f'{os.getcwd()}/{document_service.DocumentService.DOCS_DIR_PATH}/{doc_name}')

st.write('### Dokumenty')
uploaded_file = st.file_uploader('Dodaj dokument', type=['docs', 'txt', 'docx'])
if uploaded_file is not None:
    with open(f'{os.getcwd()}/{document_service.DocumentService.DOCS_DIR_PATH}/{uploaded_file.name}', "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Plik {uploaded_file.name} został zapisany pomyślnie!")
    if st.session_state.doc_service.are_changes_in_files():
        if 'vote' not in st.session_state:
            vote()
        match st.session_state.vote:
            case True:
                with st.spinner('Loading model...'):
                    st.session_state.mod_service = functions.get_updated_model_service(st.session_state.doc_service)
                    st.session_state.vote = False
    uploaded_file = None

if st.button('Wytrenuj nowy model'):
    with st.spinner('Loading model...'):
        st.session_state.mod_service = functions.get_updated_model_service(st.session_state.doc_service)

if 'last_doc_id' not in st.session_state:
    st.session_state.last_doc_id = 30
col1, col2, col3 = st.columns(3)
docs_dict = st.session_state.doc_service.docs_list()

col1, col2 = st.columns(2)

part_of_dict = list(docs_dict.items())[st.session_state.last_doc_id-30 : st.session_state.last_doc_id]
for doc_name, time in part_of_dict:
    col1, col2, col3 = st.columns([3, 2, 1])  # Ustaw proporcje kolumn dla lepszej szerokości
    with col1:
        st.write(doc_name)  # Wyświetl nazwę dokumentu
    with col2:
        st.write(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S"))  # Wyświetl czas w czytelnej formie
    with col3:
        st.button('Open', key=doc_name + '_open', on_click=open_doc, args=[doc_name])
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button('na początek', disabled=prev_disabled()):
        st.session_state.last_doc_id=30
        st.rerun()
with col2:
    st.button('poprzednie', on_click=prev_page, disabled=prev_disabled())
with col3:
    st.button('następne', key='prev', on_click=next_page, disabled=next_disabled())
with col4:
    if st.button('na koniec', disabled=next_disabled()):
        st.session_state.last_doc_id=30*len(docs_dict)//30
        st.rerun()

