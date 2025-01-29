import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spacy.lang.en import English

class QueryProcessor:
    def __init__(self):
        nltk.download(['punkt', 'stopwords', 'wordnet'])
        self.nlp = spacy.load("en_core_web_sm")
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def process_query(self, query):
        """Advanced query processing pipeline"""
        doc = self.nlp(query)
        
        # Extract entities
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Process tokens
        tokens = [
            self.lemmatizer.lemmatize(token.text.lower())
            for token in doc
            if not token.is_stop and token.is_alpha
        ]
        
        return {
            "original": query,
            "processed": " ".join(tokens),
            "entities": entities,
            "semantic_terms": self._get_semantic_terms(doc)
        }

    def _get_semantic_terms(self, doc):
        """Extract contextually important terms"""
        return [
            chunk.text.lower()
            for chunk in doc.noun_chunks
            if len(chunk.text.split()) < 4
        ]