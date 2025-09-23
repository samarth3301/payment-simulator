from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib, os
from .preprocess import preprocess_data

def train_model(csv_path: str, model_path: str):
    X, y, df = preprocess_data(csv_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # ✅ ensure directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    joblib.dump(clf, model_path)
    print(f"✅ Model saved at {model_path}")
