import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------------- LOAD DATASET ----------------
df = pd.read_csv("student_dataset.csv")

# ---------------- FEATURE & TARGET SELECTION ----------------
X = df[[
    "mid1",
    "mid2",
    "assignment1",
    "assignment2",
    "external"
]]

y = df["final_score"]

# ---------------- TRAIN-TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------- TRAIN MODEL ----------------
model = LinearRegression()
model.fit(X_train, y_train)

# ---------------- EVALUATE MODEL ----------------
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)

print(f"✅ Model trained successfully")
print(f"📊 R² Score (Accuracy): {accuracy:.2f}")

# ---------------- SAVE MODEL ----------------
with open("student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("💾 Model saved as student_model.pkl")
