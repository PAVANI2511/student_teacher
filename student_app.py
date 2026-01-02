import streamlit as st

def student_dashboard():
    st.title("🎓 Student Dashboard")
    st.caption("ML Prediction + CGPA Suggestions")

    # ---------------- HELPER ----------------
    def get_marks(mark_str):
        try:
            obtained, total = mark_str.split("/")
            return float(obtained)
        except:
            return None

    # ---------------- INPUTS ----------------
    st.subheader("📘 Enter Internal Marks")
    mid1_str = st.text_input("Mid-1 Marks (obtained/total)", "23/24")
    mid2_str = st.text_input("Mid-2 Marks (obtained/total)", "15/24")
    ass1_str = st.text_input("Assignment-1 Marks (obtained/total)", "3/3")
    ass2_str = st.text_input("Assignment-2 Marks (obtained/total)", "3/3")

    # ---------------- RATIO SELECTION ----------------
    ratio_type = st.selectbox("Select Mid Exam Ratio", ["50:50", "80:20"])

    external_total = st.number_input(
        "External Exam Total Marks",
        min_value=1,
        value=70
    )

    pass_marks = st.number_input(
        "PASS Marks",
        min_value=1,
        value=40
    )

    # ---------------- PREDICT OR SUGGEST ----------------
    option = st.radio("Select Option", ["Predict", "Suggest"])

    # ---------------- CONVERT INPUTS ----------------
    mid1 = get_marks(mid1_str)
    mid2 = get_marks(mid2_str)
    ass1 = get_marks(ass1_str)
    ass2 = get_marks(ass2_str)

    if None in [mid1, mid2, ass1, ass2]:
        st.warning("⚠️ Enter all marks in obtained/total format")
        return

    # ---------------- CALCULATE INTERNAL ----------------
    total_assignment = ass1 + ass2
    if ratio_type == "50:50":
        mid_total = (mid1 + mid2) / 2
    else:  # 80:20
        high = max(mid1, mid2)
        low = min(mid1, mid2)
        mid_total = 0.8 * high + 0.2 * low

    internal_total = mid_total + total_assignment
    st.success(f"📊 Internal Marks: {internal_total:.2f}")

    # ---------------- PREDICT OPTION ----------------
    if option == "Predict":
        expected_external = st.number_input(
            "Enter Expected External Marks",
            min_value=0.0,
            max_value=float(external_total),
            value=35.0
        )

        if st.button("🎯 Show Final Result"):
            final_total = internal_total + expected_external
            st.success(f"🏆 Final Marks (Internal + External): {final_total:.2f}")

            if final_total >= pass_marks:
                st.success("✅ PASS")
            else:
                st.error("❌ FAIL")

    # ---------------- SUGGEST OPTION ----------------
    else:  # Suggest
        if st.button("💡 Show Suggestions"):
            cgpa_targets = {
                "PASS": pass_marks,
                "CGPA 6": 50,
                "CGPA 7": 60,
                "CGPA 8": 70,
                "CGPA 9": 81,
                "CGPA 10": 91
            }

            st.subheader("📈 Required External Marks to Achieve CGPA")
            for label, target in cgpa_targets.items():
                required_external = target - internal_total

                if required_external <= 0:
                    st.success(f"{label}: Already achievable ✅")
                elif required_external <= external_total:
                    st.warning(
                        f"{label}: Need **{required_external:.2f} / {external_total}** in external"
                    )
                else:
                    st.error(
                        f"{label}: ❌ Not possible (needs {required_external:.2f})"
                    )
