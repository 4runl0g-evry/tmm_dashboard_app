import streamlit as st
import plotly.graph_objects as go

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

# Prepare data for the pie chart
def pie_chart(area_percent_dict):
    labels = list(area_percent_dict.keys())
    sizes = list(area_percent_dict.values())

    # Calculate the percentage of tasks not completed for each task
    not_completed_sizes = [100 - value for value in sizes]

    # Create a single pie chart showing the percentage of tasks not completed
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=not_completed_sizes,
        hoverinfo='label+percent+value',
        textinfo='percent',
        textposition='inside',
        hole=.5
    ))

    # Update layout for better presentation
    fig.update_layout(
        # title_text='Pending areas / Gaps',
        annotations=[dict(text='Pending Areas', x=0.5, y=0.5, font_size=10, showarrow=False)]
    )
    return fig

# Display the details of each task
# st.write('### Task Completion Details:')
# for task_name, task_percentage in tasks.items():
    # st.write(f'{task_name}: {task_percentage}% completed, {100 - task_percentage}% not completed')
