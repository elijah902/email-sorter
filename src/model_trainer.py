import os 
import pickle 
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

MODEL_PATH = 'data/models/classifier.pkl'

# Modeling 
def train_initial_model(df):
    """
    Trains initial models on the dataset
    """
    features = ['days_until_event', 'urgency_score', 'participant_count', 'research_score', 'unsubscribe_present']
    X = df[features]
    le = LabelEncoder()
    y = le.fit_transform(df['label'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    print("Random Forest Classifier Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    lin_model = LogisticRegression(max_iter=200)
    lin_model.fit(X_train, y_train)
    y_pred_lin = lin_model.predict(X_test)
    print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred_lin))
    print(classification_report(y_test, y_pred_lin))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rf_model, f)

    return rf_model, le

def load_model():
    """
    Loads saved model and LabelEncoder
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run initial training first!")
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
        
    return model


