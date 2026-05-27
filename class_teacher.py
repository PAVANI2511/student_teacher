import streamlit as st
import pandas as pd
import os


# -------------------------------------------------
# 🏫 CLASS TEACHER DASHBOARD
# -------------------------------------------------
def class_teacher_dashboard():

    st.title("🏫 Class Teacher Dashboard")

    st.caption(
        "Class Monitoring • Assignment Risk • Student Performance"
    )

    # -------------------------------------------------
    # USER FOLDER
    # -------------------------------------------------
    username = st.session_state.username

    base_folder = "uploads"
    os.makedirs(base_folder, exist_ok=True)
    role_folder = os.path.join(base_folder, "class_teacher")
    os.makedirs(role_folder, exist_ok=True)
    folder = os.path.join(role_folder, username)
    os.makedirs(folder, exist_ok=True)
    os.makedirs(folder, exist_ok=True)

    # -------------------------------------------------
    # SHOW PREVIOUS FILES
    # -------------------------------------------------
    saved_files = os.listdir(folder)

    if saved_files:

        st.sidebar.subheader("📁 Previous Files")

        for file in saved_files:

            st.sidebar.write(file)

    # -------------------------------------------------
    # FILE UPLOAD
    # -------------------------------------------------
    uploaded_file = st.file_uploader(

        "Upload Student CSV File",

        type=["csv"]
    )

    if not uploaded_file:

        st.info("Please upload CSV file")
        return

    # -------------------------------------------------
    # SAVE FILE
    # -------------------------------------------------
    save_path = os.path.join(
        folder,
        uploaded_file.name
    )

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    # -------------------------------------------------
    # READ CSV
    # -------------------------------------------------
    try:

        df = pd.read_csv(uploaded_file)

    except Exception as e:

        st.error(f"Error reading file: {e}")
        return

    # -------------------------------------------------
    # REQUIRED COLUMNS
    # -------------------------------------------------
    required_cols = {

        "class",
        "roll_no",
        "name"
    }

    missing_cols = required_cols - set(df.columns)

    if missing_cols:

        st.error(f"Missing Columns: {missing_cols}")
        return

    # -------------------------------------------------
    # CLASS FILTER
    # -------------------------------------------------
    class_name = st.selectbox(

        "Select Class",

        sorted(
            df["class"]
            .dropna()
            .unique()
        )
    )

    filtered_df = df[
        df["class"] == class_name
    ]

    # -------------------------------------------------
    # STUDENT FILTER
    # -------------------------------------------------
    student_options = ["All Students"] + sorted(

        filtered_df["roll_no"].astype(str)

        + " - "

        + filtered_df["name"]
    )

    selected_student = st.selectbox(

        "Select Student",

        student_options
    )

    if selected_student != "All Students":

        selected_roll = selected_student.split(" - ")[0]

        filtered_df = filtered_df[

            filtered_df["roll_no"].astype(str)

            == selected_roll
        ]

    # -------------------------------------------------
    # SUBJECT IDENTIFICATION
    # -------------------------------------------------
    assignment_cols = [

        c for c in filtered_df.columns

        if c.endswith("_assign1")
        or c.endswith("_assign2")
    ]

    subjects = sorted({

        c.replace("_assign1", "")
        .replace("_assign2", "")

        for c in assignment_cols
    })

    # -------------------------------------------------
    # CLASS OVERVIEW
    # -------------------------------------------------
    st.subheader("📊 Class Overview")

    total_students = len(filtered_df)

    pass_count = 0
    fail_count = 0

    if "result" in filtered_df.columns:

        pass_count = (

            filtered_df["result"]
            .astype(str)
            .str.upper()
            .eq("PASS")
            .sum()
        )

        fail_count = (

            filtered_df["result"]
            .astype(str)
            .str.upper()
            .eq("FAIL")
            .sum()
        )

    pass_percent = (

        round(
            (pass_count / total_students) * 100,
            2
        )

        if total_students > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", total_students)
    c2.metric("Pass", pass_count)
    c3.metric("Fail", fail_count)
    c4.metric("Pass %", f"{pass_percent}%")

    # -------------------------------------------------
    # ASSIGNMENT RISK
    # -------------------------------------------------
    st.subheader("⚠️ Assignment Risk Students")

    risk_students = []

    for _, row in filtered_df.iterrows():

        missing_count = 0
        missing_subjects = []

        for subject in subjects:

            a1 = row.get(f"{subject}_assign1", 0)
            a2 = row.get(f"{subject}_assign2", 0)

            # ASSIGNMENT 1
            if pd.isna(a1) or a1 == 0:

                missing_count += 1

                missing_subjects.append(
                    f"{subject} A1"
                )

            # ASSIGNMENT 2
            if pd.isna(a2) or a2 == 0:

                missing_count += 1

                missing_subjects.append(
                    f"{subject} A2"
                )

        # -------------------------------------------------
        # RISK LEVEL
        # -------------------------------------------------
        if missing_count == 0:

            risk_level = "Low"

        elif missing_count <= 2:

            risk_level = "Medium"

        else:

            risk_level = "High"

        # -------------------------------------------------
        # STORE RISK STUDENTS
        # -------------------------------------------------
        if missing_count > 0:

            risk_students.append({

                "Roll No": row["roll_no"],

                "Name": row["name"],

                "Missing Assignments": missing_count,

                "Risk Level": risk_level,

                "Missing Subjects": ", ".join(
                    missing_subjects
                )
            })

    # -------------------------------------------------
    # DISPLAY RISK TABLE
    # -------------------------------------------------
    if risk_students:

        risk_df = pd.DataFrame(risk_students)

        st.warning(
            f"{len(risk_df)} students are under assignment risk"
        )

        st.dataframe(
            risk_df,
            use_container_width=True
        )

        st.download_button(

            "⬇️ Download Risk Report",

            risk_df
            .to_csv(index=False)
            .encode("utf-8"),

            "class_risk_report.csv",

            mime="text/csv"
        )

    else:

        st.success("No Assignment Risks 🎉")

    # -------------------------------------------------
    # SUBJECT FAILURE ANALYSIS
    # -------------------------------------------------
    st.subheader("📉 Subject-wise Failure Analysis")

    fail_data = {}

    for subject in subjects:

        ext_col = f"{subject}_external"

        if ext_col in filtered_df.columns:

            fail_percentage = (

                (filtered_df[ext_col] < 40)

                .mean()

                * 100
            )

            fail_data[subject] = round(
                fail_percentage,
                2
            )

    if fail_data:

        fail_df = pd.DataFrame.from_dict(

            fail_data,

            orient="index",

            columns=["Fail %"]
        )

        st.bar_chart(fail_df)

    else:

        st.info("No External Marks Data")

    # -------------------------------------------------
    # TOP & BOTTOM PERFORMERS
    # -------------------------------------------------
    st.subheader("🏆 Student Performance")

    score_cols = [

        c for c in filtered_df.columns

        if (
            "_assign" in c
            or "_mid" in c
            or "_external" in c
        )
    ]

    if score_cols:

        filtered_df[score_cols] = (

            filtered_df[score_cols]
            .fillna(0)
        )

        filtered_df["Total_Score"] = (

            filtered_df[score_cols]
            .sum(axis=1)
        )

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # TOP STUDENTS
        # -------------------------------------------------
        with col1:

            st.success("Top 5 Students")

            top_students = (

                filtered_df

                .sort_values(
                    "Total_Score",
                    ascending=False
                )

                .head(5)
            )

            st.dataframe(

                top_students[
                    [
                        "roll_no",
                        "name",
                        "Total_Score"
                    ]
                ],

                use_container_width=True
            )

        # -------------------------------------------------
        # BOTTOM STUDENTS
        # -------------------------------------------------
        with col2:

            st.error("Bottom 5 Students")

            bottom_students = (

                filtered_df

                .sort_values("Total_Score")

                .head(5)
            )

            st.dataframe(

                bottom_students[
                    [
                        "roll_no",
                        "name",
                        "Total_Score"
                    ]
                ],

                use_container_width=True
            )

    else:

        st.info("No Marks Data Found")

    # -------------------------------------------------
    # FINAL TABLE
    # -------------------------------------------------
    st.subheader("📋 Student Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # -------------------------------------------------
    # DOWNLOAD RECORDS
    # -------------------------------------------------
    st.download_button(

        "⬇️ Download Class Records",

        filtered_df
        .to_csv(index=False)
        .encode("utf-8"),

        "class_records.csv",

        mime="text/csv"
    )