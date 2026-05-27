import streamlit as st
import pandas as pd
import os


# -------------------------------------------------
# 🏢 HOD DASHBOARD
# -------------------------------------------------
def hod_dashboard():

    st.title("🏢 HOD Dashboard")

    st.caption(
        "Department Monitoring • Assignment Risk • Student Performance"
    )

    # -------------------------------------------------
    # USER FOLDER
    # -------------------------------------------------
    username = st.session_state.username

    base_folder = "uploads"
    os.makedirs(base_folder, exist_ok=True)
    role_folder = os.path.join(base_folder, "hod")
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
    files = st.file_uploader(

        "Upload Student Files",

        type=["csv"],

        accept_multiple_files=True
    )

    if not files:

        st.info("Please upload CSV files")
        return

    dfs = []

    # -------------------------------------------------
    # SAVE FILES
    # -------------------------------------------------
    for file in files:

        save_path = os.path.join(
            folder,
            file.name
        )

        with open(save_path, "wb") as f:

            f.write(file.getbuffer())

        try:

            df_temp = pd.read_csv(file)

            dfs.append(df_temp)

        except Exception as e:

            st.error(f"Error reading {file.name}: {e}")

    if not dfs:

        st.error("No valid files uploaded")
        return

    # -------------------------------------------------
    # MERGE DATA
    # -------------------------------------------------
    df = pd.concat(dfs, ignore_index=True)

    # -------------------------------------------------
    # REQUIRED COLUMNS
    # -------------------------------------------------
    required = {

        "year",
        "department",
        "section",
        "roll_no",
        "name"
    }

    missing = required - set(df.columns)

    if missing:

        st.error(f"Missing Columns: {missing}")
        return

    # -------------------------------------------------
    # FILTERS
    # -------------------------------------------------
    st.sidebar.subheader("🔍 Filters")

    department = st.sidebar.selectbox(

        "Department",

        sorted(
            df["department"]
            .dropna()
            .unique()
        )
    )

    year = st.sidebar.selectbox(

        "Year",

        sorted(

            df[
                df["department"] == department
            ]["year"]

            .dropna()

            .unique()
        )
    )

    section = st.sidebar.selectbox(

        "Section",

        sorted(

            df[
                (df["department"] == department)
                &
                (df["year"] == year)
            ]["section"]

            .dropna()

            .unique()
        )
    )

    filtered_df = df[

        (df["department"] == department)
        &
        (df["year"] == year)
        &
        (df["section"] == section)
    ]

    # -------------------------------------------------
    # STUDENT FILTER
    # -------------------------------------------------
    student_option = st.sidebar.selectbox(

        "Student",

        ["All Students"]

        +

        sorted(

            filtered_df["roll_no"].astype(str)
            + " - "
            + filtered_df["name"]
        )
    )

    if student_option != "All Students":

        roll = student_option.split(" - ")[0]

        filtered_df = filtered_df[
            filtered_df["roll_no"].astype(str)
            == roll
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
    # OVERVIEW
    # -------------------------------------------------
    st.subheader("📊 Department Overview")

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

    c1, c2, c3 = st.columns(3)

    c1.metric("Students", total_students)
    c2.metric("Pass", pass_count)
    c3.metric("Fail", fail_count)

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

            if pd.isna(a1) or a1 == 0:

                missing_count += 1

                missing_subjects.append(
                    f"{subject} A1"
                )

            if pd.isna(a2) or a2 == 0:

                missing_count += 1

                missing_subjects.append(
                    f"{subject} A2"
                )

        if missing_count == 0:

            risk_level = "Low"

        elif missing_count <= 2:

            risk_level = "Medium"

        else:

            risk_level = "High"

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

    if risk_students:

        risk_df = pd.DataFrame(risk_students)

        st.warning(
            f"{len(risk_df)} students under assignment risk"
        )

        st.dataframe(
            risk_df,
            use_container_width=True
        )

    else:

        st.success("No Assignment Risks 🎉")

    # -------------------------------------------------
    # FAILURE ANALYSIS
    # -------------------------------------------------
    st.subheader("📉 Subject Failure %")

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

    # -------------------------------------------------
    # TOP/BOTTOM STUDENTS
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

    filtered_df[score_cols] = (
        filtered_df[score_cols]
        .fillna(0)
    )

    filtered_df["Total_Score"] = (
        filtered_df[score_cols]
        .sum(axis=1)
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success("Top 5 Students")

        st.dataframe(

            filtered_df

            .sort_values(
                "Total_Score",
                ascending=False
            )

            .head(5)[

                [
                    "roll_no",
                    "name",
                    "Total_Score"
                ]
            ],

            use_container_width=True
        )

    with col2:

        st.error("Bottom 5 Students")

        st.dataframe(

            filtered_df

            .sort_values("Total_Score")

            .head(5)[

                [
                    "roll_no",
                    "name",
                    "Total_Score"
                ]
            ],

            use_container_width=True
        )

    # -------------------------------------------------
    # FINAL TABLE
    # -------------------------------------------------
    st.subheader("📋 Student Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.download_button(

        "⬇️ Download Records",

        filtered_df
        .to_csv(index=False)
        .encode("utf-8"),

        "student_records.csv",

        mime="text/csv"
    )