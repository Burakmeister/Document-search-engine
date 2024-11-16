from service.document_service import DocumentService
from service.model_service import ModelService

def main():
    doc_service = DocumentService()
    mod_service = None
    if doc_service.are_changes_in_files():
        while True:
            inp = input('Znaleziono nowe dokumenty, czy chcesz ponownie wytrenowac model? (moze zajac to kilka minut) TAK/NIE\n')
            match str(inp).lower():
                case 'tak':
                    doc_service.read_data()
                    mod_service = ModelService(doc_service.documents)
                    mod_service.teach_model()
                    break
                case 'nie':
                    mod_service = ModelService(doc_service.documents)
                    mod_service.teach_model()
                    break
    else:
        mod_service = ModelService(doc_service.documents)
        mod_service.read_model()
    
if __name__ == "__main__":
    main()