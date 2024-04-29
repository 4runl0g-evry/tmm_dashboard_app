import streamlit as st
import pandas as pd

def header_style(header_text, font_size, text_align):
# Display the header with custom CSS
    st.markdown(f"""
        <style>
            /* Define a CSS class for the header */
            .header-text {{
                font-size: {font_size}px; /* Set the font size */
                text-align: {text_align}; /* Set the text alignment */
            }}

            /* Define a CSS class for the divider */
            .divider {{
                margin-top: 0px; /* Adjust the top margin as needed */
                border-top: 1px solid #ccc; /* Define the divider style */
            }}
        </style>
    """, unsafe_allow_html=True)

    # Display the header using the custom CSS class
    st.markdown(f'<p class="header-text">{header_text}</p>', unsafe_allow_html=True)

    # Display the divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def maturity_level_status():
    data = pd.DataFrame({'MATURITY LEVEL': ['INITIAL (LEVEL 1)', 'MANAGED (LEVEL 2)', 'DEFINED (LEVEL 3)', 'MEASURED (LEVEL 4)','OPTIMIZED (LEVEL 5)']})

    # Define the color codes for each row
    color_codes = ['red', '#387E99', '#FFC000', '#F48735', '#00BD32']

    # Apply the specified background color to each cell in the DataFrame
    for i, color in enumerate(color_codes):
        data.at[i, 'MATURITY LEVEL'] = f'<div style="background-color: {color}">{data.at[i, "MATURITY LEVEL"]}</div>'

    # Render the DataFrame using Streamlit
    st.write(data.to_html(escape=False), unsafe_allow_html=True)

    # Add some CSS to hide the index column
    st.markdown("""
    <style>
    table.dataframe th:first-child {
        display: none;
    }
    table.dataframe th {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
