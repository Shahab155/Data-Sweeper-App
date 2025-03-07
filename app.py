import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Set page config for title and layout
st.set_page_config(page_title="Data Cleaner and Convertor", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
      with open(file_name,"r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("styles.css")  


# Display the main heading at the top
st.title(f"🧹Data Cleaner and Convertor")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# Sidebar for file upload and conversion options
st.sidebar.title("File Operations")
uploaded_files = st.sidebar.file_uploader("Upload Your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=False)

# Initialize df to None
df = None

# Conversion Options in Sidebar
if uploaded_files:
    st.sidebar.subheader("Convert File")
    conversion_type = st.sidebar.radio("Convert file to:", ["CSV", "Excel"])

    # Read file after upload
    if uploaded_files.name.endswith('.csv'):
        df = pd.read_csv(uploaded_files)
    else:
        df = pd.read_excel(uploaded_files)

    buffer = BytesIO()
    if conversion_type == "CSV":
        df.to_csv(buffer, index=False)
        file_name = uploaded_files.name.replace(".xlsx", ".csv").replace(".csv", ".csv")
        mime_type = "text/csv"
    elif conversion_type == "Excel":
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        file_name = uploaded_files.name.replace(".xlsx", ".xlsx").replace(".csv", ".xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    buffer.seek(0)

    # Download Button in Sidebar
    st.sidebar.download_button(
        label=f"Download {file_name} as {conversion_type}",
        data=buffer,
        file_name=file_name,
        mime=mime_type
    )

# Main content area
if uploaded_files and df is not None:
    # File Details and Data Display
    st.title(f"Data Preview for {uploaded_files.name}")
    st.write("Showing the first 5 rows of the uploaded data:")
    st.dataframe(df.head())

    # Data Cleaning Section
    st.subheader("Data Cleaning Options")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Remove Duplicates"):
            df.drop_duplicates(inplace=True)
            st.write("Duplicates Removed!")
            st.dataframe(df.head())

    with col2:
        if st.button("Fill Missing Values"):
            numeric_cols = df.select_dtypes(include=["number"]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Missing Values have been Filled!")
            st.dataframe(df.head())

    # Remove Nulls Button
    if st.button("Remove Null Values"):
        df.dropna(inplace=True)
        st.write("Null Values Removed!")
        st.dataframe(df.head())

    # Column Selection
    st.subheader("Select Columns to Keep")
    selected_columns = st.multiselect("Choose Columns", df.columns, default=df.columns)
    df = df[selected_columns]
    st.write(f"Selected Columns: {', '.join(selected_columns)}")
    st.dataframe(df.head())

    # Visualization Section
    st.subheader("📊 Data Visualization")
    if st.checkbox("Show Visualization"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

else:
    st.warning("Please upload a file to start.")


