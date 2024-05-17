import streamlit as st
import pandas as pd
import os
import base64
import plotly.graph_objects as go
from css_style import *

# major_areas = ["REQUIREMENTS", "PLANNING & ESTIMATIONS"]
process_type = ["QA PROCESS", "AUTOMATION PROCESS"]

def show_major_expander(list, major_value, uploaded_file):
    # print(f"***********{major_value}*************")
    with st.expander(label=major_value):
        col1, col2 = st.columns([8,2])
        with col1:
            updated_df = display_checkbox_get_updated_list(list, major_value, uploaded_file)
            updated_unchecked_df = get_updated_uncheckbox_df(updated_df)
            df_percent = calculate_percentage(updated_df)
        with col2:
            st.write(generate_color_bar(df_percent, "small"), unsafe_allow_html=True)
        return updated_df, updated_unchecked_df, df_percent
    
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

def download(df):
    st.download_button(":white[Download CSV ]", df.to_csv(), mime='text/csv', file_name="downloaded_data.csv")

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
            # return df
        else:
            st.error("No file uploaded and local tmm_template.xlsx file not found.")
            return None
    else:
        # Load data from uploaded file
        qa_df = read_xlsx_by_sheetname(uploaded_file,process_type[0])
        auto_df = read_xlsx_by_sheetname(uploaded_file,process_type[1])
    qa_df = qa_df.drop(columns=qa_df.columns[qa_df.columns.str.contains('Unnamed', case=False)])
    qa_df.reset_index(drop=True, inplace=True)

    auto_df = auto_df.drop(columns=auto_df.columns[auto_df.columns.str.contains('Unnamed', case=False)])
    auto_df.reset_index(drop=True, inplace=True)

    return qa_df, auto_df

# return dataframe in a list
def get_all_column_data(qa_df,auto_df):
    if qa_df.empty or auto_df.empty:
        st.warning(f"No data found for {qa_df} or {auto_df}.")
    else:
        qa_all_column_values = qa_df[['CHECK','MAJOR','AREAS']].values.tolist()
        auto_all_column_values = auto_df[['CHECK','MAJOR','AREAS']].values.tolist()
    return qa_all_column_values, auto_all_column_values

def get_major_areas_by_process_type(qa_df, auto_df):
    qa_df = qa_df['MAJOR'].unique()
    auto_df = auto_df['MAJOR'].unique()
    return qa_df, auto_df

# Format TRUE / FALSE values with symbols on df
def format_preview_df(df):
    # df = pd.DataFrame(df,columns=['CHECK', 'MAJOR', 'AREAS'])
    def format_boolean_as_checkbox(value):
        if isinstance(value, bool):
            return "✅" if value else "❌"
        return value
    formatted_df = df.map(format_boolean_as_checkbox)
    st.write(formatted_df)
    # st.dataframe(formatted_df, width=700, height=300)

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

def generate_color_bar(percentage, bar_size):
    # Determine color based on percentage
    bar_color = colour_code_range(percentage)
    if bar_size == "large":
        color_bar = f"""
        <div style="position: relative; width: 300px; height: 30px; background-color: {bar_color}; border-radius: 15px;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: Arial, sans-serif; font-size: 12px; color: black;">{percentage}%</div>
        </div>
        """
    elif bar_size =="small":
        color_bar = f"""
        <div style="position: relative; width: 100px; height: 20px; background-color: {bar_color}; border-radius: 10px;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: Arial, sans-serif; font-size: 12px; color: black;">{percentage}%</div>
        </div>
        """
    return color_bar

def plot_gauge(
            indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
        ):
            fig = go.Figure(
                go.Indicator(
                    value=int(indicator_number), #rating
                    mode="gauge", # chencg to gauge+number, to display both guage & number
                    domain={"x": [0, 1], "y": [0, 1]},
                    number={
                        "suffix": indicator_suffix, #caption
                        "font.size": 20,
                    },
                    gauge={
                        "axis": {"range": [0, max_bound], "tickwidth": 1}, #meter_max_range
                        "bar": {"color": indicator_color}, #color
                    },
                    title={
                        "text": indicator_title, #select_options
                        "font": {"size": 20},
                    },
                )
            )
            fig.update_layout(
                # paper_bgcolor="lightgrey",
                height=353, #353
                title_text=indicator_suffix,
                # margin=dict(l=1, r=10, t=50, b=20, pad=8),
                title_x=0.46,title_y=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

# return color codes based on percentage
def colour_code_range(percentage):
    # D14C36 (red - =0%), 387E99 (blue - 0%-20%), FFC000 (light orange - 20-40%), 
    # F48735 (dark orange - 40-60%), 00BD32 (green - 80-100%)
    if percentage == 0: color = "red"
    elif percentage < 20: color = "#387E99"
    elif percentage < 40: color = "yellow"
    elif percentage < 60: color = "#FFC000"
    elif percentage < 80: color = "#F48735"
    else: color = "#00BD32"
    return color

def get_color_and_caption(percentage):
    # D14C36 (red - =0%), 387E99 (blue - 0%-20%), FFC000 (light orange - 20-40%), 
    # F48735 (dark orange - 40-60%), 00BD32 (green - 80-100%)
    if percentage == 0: color = "red"; caption = "LEVEL 0"; rating=1
    elif percentage < 20: color = "#387E99"; caption = "LEVEL 1"; rating=1
    elif percentage < 40: color = "yellow"; caption = "LEVEL 2"; rating=2
    elif percentage < 60: color = "#FFC000"; caption = "LEVEL 3"; rating=3
    elif percentage < 80: color = "#F48735"; caption = "LEVEL 4"; rating=4
    else: color = "#00BD32"; caption = "LEVEL 5"; rating=5
    return color, caption, rating

def display_area_table(qa_major_areas_array, p1, p2, p3, p4, p5, p6, p7):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'><u>AREAS</u></p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'><u>CURRENT STATUS</u></p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[0])
    with col2:
        st.write(generate_color_bar(p1, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[1])
    with col2:
        st.write(generate_color_bar(p2, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[2])
    with col2:
        st.write(generate_color_bar(p3, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[3])
    with col2:
        st.write(generate_color_bar(p4, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[4])
    with col2:
        st.write(generate_color_bar(p5, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[5])
    with col2:
        st.write(generate_color_bar(p6, "large"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(qa_major_areas_array[6])
    with col2:
        st.write(generate_color_bar(p7, "large"), unsafe_allow_html=True)