import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# lematyzacja i usuwanie stop words
def preprocessing(content):
    tokenizer = RegexpTokenizer(r'[a-z][a-z]+')
    data = tokenizer.tokenize(content.lower())
    data = [w for w in data if not w in stopwords.words('english')]
    wnl = nltk.WordNetLemmatizer()
    data = [wnl.lemmatize(w) for w in data]
    return " ".join(data)

# wczytywanie danych
def read_data():
    docs = []
    dires = [d for d in os.listdir() if os.path.isdir(d)]
    for dir in dires:
        files = [f for f in os.listdir(f'{os.getcwd()}/{dir}') if os.path.isfile(f'{os.getcwd()}/{dir}/{f}')]
        for file in files:
            content = ''
            with open(f'{os.getcwd()}/{dir}/{file}', 'r') as doc:
                content = doc.read()
            content = preprocessing(content)
            docs.append(content)
    return docs

# uczenie modelu
def teach_model(docs):
    tagged_data = [TaggedDocument(words=value, tags=[index]) for index, value in enumerate(docs)]
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
    model.save("d2v.model")

# sprawdzam zmiany w plikach
def is_changes_in_docs(docs):
    return False

def main():
    docs = read_data() #wczytywanie na osobnym watku
    if is_changes_in_docs(docs):
        while True:
            inp = input('Znaleziono nowe dokumnty, czy chcesz ponownie wytrenować model? (może zająć to kilka minut) TAK/NIE')
            match str(inp).lower():
                case 'tak':
                    teach_model(docs)
                case 'nie':
                    break
    else:
        print('Koniec')
                



if __name__ == "__main__":
    main()