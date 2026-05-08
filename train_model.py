import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load REAL dataset
df = pd.read_csv("cicids_aligned.csv")

# Clean
df.replace([float('inf'), float('-inf')], 0, inplace=True)
df.dropna(inplace=True)

# Features + Label
X = df.drop("Label", axis=1)
y = df["Label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)

print("\n=== PACKET CLASSIFIER PERFORMANCE ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save
with open("packet_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model trained and saved")
