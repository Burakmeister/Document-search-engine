from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

class ModelService:
    DOC_2_VEC_MODEL_NAME = "d2v.model"

    def __init__(self, documents):
        self.model = None
        self.documents = documents
            
    # uczenie modelu
    def teach_model(self):
        tagged_data = [TaggedDocument(words=doc.content, tags=[doc.name]) for doc in self.documents]
        max_epochs = 100
        alpha = 0.025
        model = Doc2Vec(alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)
        model.build_vocab(tagged_data)
        for epoch in range(max_epochs):
            print(f'iteration {epoch+1}')
            model.train(tagged_data, total_examples=model.corpus_count, epochs=1)
            model.alpha -= 0.0002
            model.min_alpha = model.alpha
        model.save(ModelService.DOC_2_VEC_MODEL_NAME)
        print('Model nauczony pomyslnie')
        return model

    # wczytywanie zapisanego modelu
    def read_model(self):
        try:
            model = Doc2Vec.load(ModelService.DOC_2_VEC_MODEL_NAME)
            print('Model wczytany pomyslnie')
            return model
        except FileNotFoundError:
            print(f"Nie znaleziono modelu {ModelService.DOC_2_VEC_MODEL_NAME}.")
            return None