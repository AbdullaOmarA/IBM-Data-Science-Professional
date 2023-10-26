import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Read the data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Dropdown options for the Launch Site
launch_sites = spacex_df['Launch Site'].unique().tolist()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in launch_sites]


app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # Task 1: Add a Dropdown List for Launch Site Selection
    dcc.Dropdown(id='site-dropdown', options=dropdown_options, value='ALL', placeholder="Select a Launch Site"),
    html.Br(),
    # Task 2: Pie Chart Display (Callback defined below)
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    html.P("Payload range (Kg):"),
    # Task 3: Add a Payload Range Slider
    dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, 
                    value=[min_payload, max_payload], 
                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000'},
                    step=1000),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Pie Chart Callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {selected_site}')
    return fig

# Task 4: Scatter Chart Callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title='Correlation between Payload and Success for all Sites' if selected_site == 'ALL' else f'Correlation between Payload and Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
