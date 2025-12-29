import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Evaluation System",
    layout="centered"
)

st.title("🎓 Student Performance Evaluation System")
st.caption("Rule-Based Internal + External Prediction System")

# ---------------- CLEAN CSS (NO LEGEND LINE) ----------------
st.markdown("""
<style>
.cgpa-card {
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 16px;
    font-weight: 500;
    background-color: #ffffff;
    border-left: 6px solid #cccccc;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.achievable {
    border-left-color: #2e7d32;
    color: #2e7d32;
}

.effort {
    border-left-color: #f9a825;
    color: #8d6e00;
}

.not-possible {
    border-left-color: #c62828;
    color: #c62828;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def get_marks(mark_str):
    try:
        obtained, total = mark_str.split("/")
        return float(obtained)
    except:
        return None

def calculate_internal(mid1, mid2, assignment, method):
    if method == "50 : 50":
        return ((mid1 + mid2) / 2) + assignment
    else:
        high_mid = max(mid1, mid2)
        low_mid = min(mid1, mid2)
        return (0.8 * high_mid) + (0.2 * low_mid) + assignment

def show_cgpa_suggestions(internal_marks, external_total):
    cgpa_targets = {
        "PASS (40+)": 40,
        "CGPA 6 (51–60)": 51,
        "CGPA 7 (61–70)": 61,
        "CGPA 8 (71–80)": 71,
        "CGPA 9 (81–90)": 81,
        "CGPA 10 (91–100)": 91
    }

    for label, target in cgpa_targets.items():
        required = target - internal_marks

        if required <= 0:
            css_class = "cgpa-card achievable"
            text = f"{label}: Achievable with current internal marks"
        elif required <= external_total:
            css_class = "cgpa-card effort"
            text = f"{label}: Need {required:.2f} marks (out of {external_total})"
        else:
            css_class = "cgpa-card not-possible"
            text = f"{label}: Not possible (needs {required:.2f})"

        st.markdown(
            f"<div class='{css_class}'>{text}</div>",
            unsafe_allow_html=True
        )

# ---------------- ROLE ----------------
role = st.sidebar.selectbox("Select Mode", ["Student", "Teacher"])
# ===================== STUDENT ====================
if role == "Student":
    st.header("👩‍🎓 Student Dashboard")

    mid1_str = st.text_input("Mid-1 Marks (obtained/total)", "23/24")
    mid2_str = st.text_input("Mid-2 Marks (obtained/total)", "15/24")
    assignment_str = st.text_input("Assignment Marks (obtained/total)", "6/6")

    method = st.radio("Internal Calculation Method", ["50 : 50", "80 : 20"])
    external_total = st.number_input("External Exam Total Marks", min_value=1, value=70)

    external_mode = st.radio(
        "External Mode",
        ["Predict External Marks", "Suggest Required External Marks"]
    )

    if external_mode == "Predict External Marks":
        external_str = st.text_input("Expected External Marks (obtained/total)", "40/70")

    if st.button("Calculate Result"):
        mid1 = get_marks(mid1_str)
        mid2 = get_marks(mid2_str)
        assignment = get_marks(assignment_str)

        if None in [mid1, mid2, assignment]:
            st.error("Invalid input format")
        else:
            internal = calculate_internal(mid1, mid2, assignment, method)
            st.info(f"Internal Marks: {internal:.2f}")

            if external_mode == "Predict External Marks":
                external = get_marks(external_str)
                total = internal + external
                st.success(f"Total Marks: {total:.2f}")
                st.success("PASS" if total >= 40 else "FAIL")
            else:
                show_cgpa_suggestions(internal, external_total)
# ===================== TEACHER ====================
else:
    st.header("👨‍🏫 Teacher Dashboard")

    method = st.radio("Internal Calculation Method", ["50 : 50", "80 : 20"])
    paper_level = st.radio("Question Paper Level", ["Easy", "Moderate", "Hard"])
    external_total = st.number_input("External Exam Total Marks", min_value=1, value=70)

    uploaded_file = st.file_uploader(
        "Upload CSV (roll_no, name, mid1, mid2, assignment, previous_marks)",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=",", engine="python")

        predicted_external = []
        totals = []
        results = []

        for _, row in df.iterrows():
            internal = calculate_internal(
                row["mid1"], row["mid2"], row["assignment"], method
            )

            prev = row["previous_marks"]
            if prev >= 75:
                base_ext = 50
            elif prev >= 60:
                base_ext = 45
            elif prev >= 50:
                base_ext = 40
            else:
                base_ext = 35

            if paper_level == "Easy":
                ext = base_ext + 5
            elif paper_level == "Hard":
                ext = base_ext - 5
            else:
                ext = base_ext

            ext = max(0, min(ext, external_total))
            total = internal + ext

            predicted_external.append(ext)
            totals.append(total)
            results.append("PASS" if total >= 50 else "FAIL")

        df["Predicted_External"] = predicted_external
        df["Total_Marks"] = totals
        df["Predicted_Result"] = results

        pass_count = (df["Predicted_Result"] == "PASS").sum()
        fail_count = (df["Predicted_Result"] == "FAIL").sum()

        st.subheader("📊 Prediction Summary")
        st.write(f"PASS: {pass_count} | FAIL: {fail_count}")

        fig, ax = plt.subplots()
        ax.bar(["PASS", "FAIL"], [pass_count, fail_count])
        ax.set_ylabel("Number of Students")
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        ax2.pie([pass_count, fail_count], labels=["PASS", "FAIL"],
                autopct="%1.1f%%", startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)

        st.subheader("📋 Detailed Table")
        st.dataframe(df)

# ---------------- FOOTER ----------------
st.markdown("---")