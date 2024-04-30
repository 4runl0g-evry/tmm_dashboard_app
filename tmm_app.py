import streamlit as st
import pandas as pd
import io
from util import *
from css_style import *

def show_major_expander(list, major_value, uploaded_file):
    # print(f"***********{major_value}*************")
    with st.expander(major_value):
        col1, col2 = st.columns([8,2])
        with col1:
            updated_df = display_checkbox_get_updated_list(list, major_value, uploaded_file)
            updated_unchecked_df = get_updated_uncheckbox_df(updated_df)
            df_percent = calculate_percentage(updated_df)
        with col2:
            st.write(generate_color_bar(df_percent, "100", "20", "10"), unsafe_allow_html=True)
        return updated_df, updated_unchecked_df, df_percent

def main():

    st.image('images/logo_white_bkgnd.png', width=170)
    header_style("QA PROCESS & AUTOMATION TESTING MATURITY ASSESSMENT",22,"center")
    with st.sidebar:
        st.header("Upload Existing File")
        uploaded_file = upload()
        print(f"*********  File Uploaded ? ********* {uploaded_file}")
        
    tab_titles = [ "Dashboard", "Maturity Assessment",  "Pending Areas / Gaps", "Data preview"]
    tabs = st.tabs(tab_titles)
    load_csv_df = load_data_csv_v2(uploaded_file)
    get_data_list = get_all_column_data(load_csv_df)
    # print(get_data_list)
    major_areas_array = load_csv_df['MAJOR'].unique()
    sub_area_list_01, sub_area_list_02, sub_area_list_03, sub_area_list_04, sub_area_list_05, sub_area_list_06, sub_area_list_07 = get_generic_values(get_data_list, major_areas_array)

    with tabs[1]:
        header_style("QA PROCESS",20,"left")
        updated_df1, updated_unchecked_df1, df1_percent = show_major_expander(sub_area_list_01, major_areas_array[0], uploaded_file)
        updated_df2, updated_unchecked_df2, df2_percent = show_major_expander(sub_area_list_02, major_areas_array[1], uploaded_file)
        updated_df3, updated_unchecked_df3, df3_percent = show_major_expander(sub_area_list_03, major_areas_array[2], uploaded_file)
        updated_df4, updated_unchecked_df4, df4_percent = show_major_expander(sub_area_list_04, major_areas_array[3], uploaded_file)
        updated_df5, updated_unchecked_df5, df5_percent = show_major_expander(sub_area_list_05, major_areas_array[4], uploaded_file)
        updated_df6, updated_unchecked_df6, df6_percent = show_major_expander(sub_area_list_06, major_areas_array[5], uploaded_file)
        updated_df7, updated_unchecked_df7, df7_percent = show_major_expander(sub_area_list_07, major_areas_array[6], uploaded_file)
    
    with tabs[0]:
        options = st.selectbox('Select Major Areas: ',
                        ['QA PROCESS', 'AUTOMATION TESTING'])
        if options == "QA PROCESS":
            color, caption, rating = get_color_and_caption((df1_percent+df2_percent)/2)
            plot_gauge(rating,  color, caption, options, 5)
            col1, col2 = st.columns(2)
            with col1:
                st.write(major_areas_array[0])
                st.write(major_areas_array[1])
                st.write(major_areas_array[2])
                st.write(major_areas_array[3])
                st.write(major_areas_array[4])
                st.write(major_areas_array[5])
                st.write(major_areas_array[6])
            with col2:
                st.write(generate_color_bar(df1_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df2_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df3_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df4_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df5_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df6_percent, "300", "30", "15"), unsafe_allow_html=True)
                st.write("  \n")
                st.write(generate_color_bar(df7_percent, "300", "30", "15"), unsafe_allow_html=True)
        else:
            plot_gauge(0, colour_code_range(0), "", options, 5)

    with tabs[2]:
        # Preview only unchecked items from df 
        merged_updated_uncheckbox_df = pd.concat([updated_unchecked_df1, updated_unchecked_df2], ignore_index=True)
        format_preview_df(merged_updated_uncheckbox_df)
    with tabs[3]:
       # Data preview
        option = st.radio("Display data from: ", ('Updated', 'Template / Uploaded'),horizontal=True)
        merged_updated_df = pd.concat([updated_df1, updated_df2], ignore_index=True)
        if option == 'Updated':
            format_preview_df(merged_updated_df)
        elif option == 'Template / Uploaded':
            format_preview_df(load_csv_df)

    with st.sidebar:
        download(merged_updated_df)
        maturity_level_status()
                

if __name__ == "__main__":
    main()