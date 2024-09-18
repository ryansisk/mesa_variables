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

st.title('MESA Variable Name Description Table')

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

# Configure AgGrid options
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_default_column(
    resizable=True, 
    filterable=True, 
    sorteable=True, 
    editable=False
)
gb.configure_column("Variable Name", width=150)
gb.configure_column("Description", width=300)
gb.configure_column("Source File", width=100)
gb.configure_column("Code=Value", width=200, wrapText=True, autoHeight=True)
gb.configure_selection('single')
grid_options = gb.build()

# Display the AgGrid
grid_response = AgGrid(
    filtered_df,
    gridOptions=grid_options,
    height=500,
    width='100%',
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=False,
    allow_unsafe_jscode=True
)

# Display statistics
st.sidebar.write(f"Total variables: {len(filtered_df)}")
st.sidebar.write(f"Exams represented: {', '.join(filtered_df['Source File'].unique())}")

# Display selected row (if any)
selected_rows = grid_response['selected_rows']
if selected_rows:
    st.write("Selected row:")
    st.json(selected_rows[0])
