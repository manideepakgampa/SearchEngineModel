#Project-1\Scraping_Model\nlp_model.py
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

def refine_query(user_input):
    """Process the user query and return a refined version."""
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(user_input.lower())  # Tokenize and convert to lowercase
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    refined_query = " ".join(filtered_tokens)
    return {"original_query": user_input, "preprocessed_query": refined_query}
