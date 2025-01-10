import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocessing Function
def preprocess_query(query):
    """Preprocesses the user query by removing punctuation, stopwords, and lemmatizing."""
    query = query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(query)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Intent Recognition (Simple Keyword Matching)
def recognize_intent(query):
    """Recognizes the user's intent based on keywords."""
    keywords = {
        "programming": ["programming", "coding", "development", "software"],
        "data science": ["data", "machine learning", "AI", "artificial intelligence"],
        "web development": ["web", "frontend", "backend", "javascript", "html", "css"],
        "business": ["business", "management", "marketing", "strategy"]
    }

    for intent, words in keywords.items():
        if any(word in query for word in words):
            return intent
    return "general"

# Generate Refined Query for Search
def refine_query(user_input):
    """Processes user input to refine it for the scraping model."""
    preprocessed_query = preprocess_query(user_input)
    intent = recognize_intent(preprocessed_query)
    return {
        "original_query": user_input,
        "preprocessed_query": preprocessed_query,
        "intent": intent
    }
