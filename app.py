import streamlit as st
import pandas as pd
from pathlib import Path

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

# Custom CSS to set the width of the dataframe and enable text wrapping
st.markdown("""
<style>
    .stDataFrame {
        width: 100%;
    }
    .dataframe {
        font-size: 12px;
    }
    .dataframe td {
        white-space: normal;
        text-align: left !important;
    }
    .dataframe th {
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

# Display the filtered dataframe with custom column widths
st.dataframe(
    filtered_df.reset_index(drop=True),
    column_config={
        "Variable Name": st.column_config.Column(width=150),
        "Description": st.column_config.Column(width=300),
        "Source File": st.column_config.Column(width=100),
        "Code=Value": st.column_config.Column(width=200),
    },
    height=500,  # Set the height of the dataframe
    use_container_width=True  # Use the full width of the container
)

# Display statistics
st.sidebar.write(f"Total variables: {len(filtered_df)}")
st.sidebar.write(f"Exams represented: {', '.join(filtered_df['Source File'].unique())}")
