import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

def teacher_dashboard():
    with open("student_model.pkl", "rb") as f:
        model = pickle.load(f)

    st.title("👨‍🏫 Teacher Dashboard")
    st.caption("Bulk Student Performance Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV (mid1, mid2, assignment, external)",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        required_cols = ["mid1", "mid2", "assignment", "external"]
        if not all(col in df.columns for col in required_cols):
            st.error("❌ CSV must contain mid1, mid2, assignment, external")
            return

        df["Predicted_Final_Score"] = model.predict(df[required_cols])
        df["Result"] = df["Predicted_Final_Score"].apply(
            lambda x: "PASS" if x >= 40 else "FAIL"
        )

        pass_count = (df["Result"] == "PASS").sum()
        fail_count = (df["Result"] == "FAIL").sum()

        st.subheader("📊 Summary")
        st.write(f"PASS: {pass_count}")
        st.write(f"FAIL: {fail_count}")

        fig, ax = plt.subplots()
        ax.bar(["PASS", "FAIL"], [pass_count, fail_count])
        st.pyplot(fig)

        st.subheader("📋 Detailed Results")
        st.dataframe(df)

        st.download_button(
            "⬇️ Download Results",
            df.to_csv(index=False),
            "predicted_results.csv",
            "text/csv"
        )
