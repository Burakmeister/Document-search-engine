from service.model_service import ModelService
from service.document_service import DocumentService

def get_updated_model_service(doc_service):
    doc_service.read_data()
    mod_service = ModelService(doc_service.documents)
    mod_service.train_Doc2Vec_model()
    mod_service.train_tfidf_model()
    return mod_service

def get_model_service(doc_service):
    mod_service = ModelService(doc_service.documents)
    mod_service.read_doc2vec_model()
    mod_service.read_tfidf_model()
    return mod_service