import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    # Replace this with your actual data loading method
    df = pd.read_csv('data/exam_data.csv')
    return df

df = load_data()

st.title('Variable Name Description Table')

# Sidebar for exam selection
exams = df['Source File'].unique()
selected_exams = st.sidebar.multiselect('Select Exams', exams, default=exams)

# Filter dataframe based on selected exams
filtered_df = df[df['Source File'].isin(selected_exams)]

# Search functionality
search_term = st.text_input('Search for a variable name or description:')

if search_term:
    filtered_df = filtered_df[
        filtered_df['Variable Name'].str.contains(search_term, case=False) |
        filtered_df['Description'].str.contains(search_term, case=False)
    ]

# Display the filtered dataframe
st.dataframe(filtered_df)

# Display statistics
st.sidebar.write(f"Total variables: {len(filtered_df)}")
st.sidebar.write(f"Exams represented: {', '.join(filtered_df['Source File'].unique())}")
