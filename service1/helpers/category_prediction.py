import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import joblib
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

Category_Prediction_Model = joblib.load(os.getcwd()+"/helpers/models_ml/logistic_regressor.joblib")
Vectorizer_Model = joblib.load(os.getcwd()+"/helpers/models_ml/vectorizer.joblib")

def clean_text(text):
    if not text or text == ' ' or isinstance(text, (int, float, bool)) or text.isspace():
        return None
    
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    
    tokens = word_tokenize(text)

    if len(tokens) < 4:
        return None

    stop_words = set(stopwords.words("english"))
    
    lemmatizer = WordNetLemmatizer()

    tokens = [lemmatizer.lemmatize(word) for word in tokens if re.match(r'^[a-zA-Z0-9]+$', word) and word not in stop_words]

    processed_text = " ".join(tokens)

    return processed_text

def complaint_category_prediction(complaint_text):
    input_matrix = Vectorizer_Model.transform([clean_text(complaint_text)])
    y_pred = Category_Prediction_Model.predict(input_matrix)

    return str(y_pred[0])

