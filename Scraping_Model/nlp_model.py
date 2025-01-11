### nlp_model.py

import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Ensure you download the required NLTK data files before using the module
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

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

def refine_query(user_input):
    """Processes user input to refine it for the scraping model."""
    preprocessed_query = preprocess_query(user_input)
    return preprocessed_query