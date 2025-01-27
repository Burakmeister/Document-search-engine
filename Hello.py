from service.document_service import DocumentService
from service.model_service import ModelService
import streamlit as st

st.set_page_config(
    layout='wide',
    page_icon="📄",
    initial_sidebar_state='expanded',
)

st.write('### Aplikacja służąca do wyszukiwania wzorców w dokumentach')

@st.dialog("Znaleziono nowe dokumenty, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut)")
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

def main():
    st.session_state.doc_service = DocumentService()
    st.session_state.mod_service = None
    if st.session_state.doc_service.are_changes_in_files():
        if 'vote' not in st.session_state:
            vote()
        else:
            match st.session_state.vote:
                case True:
                    print('Wczytywanie dokumentow...')
                    st.session_state.doc_service.read_data()
                    st.session_state.mod_service = ModelService(st.session_state.doc_service.documents)
                    st.session_state.mod_service.train_Doc2Vec_model()
                    st.session_state.mod_service.train_tfidf_model()
                    pass
                case False:
                    mod_service = ModelService(st.session_state.doc_service.documents)
                    mod_service.read_doc2vec_model()
                    mod_service.read_tfidf_model()
                    pass
    else:
        mod_service = ModelService(st.session_state.doc_service.documents)
        mod_service.read_tfidf_model()
        mod_service.read_doc2vec_model()

if __name__ == "__main__":
    main()