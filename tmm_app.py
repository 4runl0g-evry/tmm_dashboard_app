import streamlit as st
import pandas as pd
import io
from util import *
from css_style import *
from chart import *

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

    # MATURITY ASSESSMENT TAB
    with tabs[1]:
        header_style(process_type[0],18,"center")
        qa_updated_df1, qa_updated_unchecked_df1, qa_df1_percent = show_major_expander(qa_sub_area_list_01, qa_major_areas_array[0], uploaded_file)
        qa_updated_df2, qa_updated_unchecked_df2, qa_df2_percent = show_major_expander(qa_sub_area_list_02, qa_major_areas_array[1], uploaded_file)
        qa_updated_df3, qa_updated_unchecked_df3, qa_df3_percent = show_major_expander(qa_sub_area_list_03, qa_major_areas_array[2], uploaded_file)
        qa_updated_df4, qa_updated_unchecked_df4, qa_df4_percent = show_major_expander(qa_sub_area_list_04, qa_major_areas_array[3], uploaded_file)
        qa_updated_df5, qa_updated_unchecked_df5, qa_df5_percent = show_major_expander(qa_sub_area_list_05, qa_major_areas_array[4], uploaded_file)
        qa_updated_df6, qa_updated_unchecked_df6, qa_df6_percent = show_major_expander(qa_sub_area_list_06, qa_major_areas_array[5], uploaded_file)
        qa_updated_df7, qa_updated_unchecked_df7, qa_df7_percent = show_major_expander(qa_sub_area_list_07, qa_major_areas_array[6], uploaded_file)

        header_style(process_type[1],18,"center")
        auto_updated_df1, auto_updated_unchecked_df1, auto_df1_percent = show_major_expander(auto_sub_area_list_01, auto_major_areas_array[0], uploaded_file)
        auto_updated_df2, auto_updated_unchecked_df2, auto_df2_percent = show_major_expander(auto_sub_area_list_02, auto_major_areas_array[1], uploaded_file)
        auto_updated_df3, auto_updated_unchecked_df3, auto_df3_percent = show_major_expander(auto_sub_area_list_03, auto_major_areas_array[2], uploaded_file)
        auto_updated_df4, auto_updated_unchecked_df4, auto_df4_percent = show_major_expander(auto_sub_area_list_04, auto_major_areas_array[3], uploaded_file)
        auto_updated_df5, auto_updated_unchecked_df5, auto_df5_percent = show_major_expander(auto_sub_area_list_05, auto_major_areas_array[4], uploaded_file)
        auto_updated_df6, auto_updated_unchecked_df6, auto_df6_percent = show_major_expander(auto_sub_area_list_06, auto_major_areas_array[5], uploaded_file)
        auto_updated_df7, auto_updated_unchecked_df7, auto_df7_percent = show_major_expander(auto_sub_area_list_07, auto_major_areas_array[6], uploaded_file)
        
    # DASHBOARD TAB
    with tabs[0]:
        options = st.selectbox('Select Major Areas: ',process_type)
        if options == process_type[0]:
            color, caption, rating = get_color_and_caption((qa_df1_percent+qa_df2_percent+qa_df3_percent
                                                            +qa_df4_percent+qa_df5_percent+qa_df6_percent+qa_df7_percent)/7)
            plot_gauge(rating,  color, caption, options, 5)
            display_area_table(qa_major_areas_array,qa_df1_percent, qa_df2_percent,
                               qa_df3_percent, qa_df4_percent, qa_df5_percent, qa_df6_percent, qa_df7_percent)
        elif options == process_type[1]:
            color, caption, rating = get_color_and_caption((auto_df1_percent+auto_df2_percent+auto_df3_percent
                                                            +auto_df4_percent+auto_df5_percent+auto_df6_percent+auto_df7_percent)/7)
            plot_gauge(rating,  color, caption, options, 5)
            display_area_table(auto_major_areas_array,auto_df1_percent, auto_df2_percent, auto_df3_percent, 
                               auto_df4_percent, auto_df5_percent, auto_df6_percent, auto_df7_percent)
        else:
            plot_gauge(0, colour_code_range(0), "", options, 5)

    # PENDING AREAS / GAPS TAB
    with tabs[2]:
        # Pie chart for unchecked items
        header_style(process_type[0],18,"center")
        qa_pie_chart = {qa_major_areas_array[0]:qa_df1_percent,
                          qa_major_areas_array[1]:qa_df2_percent,
                          qa_major_areas_array[2]:qa_df3_percent,
                          qa_major_areas_array[3]:qa_df4_percent,
                          qa_major_areas_array[4]:qa_df5_percent,
                          qa_major_areas_array[5]:qa_df6_percent,
                          qa_major_areas_array[6]:qa_df7_percent}
        qa_fig = pie_chart(qa_pie_chart)
        st.plotly_chart(qa_fig)

        header_style(process_type[1],18,"center")
        auto_pie_chart = {auto_major_areas_array[0]:auto_df1_percent,
                          auto_major_areas_array[1]:auto_df2_percent,
                          auto_major_areas_array[2]:auto_df3_percent,
                          auto_major_areas_array[3]:auto_df4_percent,
                          auto_major_areas_array[4]:auto_df5_percent,
                          auto_major_areas_array[5]:auto_df6_percent,
                          auto_major_areas_array[6]:auto_df7_percent}
        auto_fig = pie_chart(auto_pie_chart)
        st.plotly_chart(auto_fig)

    # DATA PREVIEW
    with tabs[3]:
        # Data preview
        option = st.radio("Display data from: ", ('Updated', 'Template / Uploaded'),horizontal=True)
        qa_merged_updated_df = pd.concat([qa_updated_df1, qa_updated_df2,
                                          qa_updated_df3, qa_updated_df4, qa_updated_df5,
                                          qa_updated_df6, qa_updated_df7], ignore_index=True)
        auto_merged_updated_df = pd.concat([auto_updated_df1, auto_updated_df2,
                                            auto_updated_df3, auto_updated_df4, auto_updated_df5,
                                            auto_updated_df6, auto_updated_df7], ignore_index=True)
        if option == 'Updated':
            header_style(process_type[0],18,"center")
            format_preview_df(qa_merged_updated_df)
            header_style(process_type[1],18,"center")
            format_preview_df(auto_merged_updated_df)
        elif option == 'Template / Uploaded':
            header_style(process_type[0],18,"center")
            format_preview_df(qa_process_data_df)
            header_style(process_type[1],18,"center")
            format_preview_df(automation_process_data_df)

    css = '''
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:18px; font-weight: bold;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    with st.sidebar:
        download_xlsx(qa_merged_updated_df, auto_merged_updated_df)
        maturity_level_status()
                

if __name__ == "__main__":
    main()