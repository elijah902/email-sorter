import pandas as pd
import kagglehub
from src.parser import parse_email
from src.features import get_urgency_score, heuristic_classifier, get_participant_count, get_research_score, get_days_until_event, check_unsubscribe_present
from src.model_trainer import train_initial_model, load_model
from sklearn.preprocessing import LabelEncoder

def main():
    
    # Data loading
    path = kagglehub.dataset_download("wcukierski/enron-email-dataset")
    df = pd.read_csv(f"{path}/emails.csv", nrows=15000)

    # Email parsing
    parsed_data = df['message'].apply(parse_email).apply(pd.Series)
    df = pd.concat([df, parsed_data], axis=1)
    
    # Feature engineering
    df['combined_text'] = df['subject'].fillna('') + ' ' + df['body'].fillna('')
    df['days_until_event'] = df['date'].apply(get_days_until_event)
    df['urgency_score'] = df['combined_text'].apply(get_urgency_score)
    df['participant_count'] = df.apply(get_participant_count, axis=1)
    df['research_score'] = df['combined_text'].apply(get_research_score)
    df['unsubscribe_present'] = df['body'].apply(check_unsubscribe_present)

    df['lablel'] = df.apply(heuristic_classifier, axis=1)

    # Initial model training
    trained_model, label_encoder = train_initial_model(df)
    


    if __name__ == "__main__":
        main()

