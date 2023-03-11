import dash
from dash import dcc
import plotly.graph_objs as go
import pandas as pd
import requests
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
from dash import html
from dash.dependencies import Input, Output, State
template_theme1 = "quartz"
template_theme2 = "vapor"
url_theme1 = dbc.themes.QUARTZ
url_theme2 = dbc.themes.LUMEN

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[url_theme2, dbc_css])
def gauge_chart() :
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=270,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speed"}))
    return fig
app.layout = dbc.Container(
    [
        dbc.Row(
            [
            html.Div([
            dbc.Col([dbc.Input(id='input-1-state', type='text', value='Enter the fighter',style={"width":"200px","margin-right":"5px"})]),
             dbc.Col(dbc.Button(id='submit-button-state', color="primary", n_clicks=0, children='Submit')),

            ],style={"display":"flex","margin-top":"10px","justify-content":"space-between","width":"fit-content"})


            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Img(id="profile_image",src="https://www.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png", style={"width": "120px", "height": "120px","margin-bottom":"10px"})),
                dbc.Col(
                    html.Div(
                        [
                            html.H5(id="name", style={"color": "white", "margin-left": "10px","text-align": "center"}),
                            html.H5(id="nickname", style={"color": "white", "margin-left": "10px","text-align": "center"}),
                            html.H5(id="activefighter", style={"color": "white", "margin-left": "10px","text-align": "center"}),
                            html.H5(id="division", style={"color": "white", "margin-left": "10px","text-align": "center"}),
                            html.H5(id="ranking", style={"color": "white", "margin-left": "10px","text-align": "center"}),
                        ]
                        ,style={"background-color": "#52BAE9","height":"120px","border-radius":"5px"}
                    )
                ),
                dbc.Col(html.Div(
                    [

                        html.H5(id="strike_accuracy", style={"color": "darkblue","text-align": "center","padding-top":"15px"}),
                        html.H5(id="strike_landed", style={"color": "white","text-align": "center"}),
                        html.H5(id="strike_attempted", style={"color": "white","text-align": "center"}),
                    ]
                    , style={"background-color": "#52BAE9","height":"120px","border-radius":"5px"})),
                dbc.Col(html.Div(
                    [
                        html.H5(id="takedown_accuracy",style={"color": "darkblue","text-align":"center","padding-top":"15px"}),
                        html.H5(id="takedown_landed", style={"color": "white","text-align": "center"}),
                        html.H5(id="takedown_attempted", style={"color": "white","text-align": "center"}),

                    ]
                    , style={"background-color": "#52BAE9","height":"120px","border-radius":"5px"})),

            ],style={"background-color":"white","padding-top":"10px","padding-bottom":"10px"
                     ,"margin-top":"10px","margin-bottom":"10px","margin-left":"1px","margin-right":"1px"}),

        dbc.Row(
            [

                dbc.Col(
                    [dcc.Loading(children=[dcc.Graph(id="continent_wins_by_type_bar_call",style={"background-color":"#52BAE9","height":"300px"})],type="circle")]
                ),
                dbc.Col(
                    [dcc.Loading(children=[dcc.Graph(id="continent_takedown_bar_call",style={"background-color":"#52BAE9","height":"300px"})],type="circle")]
                ),
                dbc.Col(
                    [dcc.Loading(children=[dcc.Graph(id="continent_strike_la_bar_call",style={"background-color":"#52BAE9","height":"300px"})],type="circle")]
                ),
            ]

        ),
        html.Br(),
        dbc.Row(
            [

                dbc.Col(
                    [dcc.Loading(children = [dcc.Graph(id="continent_strike_pos_bar_call",style={"background-color":"#70757a","height":"300px"})],type="circle")]
                ),
                dbc.Col(
                    [dcc.Loading(children = [dcc.Graph(id="continent_strike_tar_bar_call",style={"background-color":"#70757a","height":"300px"})],type="circle")]

                )
            ]
        ),


    ],
    style= {"background-color":"#033E59","border-radius":"5px","margin-top":"10px","padding-bottom":"10px","margin-bottom":"10px","height":"100%"},

)
colors = ["#031cfc", "#24b514", "#d11d1d"]


def plot_win_by_type(data):
    plot_data = []
    wins_target_data = pd.DataFrame.from_dict(data[0], orient='index')
    plot_data.append(go.Pie(labels=wins_target_data.index.to_list(), values=wins_target_data[0]))
    layout_wins = go.Layout(title=f"Wins by Type",yaxis =  {
                                    'visible': False
                                         })
    fig = go.Figure(data=plot_data, layout=layout_wins)
    return fig

def plot_takedowns_type(data):
    plot_data_takedowns = []
    takedown_data = pd.DataFrame.from_dict(data[1], orient='index')


    cols = takedown_data.index.to_list()

    plot_data_takedowns.append(go.Bar(x=takedown_data.index.to_list(), y=takedown_data[0],text=takedown_data[0], marker=dict(color=colors)))
    layout_takdowns = go.Layout(title=f"Takedowns Attempted/Landed",yaxis =  {
                                    'visible': False
                                         })
    fig =  go.Figure(data=plot_data_takedowns, layout=layout_takdowns)
    return fig

