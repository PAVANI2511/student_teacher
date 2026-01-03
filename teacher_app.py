import streamlit as st

from subject_teacher import subject_teacher_dashboard
from class_teacher import class_teacher_dashboard
from hod import hod_dashboard


def teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")

    role = st.selectbox(
        "Select Teacher Role",
        ["Select", "Subject Teacher", "Class Teacher", "Head of Department"]
    )

    if role == "Select":
        st.info("Please select a role to continue")
        return

    if role == "Subject Teacher":
        subject_teacher_dashboard()

    elif role == "Class Teacher":
        class_teacher_dashboard()

    elif role == "Head of Department":
        hod_dashboard()
