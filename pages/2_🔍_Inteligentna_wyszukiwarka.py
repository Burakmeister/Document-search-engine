import streamlit as st
import functions
import service.document_service as document_service
import os

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

def open_doc(doc_name):
    os.startfile(f'{os.getcwd()}/{document_service.DocumentService.DOCS_DIR_PATH}/{doc_name}')

query = st.text_input('Wprowadź słowa kluczowe')
# Sprawdzanie, czy wyniki wyszukiwania są zapisane w session_state
if 'search_doc2vec' not in st.session_state:
    st.session_state.search_doc2vec = []

if 'search_tfidf' not in st.session_state:
    st.session_state.search_tfidf = []

# Przycisk do zatwierdzenia
if st.button('Zatwierdź'):
    # Zapisz wyniki wyszukiwania w session_state
    st.session_state.search_doc2vec = st.session_state.mod_service.search_doc2vec(query, 5)
    st.session_state.search_tfidf = st.session_state.mod_service.search_tfidf(query, 5)

# Wyświetlenie wyników, jeśli są zapisane w session_state
if st.session_state.search_doc2vec:
    st.write('### Najbardziej dopasowane (doc2vec)')
    for dict_part in st.session_state.search_doc2vec:
        col1, col2, col3 = st.columns([3, 2, 1])  # Ustaw proporcje kolumn dla lepszej szerokości
        with col1:
            st.write(dict_part[0])
        with col2:
            st.write(dict_part[1])
        with col3:
            st.button('Open', key=dict_part[0] + '_open', on_click=open_doc, args=[dict_part[0]])

if st.session_state.search_tfidf:
    st.write('### Najbardziej dopasowane (tfidf)')
    for idx, dict_part in enumerate(st.session_state.search_tfidf):
        col1, col2, col3 = st.columns([3, 2, 1])  # Ustaw proporcje kolumn dla lepszej szerokości
        with col1:
            st.write(dict_part[0])
        with col2:
            st.write(dict_part[1])
        with col3:
            # Dodanie unikalnego klucza na podstawie indeksu
            st.button('Open', key=f"{dict_part[0]}_open_{idx}", on_click=open_doc, args=[dict_part[0]])