from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analyze_credit_card(card_url):

    credential = AzureKeyCredential(Config.KEY)

    document_client = DocumentAnalysisClient(endpoint=Config.ENDPOINT, credential=credential)

    card_info = document_client.begin_analyze_document("prebuilt-idDocument", AnalyzeDocumentRequest(url_source=card_url), card_url)
    result = card_info.result()

    for document in result.documents:
        fields = document.get('fields', {})

        return {
            "card_name": fields.get('CardHolderName', {}).get('content'),
            "card_number": fields.get('CardNumber', {}).get('content'),
            "expiration_date": fields.get('ExpirationDate', {}).get('content'),
            "bank_name": fields.get('IssuingBank', {}).get('content')
        }

    return result