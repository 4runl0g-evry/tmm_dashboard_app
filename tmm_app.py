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
            st.write(generate_color_bar(df_percent, "small"), unsafe_allow_html=True)
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
    qa_process_data_df, automation_process_data_df = load_data_xlsx(uploaded_file)
    qa_list, auto_list = get_all_column_data(qa_process_data_df,automation_process_data_df)
    qa_major_areas_array, auto_major_areas_array = get_major_areas_by_process_type(qa_process_data_df, automation_process_data_df)
    qa_sub_area_list_01, qa_sub_area_list_02, qa_sub_area_list_03, qa_sub_area_list_04, qa_sub_area_list_05, qa_sub_area_list_06, qa_sub_area_list_07 = get_areas_list(qa_list, qa_major_areas_array)
    auto_sub_area_list_01, auto_sub_area_list_02, auto_sub_area_list_03, auto_sub_area_list_04, auto_sub_area_list_05, auto_sub_area_list_06, auto_sub_area_list_07 = get_areas_list(auto_list, auto_major_areas_array)

    with tabs[1]:
        header_style(process_type[0],18,"center")
        updated_df1, updated_unchecked_df1, df1_percent = show_major_expander(qa_sub_area_list_01, qa_major_areas_array[0], uploaded_file)
        updated_df2, updated_unchecked_df2, df2_percent = show_major_expander(qa_sub_area_list_02, qa_major_areas_array[1], uploaded_file)
        updated_df3, updated_unchecked_df3, df3_percent = show_major_expander(qa_sub_area_list_03, qa_major_areas_array[2], uploaded_file)
        updated_df4, updated_unchecked_df4, df4_percent = show_major_expander(qa_sub_area_list_04, qa_major_areas_array[3], uploaded_file)
        updated_df5, updated_unchecked_df5, df5_percent = show_major_expander(qa_sub_area_list_05, qa_major_areas_array[4], uploaded_file)
        updated_df6, updated_unchecked_df6, df6_percent = show_major_expander(qa_sub_area_list_06, qa_major_areas_array[5], uploaded_file)
        updated_df7, updated_unchecked_df7, df7_percent = show_major_expander(qa_sub_area_list_07, qa_major_areas_array[6], uploaded_file)

        header_style(process_type[1],18,"center")
        auto_updated_df1, auto_updated_unchecked_df1, auto_df1_percent = show_major_expander(auto_sub_area_list_01, auto_major_areas_array[0], uploaded_file)
        auto_updated_df2, auto_updated_unchecked_df2, auto_df2_percent = show_major_expander(auto_sub_area_list_02, auto_major_areas_array[1], uploaded_file)
        auto_updated_df3, auto_updated_unchecked_df3, auto_df3_percent = show_major_expander(auto_sub_area_list_03, auto_major_areas_array[2], uploaded_file)
        auto_updated_df4, auto_updated_unchecked_df4, auto_df4_percent = show_major_expander(auto_sub_area_list_04, auto_major_areas_array[3], uploaded_file)
        auto_updated_df5, auto_updated_unchecked_df5, auto_df5_percent = show_major_expander(auto_sub_area_list_05, auto_major_areas_array[4], uploaded_file)
        auto_updated_df6, auto_updated_unchecked_df6, auto_df6_percent = show_major_expander(auto_sub_area_list_06, auto_major_areas_array[5], uploaded_file)
        auto_updated_df7, auto_updated_unchecked_df7, auto_df7_percent = show_major_expander(auto_sub_area_list_07, auto_major_areas_array[6], uploaded_file)
        
    with tabs[0]:
        options = st.selectbox('Select Major Areas: ',process_type)
        if options == process_type[0]:
            color, caption, rating = get_color_and_caption((df1_percent+df2_percent+df3_percent+df4_percent+df5_percent+df6_percent+df7_percent)/2)
            plot_gauge(rating,  color, caption, options, 5)
            display_area_table(qa_major_areas_array,df1_percent, df2_percent,
                               df3_percent, df4_percent, df5_percent, df6_percent, df7_percent)
        elif options == process_type[1]:
            color, caption, rating = get_color_and_caption((df1_percent+df2_percent+df3_percent+df4_percent+df5_percent+df6_percent+df7_percent)/2)
            plot_gauge(rating,  color, caption, options, 5)
            display_area_table(auto_major_areas_array,auto_df1_percent, auto_df2_percent, auto_df3_percent, 
                               auto_df4_percent, auto_df5_percent, auto_df6_percent, auto_df7_percent)
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
            format_preview_df(qa_process_data_df)
            # format_preview_df(automation_process_data_df)

    with st.sidebar:
        # download(merged_updated_df)
        maturity_level_status()
                

if __name__ == "__main__":
    main()