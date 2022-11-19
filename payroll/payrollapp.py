import streamlit as st
import pandas as pd
import numpy as np

import plotly
import plotly.express as px
from matplotlib.pyplot import plot as plt

st.title("Pay Roll Attendance Analyzer")

upload_file = st.file_uploader("Please upload an .xlsx file", type = 'xlsx')

if upload_file is not None:
    data_sheets = pd.read_excel(upload_file, sheet_name = None)
    
    with st.form("my_form"):
        
        sheets = st.selectbox(
            "Select which Month you want to analyze attendance for.",
            options=list(data_sheets.keys()),
        )
        
        submit_button = st.form_submit_button(label="Submit")
        
    if sheets:
        data = data_sheets[sheets]

        st.write(f"Showing sample of {sheets} uploaded below:")
        st.dataframe(data.head(5))

        # Tranform dataframe (Easier for later analysis)
        data = data.T
        data.columns = data.iloc[0] # Rename columns

        # Remove first row, as they are now column names
        data = data[1:]

        # Fillna
        data = data.fillna('A')

        # Get base dictionary (all unique possibilities mapped to 0)
        base_dict = {i : 0 for i in np.unique(data.values.flatten())}

        results = {} #Initialize empty dictionary to store results
        # Loop to count attendence per person
        for col in data.columns:
            base = base_dict.copy() # Initialize possibilities
            tmp = data[col].value_counts().to_dict() # Get inidividuals attendence counts
            base.update(tmp)
            results[col] = base

        payroll = pd.DataFrame(results).T

        st.subheader(f'{sheets} Pay Roll Attendance Table')
        st.dataframe(payroll)

        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(payroll)

        st.download_button(
            label=f"Download {sheets} Attendance Table as CSV",
            data=csv,
            file_name=f'{sheets}_attendance.csv',
            mime='text/csv',
            )
        st.subheader(f'{sheets} Pay Roll Attendance Plot')
        fig = px.bar(payroll.sort_values('A', ascending = True),  title=f"{sheets} Payroll Top 10 Missing Attendence")
        fig.update_layout(
                xaxis_title="Names",
                yaxis_title="Attendance")
        st.plotly_chart(fig, use_container_width=True)
    