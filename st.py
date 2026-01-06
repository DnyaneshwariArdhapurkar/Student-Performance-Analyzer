import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Student Marks Analysis", layout="centered")

st.title("📊 Student Marks Analysis App")
st.write("Upload a CSV file with columns: Name, Subject, Marks")

uploaded_file = st.file_uploader("Upload Student Marks CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # 🔥 Encoding-safe CSV read
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        # Check required columns
        required_cols = {"Name", "Subject", "Marks"}
        if not required_cols.issubset(df.columns):
            st.error("❌ CSV must contain columns: Name, Subject, Marks")
        else:
            st.subheader("📄 Student Dataset")
            st.dataframe(df)

            # Basic insights
            st.subheader("📈 Basic Insights")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Marks", round(df["Marks"].mean(), 2))
            col2.metric("Highest Marks", df["Marks"].max())
            col3.metric("Lowest Marks", df["Marks"].min())

            # Filter by subject
            st.subheader("🎯 Filter by Subject")
            selected_subject = st.selectbox(
                "Select Subject", df["Subject"].unique()
            )

            filtered_df = df[df["Subject"] == selected_subject]
            st.dataframe(filtered_df)

            # 📊 Student Marks Chart using Streamlit native bar_chart
            st.subheader("📊 Student Marks Bar Chart")
            st.bar_chart(filtered_df.set_index("Name")["Marks"])

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")

else:
    st.info("👆 Please upload a CSV file to see analysis")
