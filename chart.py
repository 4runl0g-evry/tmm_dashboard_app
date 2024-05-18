import streamlit as st
import plotly.graph_objects as go

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
