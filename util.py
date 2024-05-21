import streamlit as st
import pandas as pd
import os
import base64
import plotly.graph_objects as go
from css_style import *
import io
from constants import *
from chart import *

def show_major_expander(list, major_value, uploaded_file):
    with st.expander(label=major_value):
        col1, col2 = st.columns([8,2])
        with col1:
            updated_df = display_checkbox_get_updated_list(list, major_value, uploaded_file)
            # updated_unchecked_df = get_updated_uncheckbox_df(updated_df)
            df_percent = calculate_percentage(updated_df)
        with col2:
            st.write(generate_color_bar(df_percent, "small"), unsafe_allow_html=True)
        return updated_df, df_percent
    
# Method to calculate percentage of selected checkboxes
def calculate_percentage(df):
    checkbox_values = df['CHECK'].tolist()
    total_checkboxes = len(checkbox_values)
    selected_count = sum(checkbox_values)
    percentage = (selected_count / total_checkboxes) * 100
    return int(percentage)

# Method to create dataframe of selected values
def create_dataframe(checkbox_values, major_area_title):
    selected_values = pd.DataFrame(columns=["CHECK", "MAJOR", "AREAS"])
    selected_values["CHECK"] = checkbox_values.values()
    selected_values["MAJOR"] = major_area_title
    selected_values["AREAS"] = checkbox_values.keys()
    return selected_values

def display_unselected_values(checkbox_values, major_area_title):
    selected_checkbox_values = {key: value for key, value in checkbox_values.items() if not value}
    selected_values = pd.DataFrame(columns=["CHECK", "MAJOR", "AREAS"])
    selected_values["CHECK"] = selected_checkbox_values.values()
    selected_values["MAJOR"] = major_area_title
    selected_values["AREAS"] = selected_checkbox_values.keys()
    return selected_values

def display_unselected_values_v2(dict_values):
    # print(dict_values)
    unchecked_values = {}
    for key, value in dict_values.items():
        if not value:  # If the value is False or empty
            unchecked_values[key] = value
    # unchecked_checkboxes = get_unchecked_checkbox_values(checkbox_values)

    # Convert unchecked_checkboxes dictionary to DataFrame
    df = pd.DataFrame(list(unchecked_values.items()), columns=['Key', 'Value'])
    return df

def display_checkbox_get_updated_list(checkbox_dicts,suffix,uploaded_file):
    main_checkboxes = [st.checkbox(label="CheckAll",key={suffix},label_visibility="hidden")]
    # print(f"***********{suffix}*************")
    if uploaded_file is None: # if template.csv file loaded
        for i, (main_checkbox, checkbox_dict) in enumerate(zip(main_checkboxes, checkbox_dicts)):
                if main_checkbox:
                    for key in checkbox_dict:
                        checkbox_dict[key] = True
                else:
                    for key in checkbox_dict:
                        checkbox_dict[key] = False
    elif uploaded_file is not None: # using upload csv file
        # content = uploaded_file.getvalue().decode("utf-8")
        # # print(len(content))
        # if len(content) > 0:
        #     print(f"uploaded_file is NOT NONE len(content) > 0 main_checkboxes ====> {main_checkboxes}")
        # st.success("File uploaded successfully!")
        # try:
            # Read the Excel file
        df = pd.read_excel(uploaded_file, engine='openpyxl')
            # Display the dataframe
            # st.write(df)
        # except Exception as e:
            # st.error(f"Error: {e}")
    # Display individual checkboxes based on the states
    for checkbox_dict in checkbox_dicts:
        for key in checkbox_dict:
            checkbox_dict[key] = st.checkbox(key, checkbox_dict[key])
    df = pd.DataFrame.from_dict(checkbox_dict, orient='index',columns=['AREAS'])
    df.reset_index(inplace=True)
    df.columns = ['AREAS','CHECK']
    df["MAJOR"] = suffix
    desired_order = ['CHECK','MAJOR','AREAS']
    df_reordered = df[desired_order]
    # print(df_reordered)
    return df_reordered


# checkbox_dicts = [
#     {i: False for i in requirements_list},
#     {i: False for i in planning_and_estimations_list}
# ]

def upload():
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    return uploaded_file


def download_link(df):
    # st.header("Download file")
    csv = df.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="downloaded_data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

#download csv file
def download(df):
    st.download_button(":white[Download CSV ]", df.to_csv(), mime='text/csv', file_name="downloaded_data.csv")

# Create a function to save dataframes to an Excel file in memory
def to_excel(dfs, sheetnames):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for df, sheetname in zip(dfs, sheetnames):
            df.to_excel(writer, sheet_name=sheetname, index=False)
    output.seek(0)
    return output

