import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string


# Ensure you download the required NLTK data files before using the module:
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocessing Function
def preprocess_query(query):
    """Preprocesses the user query by removing punctuation, stopwords, and lemmatizing."""
    # Convert to lowercase
    query = query.lower()

    # Remove punctuation
    query = query.translate(str.maketrans('', '', string.punctuation))

    # Tokenize
    tokens = word_tokenize(query)

    # Remove stopwords and lemmatize
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

# Example Usage
if __name__ == "__main__":
    user_input = input("Enter your course search query: ")
    refined = refine_query(user_input)

    print("\n--- Refined Query ---")
    print(f"Original Query: {refined['original_query']}")
    print(f"Preprocessed Query: {refined['preprocessed_query']}")
    print(f"Intent: {refined['intent']}")
