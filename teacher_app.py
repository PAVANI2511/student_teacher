import streamlit as st
from subject_teacher import subject_teacher_dashboard
from class_teacher import class_teacher_dashboard
from hod import hod_dashboard


def teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")

    # Initialize role state
    if "teacher_role" not in st.session_state:
        st.session_state.teacher_role = None

    # ---------------- ROLE SELECTION ----------------
    if st.session_state.teacher_role is None:
        role = st.selectbox(
            "Select Teacher Role",
            ["Select", "Subject Teacher", "Class Teacher", "Head of Department"]
        )

        if st.button("Continue"):
            if role != "Select":
                st.session_state.teacher_role = role
                st.rerun()
            else:
                st.error("Please select a role to continue")

        return

    # ---------------- SUBJECT TEACHER ----------------
    if st.session_state.teacher_role == "Subject Teacher":
        subject_teacher_dashboard()

    # ---------------- CLASS TEACHER ----------------
    elif st.session_state.teacher_role == "Class Teacher":
        class_teacher_dashboard()

    # ---------------- HOD ----------------
    elif st.session_state.teacher_role == "Head of Department":
        hod_dashboard()

    # ---------------- LOGOUT ----------------
    st.divider()
    if st.button("⬅️ Back to Teacher Role Selection"):
        st.session_state.teacher_role = None
        st.rerun()
