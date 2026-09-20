import pandas as pd
import numpy as np

def load_and_prepare_data(csv_path: str):
    df = pd.read_csv(csv_path, sep=';')
    
    def get_risk(g3):
        if g3 >= 14:
            return 'LOW'
        elif g3 >= 8:
            return 'MEDIUM'
        else:
            return 'HIGH'
            
    df['risk_level'] = df['G3'].apply(get_risk)
    
    df['internet'] = df['internet'].map({'yes': 1, 'no': 0})
    df['activities'] = df['activities'].map({'yes': 1, 'no': 0})
    
    features = ['age', 'studytime', 'absences', 'G1', 'G2', 'failures', 'Dalc', 'Walc', 'internet', 'activities']
    
    # Check available columns to ensure we don't error out if some are missing
    available_features = [f for f in features if f in df.columns]
    
    X = df[available_features]
    y = df['risk_level']
    
    return X, y

def prepare_prediction_input(features_dict: dict):
    # Mapping request features to UCI features
    age = features_dict.get('age', 18)
    study_time = features_dict.get('study_time', 2.0)
    attendance = features_dict.get('attendance', 100.0)
    
    absences = round((100 - attendance) / 5)
    
    previous_score = features_dict.get('previous_score', 50.0)
    g1 = previous_score / 5
    g2 = previous_score / 5
    
    internet = 1 if features_dict.get('internet_access', True) else 0
    activities = 1 if features_dict.get('extracurricular', False) else 0
    
    failures = 0
    dalc = 1
    walc = 1
    
    # Feature order: ['age', 'studytime', 'absences', 'G1', 'G2', 'failures', 'Dalc', 'Walc', 'internet', 'activities']
    return np.array([[age, study_time, absences, g1, g2, failures, dalc, walc, internet, activities]])
