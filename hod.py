import streamlit as st
import pandas as pd
import pickle

def hod_dashboard():
    st.subheader("🏢 HOD Dashboard")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        dept = st.selectbox("Select Department", df["department"].unique())
        df = df[df["department"] == dept]

        with open("student_model.pkl", "rb") as f:
            model = pickle.load(f)

        df["Predicted"] = model.predict(df[["mid1","mid2","assignment","external"]])
        df["Result"] = df["Predicted"].apply(lambda x: "PASS" if x >= 40 else "FAIL")

        st.write("📊 Average Marks by Class")
        st.write(df.groupby("class")["Predicted"].mean())

        st.dataframe(df)
