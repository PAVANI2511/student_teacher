import streamlit as st
import pandas as pd

# -------------------------------------------------
# 🔐 HOD LOGIN
# -------------------------------------------------
def hod_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 HOD Login")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user == "hod" and pwd == "hod123":
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
        return False
    return True


# -------------------------------------------------
# 🏢 HOD DASHBOARD
# -------------------------------------------------
def hod_dashboard():
    st.subheader("🏢 HOD Dashboard – Academic Monitoring System")
    st.caption("Department • Year • Section • Student • Assignment Risk")

    # -------------------------------------------------
    # 📂 FILE UPLOAD (CSV + EXCEL)
    # -------------------------------------------------
    files = st.file_uploader(
        "Upload Student Files (CSV / Excel)",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    if not files:
        st.info("Please upload at least one file")
        return

    if len(files) > 10:
        st.error("Maximum 10 files allowed")
        return

    dfs = []

    for f in files:
        try:
            if f.name.endswith(".csv"):
                df_temp = pd.read_csv(f, engine="python", on_bad_lines="skip")
            elif f.name.endswith(".xlsx"):
                df_temp = pd.read_excel(f)
            else:
                st.warning(f"Unsupported file skipped: {f.name}")
                continue

            dfs.append(df_temp)

        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    if not dfs:
        st.error("No valid files uploaded")
        return

    df = pd.concat(dfs, ignore_index=True)

    # -------------------------------------------------
    # ✅ BASIC VALIDATION
    # -------------------------------------------------
    required = {"year", "department", "section", "roll_no", "name"}
    if not required.issubset(df.columns):
        st.error(f"Missing required columns: {required - set(df.columns)}")
        return

    # -------------------------------------------------
    # 🔍 FILTERS
    # -------------------------------------------------
    st.sidebar.header("🔍 Filters")

    department = st.sidebar.selectbox(
        "Department",
        sorted(df["department"].dropna().unique())
    )

    year = st.sidebar.selectbox(
        "Year",
        sorted(df[df["department"] == department]["year"].dropna().unique())
    )

    section = st.sidebar.selectbox(
        "Section",
        sorted(df[(df["department"] == department) & (df["year"] == year)]["section"].dropna().unique())
    )

    filtered_df = df[(df["department"] == department) & (df["year"] == year) & (df["section"] == section)]

    student_option = st.sidebar.selectbox(
        "Student",
        ["All Students"] + sorted(filtered_df["roll_no"].astype(str) + " - " + filtered_df["name"])
    )

    if student_option != "All Students":
        roll = student_option.split(" - ")[0]
        filtered_df = filtered_df[filtered_df["roll_no"].astype(str) == roll]

    st.success(
        f"Department: {department} | Year: {year} | "
        f"Section: {section} | Records: {len(filtered_df)}"
    )

    # -------------------------------------------------
    # 📘 SUBJECT IDENTIFICATION
    # -------------------------------------------------
    assign_cols = [c for c in filtered_df.columns if c.endswith("_assign1") or c.endswith("_assign2")]

    subjects = sorted({c.replace("_assign1", "").replace("_assign2", "") for c in assign_cols})

    # -------------------------------------------------
    # 📊 DEPARTMENT OVERVIEW
    # -------------------------------------------------
    st.subheader("📊 Department Overview")

    total_students = len(filtered_df)
    pass_count = (filtered_df["result"] == "PASS").sum() if "result" in filtered_df.columns else 0
    fail_count = (filtered_df["result"] == "FAIL").sum() if "result" in filtered_df.columns else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", total_students)
    c2.metric("Pass", pass_count)
    c3.metric("Fail", fail_count)

    # -------------------------------------------------
    # ⚠️ ASSIGNMENT RISK
    # -------------------------------------------------
    st.subheader("⚠️ Assignment Risk")

    risk_list = []

    for _, row in filtered_df.iterrows():
        a1_missing, a2_missing = 0, 0

        for s in subjects:
            if pd.isna(row.get(f"{s}_assign1", 0)) or row.get(f"{s}_assign1", 0) == 0:
                a1_missing += 1
            if pd.isna(row.get(f"{s}_assign2", 0)) or row.get(f"{s}_assign2", 0) == 0:
                a2_missing += 1

        if a1_missing or a2_missing:
            risk_list.append({
                "Roll No": row["roll_no"],
                "Name": row["name"],
                "Assign-1 Missing": a1_missing,
                "Assign-2 Missing": a2_missing
            })

    if risk_list:
        risk_df = pd.DataFrame(risk_list)
        st.warning(f"{len(risk_df)} students have assignment issues")
        st.dataframe(risk_df, use_container_width=True)

        st.download_button(
            "⬇️ Download Assignment Risk",
            risk_df.to_csv(index=False).encode("utf-8"),
            "assignment_risk.csv"
        )
    else:
        st.success("No assignment risks 🎉")

    # -------------------------------------------------
    # 📉 SUBJECT FAILURE ANALYSIS
    # -------------------------------------------------
    st.subheader("📉 Subject-wise Failure %")

    fail_data = {}
    for s in subjects:
        ext_col = f"{s}_external"
        if ext_col in filtered_df.columns:
            fail_data[s] = (filtered_df[ext_col] < 40).mean() * 100

    if fail_data:
        st.bar_chart(pd.DataFrame.from_dict(fail_data, orient="index", columns=["Fail %"]))
    else:
        st.info("No external marks data")

    # -------------------------------------------------
    # 🏆 TOP & BOTTOM PERFORMERS
    # -------------------------------------------------
    st.subheader("🏆 Top & Bottom Performers")

    score_cols = [c for c in filtered_df.columns if "_mid" in c or "_assign" in c or "_external" in c]
    filtered_df["Total_Score"] = filtered_df[score_cols].sum(axis=1)

    col1, col2 = st.columns(2)

    with col1:
        st.success("Top 5 Students")
        st.dataframe(
            filtered_df.sort_values("Total_Score", ascending=False)
            .head(5)[["roll_no", "name", "Total_Score"]],
            use_container_width=True
        )

    with col2:
        st.error("Bottom 5 Students")
        st.dataframe(
            filtered_df.sort_values("Total_Score")
            .head(5)[["roll_no", "name", "Total_Score"]],
            use_container_width=True
        )

    # -------------------------------------------------
    # 📋 FINAL TABLE
    # -------------------------------------------------
    st.subheader("📋 Student Records")
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(
        "⬇️ Download Filtered Records",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "filtered_student_records.csv"
    )