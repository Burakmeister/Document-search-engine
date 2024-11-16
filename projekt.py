from service.document_service import DocumentService
from model.document import Document
import os
import json
from nltk.corpus import stopwords
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

DOC_2_VEC_MODEL_NAME = "d2v.model"

            
# uczenie modelu
def teach_model(docs):
    tagged_data = [TaggedDocument(words=doc.content, tags=[doc.name]) for doc in docs]
    print(len(tagged_data))
    max_epochs = 100
    alpha = 0.025
    model = Doc2Vec(alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
    model.build_vocab(tagged_data)
    for epoch in range(max_epochs):
        print(f'iteration {epoch+1}')
        model.train(tagged_data, total_examples=model.corpus_count, epochs=1)
        model.alpha -= 0.0002
        model.min_alpha = model.alpha
    model.save(DOC_2_VEC_MODEL_NAME)
    print('Model nauczony pomyslnie')
    return model

# wczytywanie zapisanego modelu
def read_model():
    try:
        model = Doc2Vec.load(DOC_2_VEC_MODEL_NAME)
        print('Model wczytany pomyslnie')
        return model
    except FileNotFoundError:
        print(f"Nie znaleziono modelu {DOC_2_VEC_MODEL_NAME}.")
        return None

def main():
    model = None
    doc_service = DocumentService()
    if doc_service.are_changes_in_files():
        while True:
            inp = input('Znaleziono nowe dokumenty, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut) TAK/NIE\n')
            match str(inp).lower():
                case 'tak':
                    doc_service.read_data()
                    model = teach_model(doc_service.documents)
                    break
                case 'nie':
                    model = read_model()
                    break
    else:
        model = read_model()
    
    # do pracy rodacy

if __name__ == "__main__":
    main()