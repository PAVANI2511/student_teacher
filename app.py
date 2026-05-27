import streamlit as st

from student_app import student_dashboard
from teacher_app import teacher_dashboard


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Student Performance System",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------------------------------
# MAIN LOGIN
# -------------------------------------------------
if st.session_state.role is None:

    st.title("🔐 Login")

    role = st.selectbox(

        "Select Role",

        [
            "Select",
            "Student",
            "Teacher"
        ]
    )

    if st.button("Continue"):

        if role != "Select":

            st.session_state.role = role

            st.rerun()

        else:

            st.error("Please select a role")

# -------------------------------------------------
# STUDENT
# -------------------------------------------------
elif st.session_state.role == "Student":

    student_dashboard()

    if st.button(
        "Logout",
        key="student_logout"
    ):

        st.session_state.role = None

        st.rerun()

# -------------------------------------------------
# TEACHER
# -------------------------------------------------
elif st.session_state.role == "Teacher":

    teacher_dashboard()