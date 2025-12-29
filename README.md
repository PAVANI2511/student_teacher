# 🎓 Student Performance Evaluation System

This project is a **rule-based student performance evaluation system** developed using **Python and Streamlit**.  
It predicts student outcomes and provides academic insights based on **internal assessments, previous performance, and external exam prediction**.

---

## 📌 Project Features

### 👩‍🎓 Student Module
- Enter Mid-1, Mid-2, and Assignment marks
- Choose internal calculation method:
  - 50 : 50
  - 80 : 20
- Predict final result using expected external marks
- Get CGPA-based guidance for required external marks

---

### 👨‍🏫 Teacher Module
- Upload student data using CSV file
- Uses:
  - Mid-1 marks
  - Mid-2 marks
  - Assignment marks
  - Previous academic marks
  - Question paper difficulty level
- Predicts:
  - External marks
  - Total marks
  - PASS / FAIL status
- Displays:
  - Pass / Fail count
  - Roll numbers of passed and failed students
  - Bar chart and Pie chart for visual analysis

---

## 📊 Technologies Used

- **Python**
- **Streamlit** – Web interface
- **Pandas** – Data handling
- **Matplotlib** – Graphs and visualization

---

## 📁 CSV Format (Teacher Upload)

```csv
roll_no,name,mid1,mid2,assignment,previous_marks