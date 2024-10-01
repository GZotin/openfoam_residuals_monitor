import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Initializing the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

stop_updates = False

log_file = "./log.rhoSimpleFoam"

# Layout of the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Simulation Monitor', className='text-center')),
    ]),
    dbc.Row([
        dbc.Col(html.P('Log file = ' + log_file)),
        dbc.Col(html.P(id='sim_status', children='Status: Not initialized')),
        dbc.Col(html.P(id='sim_time', children='Time: 0 s')),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='residuals_graph', className='graph')),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='continuity_graph', className='graph')),
    ]),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
], fluid=True)

# Callback to check the simulation status and change color
@app.callback(
    Output('sim_status', 'children'),
    Output('sim_status', 'style'),
    Input('interval-component', 'n_intervals')
)
def update_status(n):
    global log_file

    sim_status = "Status: Not initialized"
    status_color = 'red'  # Initial color for "Not initialized"
    
    with open(log_file, 'r') as file:
        lines = file.readlines()

        # Checking simulation status
        sim_started = any("Starting time loop" in line for line in lines)
        sim_ended = any("End" in line for line in lines)

        if sim_started and not sim_ended:
            sim_status = "Status: Running"
            status_color = 'blue'  # Blue for "Running"
        elif sim_ended:
            sim_status = "Status: Ended"
            status_color = 'green'  # Green for "Ended"

    return sim_status, {'color': status_color}

# Callback to update the simulation time
@app.callback(
        Output('sim_time','children'),
        Input('interval-component','n_intervals')
)
def update_time(n):
    global log_file

    sim_time = "Time: 0 s"

    with open(log_file, 'r') as file:
        for line in file:
            if 'ClockTime' in line:
                var_aux = line.split()
                sim_time = "Time: " + var_aux[6] + " s"
    return sim_time


# Callback to update the residuals graph
@app.callback(
    [Output('residuals_graph', 'figure'),
     Output('interval-component', 'disabled')],
    Input('interval-component', 'n_intervals')
)
def update_graph_residuals(n):
    global stop_updates
    global log_file

    Ux_res = np.array([])
    Uy_res = np.array([])
    Uz_res = np.array([])
    p_res = np.array([])
    k_res = np.array([])
    eps_res = np.array([])
    e_res = np.array([])
    continuity_res = np.array([])

    with open(log_file, 'r') as file:
        for line in file:
            if 'End' in line:
                stop_updates = True

            if 'Solving for Ux,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                Ux_res = np.append(Ux_res, float(var_aux[0]))

            if 'Solving for Uy,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                Uy_res = np.append(Uy_res, float(var_aux[0]))

            if 'Solving for Uz,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                Uz_res = np.append(Uz_res, float(var_aux[0]))

            if 'Solving for p,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                p_res = np.append(p_res, float(var_aux[0]))

            if 'Solving for k,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                k_res = np.append(k_res, float(var_aux[0]))
            
            if 'Solving for epsilon,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                eps_res = np.append(eps_res, float(var_aux[0]))
            
            if 'Solving for e,' in line:
                var_aux = line.split()
                var_aux = var_aux[11].split(',')
                e_res = np.append(e_res, float(var_aux[0]))

            if 'time step continuity errors' in line:
                var_aux = line.split()
                var_aux = var_aux[8].split(',')
                continuity_res = np.append(continuity_res, float(var_aux[0]))



    it = np.arange(1, len(p_res)+1, 1)

    fig = go.Figure()

    # Adding data to the graph
    if len(Ux_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=Ux_res, mode='lines', name='Ux'))
    if len(Uy_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=Uy_res, mode='lines', name='Uy'))
    if len(Uz_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=Uz_res, mode='lines', name='Uz'))
    if len(p_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=p_res, mode='lines', name='p'))
    if len(k_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=k_res, mode='lines', name='k'))
    if len(eps_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=eps_res, mode='lines', name='epsilon'))
    if len(e_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=e_res, mode='lines', name='e'))
    if len(continuity_res) > 0:
        fig.add_trace(go.Scatter(x=it, y=continuity_res, mode='lines', name='continuity'))

    fig.update_layout(
        title={
            'text': "Residuals Monitoring",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial',
                'size': 24,
                'color': 'black'
            }
        },
        xaxis_title={
            'text': 'Iterations',
            'font':  {
                'family': 'Arial',
                'size': 18,
                'color': 'black'
            }
        },
        
        xaxis=dict(
            title = 'Iteration',
            linecolor='black',
            linewidth=2,
            ticks='outside',
            ticklen=8,
            tickwidth=2,
            tickcolor='black',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title = 'Residual',
            linecolor='black',
            linewidth=2,
            ticks='outside',
            ticklen=8,
            tickwidth=2,
            tickcolor='black',
            exponentformat='e',
            gridcolor='lightgray'
        ),
        plot_bgcolor='rgba(249, 249, 249, 1)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        font=dict(family='Arial', size=12, color='black'),
        hovermode='closest'
    )
    fig.update_yaxes(type='log')
    return fig, stop_updates

@app.callback(
    Output('continuity_graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_continuity(n):
    global log_file

    continuity_sum_local = np.array([])
    continuity_global = np.array([])
    continuity_cumulative = np.array([])

    with open(log_file, 'r') as file:
        for line in file:
            if 'time step continuity errors' in line:
                var_aux = line.split()
                var_aux1 = var_aux[8].split(',')
                var_aux2 = var_aux[11].split(',')
                var_aux3 = var_aux[14].split(',')
                continuity_sum_local = np.append(continuity_sum_local, float(var_aux1[0]))
                continuity_global = np.append(continuity_global, float(var_aux2[0]))
                continuity_cumulative = np.append(continuity_cumulative, float(var_aux3[0]))


    it = np.arange(1, len(continuity_global)+1, 1)

    fig = go.Figure()

    # Adding data to the graph
    if len(continuity_sum_local) > 0:
        fig.add_trace(go.Scatter(x=it, y=continuity_sum_local, mode='lines', name='continuity sum local'))
    if len(continuity_global) > 0:
        fig.add_trace(go.Scatter(x=it, y=continuity_global, mode='lines', name='continuity global'))
    if len(continuity_cumulative) > 0:
        fig.add_trace(go.Scatter(x=it, y=continuity_cumulative, mode='lines', name='continuity cumulative'))

    fig.update_layout(
        title={
            'text': "Continuity Monitoring",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial',
                'size': 24,
                'color': 'black'
            }
        },
        xaxis_title={
            'text': 'Iterations',
            'font':  {
                'family': 'Arial',
                'size': 18,
                'color': 'black'
            }
        },
        yaxis_title={
            'text': 'Residual',
            'font':  {
                'family': 'Arial',
                'size': 18,
                'color': 'black'
            }
        },
        xaxis=dict(
            linecolor='black',
            linewidth=2,
            ticks='outside',
            ticklen=8,
            tickwidth=2,
            tickcolor='black',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            linecolor='black',
            linewidth=2,
            ticks='outside',
            ticklen=8,
            tickwidth=2,
            tickcolor='black',
            exponentformat='e',
            gridcolor='lightgray'
        ),
        plot_bgcolor='rgba(249, 249, 249, 1)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        font=dict(family='Arial', size=12, color='black'),
        hovermode='closest'
    )
    return fig


# Start the Dash server
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
