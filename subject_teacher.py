import streamlit as st
import pandas as pd
import pickle

def subject_teacher_dashboard():
    st.subheader("📘 Subject Teacher Dashboard")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        subject = st.selectbox("Select Subject", df["subject"].unique())
        df = df[df["subject"] == subject]

        with open("student_model.pkl", "rb") as f:
            model = pickle.load(f)

        df["Predicted"] = model.predict(df[["mid1","mid2","assignment","external"]])
        df["Result"] = df["Predicted"].apply(lambda x: "PASS" if x >= 40 else "FAIL")

        st.dataframe(df)
