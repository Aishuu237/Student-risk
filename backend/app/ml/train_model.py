import os
import zipfile
import requests
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.ml.preprocess import load_and_prepare_data

def train():
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    models_dir = os.path.join(os.path.dirname(__file__), '../../models')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, 'student-mat.csv')
    
    if not os.path.exists(csv_path):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip'
        zip_path = os.path.join(data_dir, 'student.zip')
        print(f"Downloading dataset from {url}...")
        r = requests.get(url)
        with open(zip_path, 'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("Dataset downloaded and extracted.")

    print("Loading and preparing data...")
    X, y = load_and_prepare_data(csv_path)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    print("Saving model and metadata...")
    joblib.dump(model, os.path.join(models_dir, 'rf_model.pkl'))
    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'feature_names.pkl'))
    joblib.dump(model.classes_.tolist(), os.path.join(models_dir, 'label_classes.pkl'))
    print("Training complete.")

if __name__ == '__main__':
    # Make sure we can import from app
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    train()