def plot_strikes_la(data):
    plot_data_strikes_la = []
    strike_la_data = pd.DataFrame.from_dict(data[4], orient='index')
    plot_data_strikes_la.append(go.Bar(x=["Strikes Attempted","Strikes Landed"], y=strike_la_data[0],text=strike_la_data[0], marker=dict(color=colors),
            textposition='auto'))
    layout_stikes_la = go.Layout(title=f"Strikes Attempted/Landed",yaxis =  {
                                    'visible': False
                                         })
    fig =  go.Figure(data=plot_data_strikes_la, layout=layout_stikes_la)
    return fig

def plot_strikes_pos(data):
    plot_data_strikes_pos = []
    strikes_position_data = pd.DataFrame.from_dict(data[2], orient='index')
    plot_data_strikes_pos.append(go.Bar(x=strikes_position_data.index.to_list(), y=strikes_position_data[0],text=strikes_position_data[0],marker=dict(color=colors),
            textposition='auto'))
    layout_stikes_la = go.Layout(title=f"Strikes By Position",yaxis =  {
                                    'visible': False})
    fig =  go.Figure(data=plot_data_strikes_pos, layout=layout_stikes_la)
    return fig

def plot_strikes_tar(data):
    plot_data_strikes_tar = []
    strikes_target_data = pd.DataFrame.from_dict(data[3], orient='index')
    plot_data_strikes_tar.append(go.Bar(x=strikes_target_data.index.to_list(), y=strikes_target_data[0],text=strikes_target_data[0],marker=dict(color=colors),
            textposition='auto'))
    layout_stikes_la = go.Layout(title=f"Strikes By Target",yaxis =  {
                                    'visible': False
                                         })
    fig =  go.Figure(data=plot_data_strikes_tar, layout=layout_stikes_la)
    return fig
def profile_image(data) :
    image_url = data[6][5]
    return image_url
def takedowns_laaccu(data) :
    strikes_la = data[1]
    return strikes_la
def strikes_laaccu(data) :
    strikes_la = data[4]
    return strikes_la
def profile_image(data) :
    image_url = data[6][5]
    return image_url

def plot_dis(data):

    fig_wins = plot_win_by_type(data)
    fig_takedowns = plot_takedowns_type(data)
    fig_strikes_la = plot_strikes_la(data)
    fig_strikes_pos = plot_strikes_pos(data)
    fig_strikes_tar = plot_strikes_tar(data)
    image_url = profile_image(data)
    strikes_la = strikes_laaccu(data)
    strkes_l_number = "Landed: "+str(strikes_la['strikr_landed'])
    strikes_a_number ="Attempted: "+str(strikes_la['strike_att'])
    takedowns_la = takedowns_laaccu(data)
    takedown_l_number = "Landed: "+str(takedowns_la['landed'])
    takedowns_a_number = "Attempted: "+str(takedowns_la['attempted'])
    stries_accuracy ="Strikes Accuracy " + str(round(int(strikes_la['strikr_landed'])/int(strikes_la['strike_att'])*100,2))+"%"
    takedown_accuracy ="Takedowns Accuracy "+str(round(int(takedowns_la['landed'])/int(takedowns_la['attempted'])*100,2))+"%"
    name = data[-1][1]
    nickname = data[-1][0]
    division = data[-1][2]
    ranking = data[-1][3]
    return fig_wins,fig_takedowns, fig_strikes_la, fig_strikes_pos,fig_strikes_tar,image_url,strkes_l_number,strikes_a_number,takedown_l_number,takedowns_a_number,stries_accuracy,takedown_accuracy,name,nickname,division,ranking
@app.callback(Output('continent_wins_by_type_bar_call', 'figure'),
              Output('continent_takedown_bar_call', 'figure'),
              Output('continent_strike_la_bar_call', 'figure'),
              Output('continent_strike_pos_bar_call', 'figure'),
              Output('continent_strike_tar_bar_call', 'figure'),
              Output('profile_image', 'src'),
              Output('strike_landed', 'children'),
              Output('strike_attempted', 'children'),
              Output('takedown_landed', 'children'),
              Output('takedown_attempted', 'children'),
              Output('strike_accuracy', 'children'),
              Output('takedown_accuracy', 'children'),
              Output('name', 'children'),
              Output('nickname', 'children'),
              Output('division', 'children'),
              Output('ranking', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))

def update_output(n_clicks, input1):
    if n_clicks==0:
        raise PreventUpdate
    else:
        first = input1.split(" ")[0]
        second = input1.split(" ")[1]
        donnees = requests.get("http://127.0.0.1:5000/"+first+"-"+second)
        x = donnees.json()
        return plot_dis(x)

if __name__ == "__main__":
    app.run_server(port=4050, debug=True)
