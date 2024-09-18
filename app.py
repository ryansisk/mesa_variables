import streamlit as st
import pandas as pd
from pathlib import Path
from awesome_table import AwesomeTable
from awesome_table.column import (Column, ColumnDType)

# Load the data
@st.cache_data
def load_data():

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/exam_data.csv'
    df = pd.read_csv(DATA_FILENAME)

    if df.columns[0] == 'Unnamed: 0':
        df = df.drop(columns=['Unnamed: 0'])

    return df

df = load_data()

st.set_page_config(page_title='MESA Variable Name Description Table', layout='wide')
#st.title('')

# Sidebar for exam selection
exams = df['Source File'].unique()
selected_exams = st.sidebar.multiselect('Select Exams', exams, default=exams)

# Filter dataframe based on selected exams
filtered_df = df[df['Source File'].isin(selected_exams)]

# Search functionality
#search_term = st.text_input('Search for a variable name or description:')

#if search_term:
#    filtered_df = filtered_df[
#        filtered_df['Variable Name'].str.contains(search_term, case=False) |
#        filtered_df['Description'].str.contains(search_term, case=False)
#    ]

# Display the filtered dataframe
#st.dataframe(filtered_df, use_container_width=True)

AwesomeTable(pd.filtered_df, columns=[
    Column(name='Variable Name', label='Variable ID'),
    Column(name='Description', label='Variable Definition'),
    Column(name='Type', label='Data Type'),
    Column(name='Code=Value', label='Code Definitions'),
    Column(name='Source file', label='Exam'),
], show_search=True)

# Display statistics
st.sidebar.write(f"Total variables: {len(filtered_df)}")
st.sidebar.write(f"Exams represented: {', '.join(filtered_df['Source File'].unique())}")
