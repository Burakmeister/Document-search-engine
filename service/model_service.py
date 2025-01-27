from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from service.document_service import DocumentService
import numpy as np
import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ModelService:
    DOC_2_VEC_MODEL_PATH = "d2v.model"
    DOC_VECTORS_PATH = "doc_vectors.json"
    TFIDF_MODEL_PATH="tfidf_model.pkl"
    TFIDF_MATRIX_PATH="tfidf_matrix.pkl"

    def __init__(self, documents):
        self.model = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.document_names = []
        self.documents = documents
            
    # uczenie modelu Doc2Vec
    def train_Doc2Vec_model(self):
        tagged_data = [TaggedDocument(words=doc.content, tags=[doc.name]) for doc in self.documents]
        max_epochs = 100
        alpha = 0.025
        model = Doc2Vec(alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
        model.build_vocab(tagged_data)
        for _ in range(max_epochs):
            model.train(tagged_data, total_examples=model.corpus_count, epochs=1)
            model.alpha -= 0.0002
            model.min_alpha = model.alpha
        model.save(ModelService.DOC_2_VEC_MODEL_PATH)
        self.model = model
        self.save_doc_vectors()
        print('Model Doc2Vec zapisany pomyslnie')
    
    # uczenie modelu TF-IDF
    def train_tfidf_model(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        contents = [doc.content for doc in self.documents]
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(contents)
        self.document_names = [doc.name for doc in self.documents]
        
        # Zapis modelu TF-IDF i macierzy
        joblib.dump((self.tfidf_vectorizer, self.tfidf_matrix, self.document_names), ModelService.TFIDF_MODEL_PATH)
        print("Model TF-IDF zapisany pomyslnie.")
    
    # wczytywanie zapisanego modelu
    def read_doc2vec_model(self):
        try:
            self.model = Doc2Vec.load(ModelService.DOC_2_VEC_MODEL_PATH)
            self.load_vectors_from_json()
            print('Model Doc2Vec wczytany pomyslnie')
        except FileNotFoundError:
            print(f"Nie znaleziono modelu {ModelService.DOC_2_VEC_MODEL_PATH}.")
    
    # wczytywanie zapisanego modelu
    def read_tfidf_model(self):
        try:
            self.tfidf_vectorizer, self.tfidf_matrix, self.document_names = joblib.load(ModelService.TFIDF_MODEL_PATH)
            print("Model TF-IDF wczytany pomyslnie.")
        except FileNotFoundError:
            print(f"Nie znaleziono modelu {ModelService.TFIDF_MODEL_PATH}.")

    def save_doc_vectors(self):
        self.doc_vectors = {doc.name: self.model.dv[doc.name].tolist() for doc in self.documents}
        with open(ModelService.DOC_VECTORS_PATH, "w+") as file:
            json.dump(self.doc_vectors, file)
            
    def load_vectors_from_json(self):
        with open(ModelService.DOC_VECTORS_PATH, "r") as file:
            self.doc_vectors = json.load(file)
            
    def search_doc2vec(self, query, top_n):
        query = DocumentService.preprocessing(query)
        query_vector = self.model.infer_vector(query.split())
        similarities = []
        
        for doc_name, doc_vector in self.doc_vectors.items():
            similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
            similarities.append((doc_name, round(similarity,2)))
        
        sorted_results = sorted(similarities, key=lambda x: -x[1])
        return sorted_results[:top_n]
    
    def search_tfidf(self, query, top_n):
        query = DocumentService.preprocessing(query)
        query_vector = self.tfidf_vectorizer.transform([query])
        
        # Obliczenie podobieństwa cosinusowego
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        similarities = np.array([round(similarity, 2) for similarity in similarities])
        # Posortowanie indeksów według podobieństwa
        sorted_indices = similarities.argsort()[::-1][:top_n]
        
        # Zwracanie nazw dokumentów
        return [(self.document_names[idx], similarities[idx]) for idx in sorted_indices]