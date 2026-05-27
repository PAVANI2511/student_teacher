import streamlit as st

from subject_teacher import subject_teacher_dashboard
from class_teacher import class_teacher_dashboard
from hod import hod_dashboard


# -------------------------------------------------
# 👨‍🏫 TEACHER DASHBOARD
# -------------------------------------------------
def teacher_dashboard():

    st.title("👨‍🏫 Teacher Portal")

    # -------------------------------------------------
    # SESSION VARIABLES
    # -------------------------------------------------
    if "teacher_role" not in st.session_state:
        st.session_state.teacher_role = None

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    # -------------------------------------------------
    # ROLE SELECTION
    # -------------------------------------------------
    if st.session_state.teacher_role is None:

        role = st.selectbox(

            "Select Teacher Role",

            [
                "Select",
                "Subject Teacher",
                "Class Teacher",
                "Head of Department"
            ]
        )

        if st.button("Continue"):

            if role != "Select":

                st.session_state.teacher_role = role

                st.rerun()

            else:

                st.error("Please select a role")

        return

    # -------------------------------------------------
    # LOGIN PAGE
    # -------------------------------------------------
    if not st.session_state.logged_in:

        st.subheader(f"🔐 {st.session_state.teacher_role} Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            # -------------------------------------------------
            # HOD LOGIN
            # -------------------------------------------------
            if (
                st.session_state.teacher_role
                == "Head of Department"
            ):

                if (
                    username == "hod"
                    and password == "hod123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login Successful")
                    st.rerun()

                else:

                    st.error("Invalid Credentials")

            # -------------------------------------------------
            # CLASS TEACHER LOGIN
            # -------------------------------------------------
            elif (
                st.session_state.teacher_role
                == "Class Teacher"
            ):

                if (
                    username == "class_teacher"
                    and password == "class123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login Successful")
                    st.rerun()

                else:

                    st.error("Invalid Credentials")

            # -------------------------------------------------
            # SUBJECT TEACHER LOGIN
            # -------------------------------------------------
            elif (
                st.session_state.teacher_role
                == "Subject Teacher"
            ):

                if (
                    username == "subject_teacher"
                    and password == "subject123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login Successful")
                    st.rerun()

                else:

                    st.error("Invalid Credentials")

        return

    # -------------------------------------------------
    # OPEN DASHBOARDS
    # -------------------------------------------------
    if st.session_state.teacher_role == "Subject Teacher":

        subject_teacher_dashboard()

    elif st.session_state.teacher_role == "Class Teacher":

        class_teacher_dashboard()

    elif st.session_state.teacher_role == "Head of Department":

        hod_dashboard()

    # -------------------------------------------------
    # LOGOUT
    # -------------------------------------------------
    st.divider()

    if st.button(
        "Logout",
        key="teacher_logout"
    ):
        st.session_state.logged_in = False
        st.session_state.teacher_role = None
        st.session_state.username = ""
        st.rerun()