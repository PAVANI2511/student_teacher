import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ---------------- LOAD DATASET ----------------
df = pd.read_csv("kaggle_student_dataset.csv")

# ---------------- SELECT REQUIRED COLUMNS ----------------
# IMPORTANT:
# mid1, mid2, assignment, external must be NUMERIC (obtained marks)
df = df[[
    "mid1",          # obtained marks (e.g., 23)
    "mid2",          # obtained marks (e.g., 15)
    "assignment",    # obtained marks (e.g., 6)
    "external",      # obtained external marks (e.g., 40)
    "final_score"    # total score
]]

# ---------------- FEATURES & TARGET ----------------
X = df.drop("final_score", axis=1)
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

# ---------------- SAVE MODEL ----------------
with open("student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained successfully with marks-based features only")