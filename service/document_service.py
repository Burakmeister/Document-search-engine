from model.document import Document
from exception.changes_in_docs_exception import ChangesInDocumentsException
from nltk.corpus import stopwords
import nltk
import json
import os
from nltk.tokenize import RegexpTokenizer

class DocumentService:
    FILES_EXTENSIONS = ('.docs', '.txt')
    DOCS_DATA_FILE_PATH = "docs_data"

    # sprawdzanie zmian w dokumentach
    def __init__(self):
        self.documents = []
    
    # wczytywanie danych
    def read_data(self):
        status_data = {}
        dires = [d for d in os.listdir() if os.path.isdir(d)]
        for dir in dires:
            files = [f for f in os.listdir(f'{os.getcwd()}/{dir}') if os.path.isfile(f'{os.getcwd()}/{dir}/{f}') and f.endswith(DocumentService.FILES_EXTENSIONS)]
            for file in files:
                content = ''
                path = f'{os.getcwd()}/{dir}/{file}'
                with open(path, 'r', encoding="latin-1") as doc:
                    content = doc.read()
                content = self.preprocessing(content)
                status_data[file] = os.path.getmtime(path)
                self.documents.append(Document(file, os.path.getmtime(path), content))
        json.dump(status_data, open(DocumentService.DOCS_DATA_FILE_PATH,'w+'))

    
    # lematyzacja i usuwanie stop words
    def preprocessing(SELF, content):
        tokenizer = RegexpTokenizer(r'[a-z][a-z]+')
        data = tokenizer.tokenize(content.lower())
        data = [w for w in data if not w in stopwords.words('english')]
        wnl = nltk.WordNetLemmatizer()
        data = [wnl.lemmatize(w) for w in data]
        return " ".join(data)
    
    def are_changes_in_files(self):
        dires = [d for d in os.listdir() if os.path.isdir(d)]
        docs = {}
        try:
            docs = json.load(open(DocumentService.DOCS_DATA_FILE_PATH, 'r'))
        except:
            return True
        num_of_files = 0
        for dir in dires:
            files = [f for f in os.listdir(f'{os.getcwd()}/{dir}') if os.path.isfile(f'{os.getcwd()}/{dir}/{f}') and f.endswith(DocumentService.FILES_EXTENSIONS)]
            for file in files:
                # tu sprawdzam daty edycji i nazwy
                path = f'{os.getcwd()}/{dir}/{file}'
                mod_date = os.path.getmtime(path)
                num_of_files+=1
                if(not file in docs or docs[file]!=mod_date):
                    return True
        # sprawdzam czy liczba plikow sie zgadza
        if num_of_files != len(docs.keys()):
            return True
        return False
    
    
    
    def documents_to_dict(self):
        doc_dict = {}
        for doc in self.documents:
            doc_dict[doc.name] = doc.content