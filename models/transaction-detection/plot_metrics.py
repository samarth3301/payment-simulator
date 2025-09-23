import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, accuracy_score
import joblib
from models.fraud_detection.preprocess import preprocess_data
from sklearn.model_selection import train_test_split

def plot_metrics(csv_path: str, model_path: str, output_img: str = "roc_curve.png"):
    # Load model & preprocess data
    model = joblib.load(model_path)
    X, y, df = preprocess_data(csv_path)

    # Train/test split (same as in training)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]  # probability for ROC curve

    # Accuracy
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.4f}")

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - Fraud Detection Model")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig(output_img)
    plt.close()
    print(f"📊 ROC curve saved to {output_img}")

# ----------------- Runner -----------------
if __name__ == "__main__":
    # Adjust paths if needed
    csv_path = "data/transactions.csv"
    model_path = "model/fraud_model.joblib"
    plot_metrics(csv_path, model_path, "roc_curve.png")
