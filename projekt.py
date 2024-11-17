from service.document_service import DocumentService
from service.model_service import ModelService

def main():
    doc_service = DocumentService()
    mod_service = None
    if doc_service.are_changes_in_files():
        inp = input('Znaleziono nowe dokumenty, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut) TAK/NIE\n')
        match inp.lower():
            case 'tak':
                print('Wczytywanie dokumentow...')
                doc_service.read_data()
                mod_service = ModelService(doc_service.documents)
                mod_service.train_Doc2Vec_model()
                mod_service.train_tfidf_model()
                pass
            case 'nie':
                mod_service = ModelService(doc_service.documents)
                mod_service.read_doc2vec_model()
                mod_service.read_tfidf_model()
                pass
    else:
        mod_service = ModelService(doc_service.documents)
        mod_service.read_tfidf_model()
        mod_service.read_doc2vec_model()
    while True:
        print('1. Wyszukaj dokument Word2Vec')
        print('2. Wyszukaj dokument Tf-idf')
        print('3. Sprawdz zmiany w dokumentach')
        print('4. Koniec')
        inp = input('Opcja: ')
        match inp.lower():
            case '1':
                query = input('Wprowadź zapytanie: ')
                print(mod_service.search_doc2vec(query, 5))
                pass
            case '2':
                query = input('Wprowadź zapytanie: ')
                print(mod_service.search_tfidf(query, 5))
                pass
            case '3':
                if doc_service.are_changes_in_files():
                    inp = input('Znaleziono nowe dokumenty, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut) TAK/NIE\n')
                    match inp.lower():
                        case 'tak':
                            print('Wczytywanie dokumentow...')
                            doc_service.read_data()
                            mod_service = ModelService(doc_service.documents)
                            mod_service.train_Doc2Vec_model()
                            mod_service.train_tfidf_model()
                            pass
                        case 'nie':
                            pass
                else:
                    print('Brak zmian w dokumentach')
            case '4':
                break
if __name__ == "__main__":
    main()