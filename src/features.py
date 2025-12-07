import re
import pandas as pd
from datetime import datetime as dt
from dateparser.search import search_dates

# Feature engineering functions

def get_days_until_event(text):
    """ 
    Scans text using dateparser to find the closest future date 
    and returns how many days away it is
    """
    # Ensure that text is a string
    if not isinstance(text, str): return 999

    now = dt.now()
    extracted_dates = search_dates(text, languages=['en'], settings={'PREFER_DATES_FROM': 'future'})

    if not extracted_dates: 
        return 999 #default for no date found
    
    future_dates = []
    for date_tuple in extracted_dates:
        found_date = date_tuple[1]
        found_date = found_date.replace(tzinfo=None)    
        if found_date > now:
            future_dates.append(found_date)

    if not future_dates:
        return 999
    
    # Get the soonest date
    soonest_date = min(future_dates)
    delta = soonest_date - now
    return delta.days

def check_unsubscribe_present(row):
    """
    Checks emails for 'unsubscribe', and returns one if found, else zero 
    """
    # Check header
    if "List-Unsubscribe" in row['headers']:
        return 1
    
    # Check body
    if re.search (r'unsubscribe|manage - preferences|opt-out', row['body'], re.IGNORECASE):
        return 1

    return 0 


def get_urgency_score(text):
    """
    Simple urgency score based on presence of certain keywords
    """
    # Ensure that text is a string
    if not isinstance(text, str): return 0

    urgency_keywords = ['urgent', 'asap', 'immediately', 'priority', 'important', 'attention', 'confirm', 'deadline', 'action required', 'due', 'response needed', 'follow up', 'time sensitive', 'reminder']
    score = 0
    for word in urgency_keywords:
        if word in text.lower():
            score += 1
    return score

def get_participant_count(row):
    """
    Counts number of unique email addresses in To, CC, BCC
    """
    participants = set()
    for field in ['to', 'cc', 'bcc']:
        if pd.notna(row[field]):
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', row[field])
            participants.update(emails)

    return len(participants)

def get_research_score(text):
    """
    Simple research score based on presence of certain keywords
    """
    research_keywords = ['research', 'study', 'analysis', 'data', 'findings', 'report', 'survey', 'experiment', 'results']
    score = 0

   
    for word in research_keywords:
        if word in text.lower():
            score += 1 
    return score

# Hueristic classifier to solve cold start problem

def heuristic_classifier(row):
    """
    Classifies email urgency based on engineered features
    """
    if row['days_until_event'] < 7:
        return "Important"
    
    if row ['urgency_score'] > 0 or row['research_score'] > 0:
        return "Important"
    
    if row['participant_count'] > 5 and row['urgency_score'] > 0:
        return "Important"
    
    if row['unsubscribe_present'] == 1:
        return "Archive"
    
    if row['participant_count'] > 5 and row['urgency_score'] == 0:
        return "Archive"
    
    else: 
        return "Archive"