def download_xlsx(df1,df2,df3,df4):
    # Create a list of dataframes and corresponding sheet names
    dataframes = [df1, df2, df3, df4]
    sheetnames = process_type

    # Generate the Excel file
    excel_data = to_excel(dataframes, sheetnames)
    st.download_button(
        label=':green[Download XLSX]',
        data=excel_data,
        file_name='downloaded_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def upload():
    # st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a XLSX file", type=['xlsx'])
    return uploaded_file

def load_data():
    df = pd.read_csv("data/tmm_template.csv")
    print(df)
    return df

# load csv data and return dataframe of all columns
def load_data_csv(uploaded_file):
    if uploaded_file is None:
        # Load data from local data.csv file
        if os.path.exists("data/tmm_template.csv"):
            df = pd.read_csv("data/tmm_template.csv")
            # return df
        else:
            st.error("No file uploaded and local data.csv file not found.")
            return None
    else:
        # Load data from uploaded file
        df = pd.read_csv(uploaded_file)
    df = df.drop(columns=df.columns[df.columns.str.contains('Unnamed', case=False)])
    df.reset_index(drop=True, inplace=True)
    return df

def read_xlsx_by_sheetname(uploaded_file, sheet_name):
    df = pd.read_excel(
            io=uploaded_file,
            engine='openpyxl',
            sheet_name=sheet_name
            )
    return df
# load xlsx data and return dataframe of all columns
def load_data_xlsx(uploaded_file):
    if uploaded_file is None:
        # Load data from local data/tmm_template.xlsx file
        if os.path.exists("data/tmm_template.xlsx"):
            qa_df = read_xlsx_by_sheetname("data/tmm_template.xlsx",process_type[0])
            auto_df = read_xlsx_by_sheetname("data/tmm_template.xlsx",process_type[1])
            db_df = read_xlsx_by_sheetname("data/tmm_template.xlsx",process_type[2])
            perf_df = read_xlsx_by_sheetname("data/tmm_template.xlsx",process_type[3])
            # return df
        else:
            st.error("No file uploaded and local tmm_template.xlsx file not found.")
            return None
    else:
        # Load data from uploaded file
        qa_df = read_xlsx_by_sheetname(uploaded_file,process_type[0])
        auto_df = read_xlsx_by_sheetname(uploaded_file,process_type[1])
        db_df = read_xlsx_by_sheetname(uploaded_file,process_type[2])
        perf_df = read_xlsx_by_sheetname(uploaded_file,process_type[3])

    qa_df = qa_df.drop(columns=qa_df.columns[qa_df.columns.str.contains('Unnamed', case=False)])
    qa_df.reset_index(drop=True, inplace=True)

    auto_df = auto_df.drop(columns=auto_df.columns[auto_df.columns.str.contains('Unnamed', case=False)])
    auto_df.reset_index(drop=True, inplace=True)

    db_df = db_df.drop(columns=db_df.columns[db_df.columns.str.contains('Unnamed', case=False)])
    db_df.reset_index(drop=True, inplace=True)

    perf_df = perf_df.drop(columns=perf_df.columns[perf_df.columns.str.contains('Unnamed', case=False)])
    perf_df.reset_index(drop=True, inplace=True)

    return qa_df, auto_df, db_df, perf_df

# return dataframe in a list
def get_all_column_data(qa_df,auto_df,db_df,perf_df):
    if qa_df.empty or auto_df.empty or db_df.empty or perf_df.empty:
        st.warning(f"No data found for {qa_df} or {auto_df} or {db_df} or {perf_df}.")
    else:
        qa_all_column_values = qa_df[['CHECK','MAJOR','AREAS']].values.tolist()
        auto_all_column_values = auto_df[['CHECK','MAJOR','AREAS']].values.tolist()
        db_all_column_values = db_df[['CHECK','MAJOR','AREAS']].values.tolist()
        perf_all_column_values = perf_df[['CHECK','MAJOR','AREAS']].values.tolist()
    return qa_all_column_values, auto_all_column_values, db_all_column_values, perf_all_column_values

def get_major_areas_by_process_type(qa_df, auto_df,db_df,perf_df):
    qa_df = qa_df['MAJOR'].unique()
    auto_df = auto_df['MAJOR'].unique()
    db_df = db_df['MAJOR'].unique()
    perf_df = perf_df['MAJOR'].unique()
    return qa_df, auto_df, db_df, perf_df

# Format TRUE / FALSE values with symbols on df
def format_preview_df(df):
    # df = pd.DataFrame(df,columns=['CHECK', 'MAJOR', 'AREAS'])
    def format_boolean_as_checkbox(value):
        if isinstance(value, bool):
            return "✅" if value else "❌"
        return value
    formatted_df = df.map(format_boolean_as_checkbox)
    # st.write(formatted_df)
    st.dataframe(formatted_df, width=700, height=300,hide_index=True)

def get_areas_list(list, major_areas_array):
    sub_area_list_01 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[0]}]
    sub_area_list_02 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[1]}]
    sub_area_list_03 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[2]}]
    sub_area_list_04 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[3]}]
    sub_area_list_05 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[4]}]
    sub_area_list_06 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[5]}]
    sub_area_list_07 = [{ i[2]:i[0] for i in list if i[1] == major_areas_array[6]}]
    return sub_area_list_01, sub_area_list_02, sub_area_list_03, sub_area_list_04, sub_area_list_05, sub_area_list_06, sub_area_list_07

def get_updated_uncheckbox_df(df):
    df = df[df['CHECK'] == False]
    return df